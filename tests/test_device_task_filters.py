import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "android/app/src/main/python"))

from task_filters import (
    clean_keyword_tags,
    copy_or_fallback,
    deliver_task_message,
    is_protected,
    iter_message_ids,
    matches_message_filters,
    message_category,
    split_filter_values,
)


def message(**values):
    defaults = {
        "video": None,
        "audio": None,
        "voice": None,
        "photo": None,
        "animation": None,
        "document": None,
        "sticker": None,
        "text": None,
        "caption": "",
        "has_protected_content": False,
        "chat": SimpleNamespace(has_protected_content=False),
    }
    defaults.update(values)
    return SimpleNamespace(**defaults)


class DeviceTaskFilterTests(unittest.TestCase):
    def test_filter_values_are_trimmed_and_case_insensitive(self):
        self.assertEqual(split_filter_values(" Video, audio,video "), {"video", "audio"})

    def test_media_type_and_include_keyword_match_caption(self):
        item = message(video=SimpleNamespace(file_name="episode.mkv"), caption="Season 2")
        self.assertEqual(message_category(item), "video")
        self.assertTrue(matches_message_filters(item, {"video"}, {"season 2"}, set()))

    def test_excluded_keyword_and_wrong_media_type_are_rejected(self):
        item = message(document=SimpleNamespace(file_name="sample.pdf"), caption="Trailer")
        self.assertFalse(matches_message_filters(item, {"document"}, set(), {"trailer"}))
        self.assertFalse(matches_message_filters(item, {"video"}, set(), set()))

    def test_voice_is_classified_as_audio(self):
        item = message(voice=SimpleNamespace(file_name="note.ogg"))
        self.assertEqual(message_category(item), "voice")
        self.assertTrue(matches_message_filters(item, {"voice"}, set(), set()))

    def test_text_and_sticker_categories_match_web_task_types(self):
        text = message(text="release notes")
        sticker = message(sticker=SimpleNamespace(file_name="sticker.webp"))
        self.assertEqual(message_category(text), "text")
        self.assertEqual(message_category(sticker), "sticker")
        self.assertTrue(matches_message_filters(text, {"text"}, {"release"}, set()))
        self.assertTrue(matches_message_filters(sticker, {"sticker"}, set(), set()))

    def test_protected_message_or_chat_is_rejected(self):
        self.assertTrue(is_protected(message(has_protected_content=True)))
        self.assertTrue(is_protected(message(chat=SimpleNamespace(has_protected_content=True))))
        self.assertFalse(is_protected(message()))

    def test_cleanup_tags_are_removed_case_insensitively(self):
        self.assertEqual(clean_keyword_tags("Show @Tag and TAG", ["@tag", "tag"]),
                         "Show  and")

    def test_message_range_has_no_fixed_batch_ceiling(self):
        message_ids = iter_message_ids(1, 100_001)
        self.assertEqual(message_ids.start, 1)
        self.assertEqual(message_ids.stop, 100_002)
        self.assertEqual(message_ids.step, 1)

    def test_message_range_rejects_invalid_ids(self):
        with self.assertRaises(ValueError):
            iter_message_ids(0, 5)
        with self.assertRaises(ValueError):
            iter_message_ids(10, 5)


class CopyFallbackTests(unittest.IsolatedAsyncioTestCase):
    async def test_unrestricted_media_uses_copy(self):
        calls = []

        async def copy_operation():
            calls.append("copy")
            return "copied"

        async def fallback_operation():
            calls.append("fallback")
            return "uploaded"

        result = await copy_or_fallback(message(), copy_operation, fallback_operation)

        self.assertEqual(result, "copied")
        self.assertEqual(calls, ["copy"])

    async def test_protected_media_uses_download_fallback(self):
        calls = []

        async def copy_operation():
            calls.append("copy")
            return "copied"

        async def fallback_operation():
            calls.append("fallback")
            return "uploaded"

        result = await copy_or_fallback(
            message(has_protected_content=True), copy_operation, fallback_operation)

        self.assertEqual(result, "uploaded")
        self.assertEqual(calls, ["fallback"])

    async def test_forward_restriction_uses_download_fallback(self):
        async def copy_operation():
            raise RuntimeError("CHAT_FORWARDS_RESTRICTED")

        async def fallback_operation():
            return "uploaded"

        result = await copy_or_fallback(message(), copy_operation, fallback_operation)

        self.assertEqual(result, "uploaded")

    async def test_cleanup_can_force_download_fallback(self):
        calls = []

        async def copy_operation():
            calls.append("copy")
            return "copied"

        async def fallback_operation():
            calls.append("fallback")
            return "uploaded"

        result = await copy_or_fallback(
            message(), copy_operation, fallback_operation, force_fallback=True)

        self.assertEqual(result, "uploaded")
        self.assertEqual(calls, ["fallback"])

    async def test_unrelated_copy_failure_does_not_trigger_download(self):
        calls = []

        async def copy_operation():
            raise RuntimeError("NETWORK_TIMEOUT")

        async def fallback_operation():
            calls.append("fallback")
            return "uploaded"

        with self.assertRaisesRegex(RuntimeError, "NETWORK_TIMEOUT"):
            await copy_or_fallback(message(), copy_operation, fallback_operation)
        self.assertEqual(calls, [])


class TransferModeTests(unittest.IsolatedAsyncioTestCase):
    async def test_forward_mode_never_downloads(self):
        calls = []

        async def forward():
            calls.append("forward")
            return "forwarded"

        async def download():
            calls.append("download")
            return "downloaded"

        result = await deliver_task_message("FORWARD", message(), forward, download)

        self.assertEqual(result, "forwarded")
        self.assertEqual(calls, ["forward"])

    async def test_download_mode_never_forwards(self):
        calls = []

        async def forward():
            calls.append("forward")
            return "forwarded"

        async def download():
            calls.append("download")
            return "downloaded"

        result = await deliver_task_message("DOWNLOAD", message(), forward, download)

        self.assertEqual(result, "downloaded")
        self.assertEqual(calls, ["download"])

    async def test_unknown_transfer_mode_is_rejected(self):
        async def unused():
            self.fail("No operation should run for an unknown mode")

        with self.assertRaisesRegex(ValueError, "Transfer mode"):
            await deliver_task_message("SOMETHING_ELSE", message(), unused, unused)

    async def test_auto_mode_keeps_copy_then_fallback_behavior(self):
        calls = []

        async def forward():
            calls.append("forward")
            return "forwarded"

        async def copy():
            calls.append("copy")
            raise RuntimeError("CHAT_FORWARDS_RESTRICTED")

        async def download():
            calls.append("download")
            return "downloaded"

        result = await deliver_task_message(
            "AUTO", message(), forward, download, copy_operation=copy)

        self.assertEqual(result, "downloaded")
        self.assertEqual(calls, ["copy", "download"])

    async def test_forward_mode_does_not_fall_back_to_download(self):
        calls = []

        async def forward():
            calls.append("forward")
            raise RuntimeError("CHAT_FORWARDS_RESTRICTED")

        async def download():
            calls.append("download")
            return "downloaded"

        with self.assertRaisesRegex(RuntimeError, "CHAT_FORWARDS_RESTRICTED"):
            await deliver_task_message("FORWARD", message(), forward, download)
        self.assertEqual(calls, ["forward"])

    async def test_false_copy_result_is_not_reported_as_success(self):
        async def copy_operation():
            return None

        async def fallback_operation():
            return "uploaded"

        with self.assertRaisesRegex(RuntimeError, "no result"):
            await copy_or_fallback(message(), copy_operation, fallback_operation)


if __name__ == "__main__":
    unittest.main()
