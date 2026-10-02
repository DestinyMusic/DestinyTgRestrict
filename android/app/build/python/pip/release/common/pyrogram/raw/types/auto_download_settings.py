#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO
from typing import TYPE_CHECKING, List, Optional, Any

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject

if TYPE_CHECKING:
    from pyrogram import raw

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class AutoDownloadSettings(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.AutoDownloadSettings`.

    Details:
        - Layer: ``228``
        - ID: ``BAA57628``

    Parameters:
        photo_size_max (``int`` ``32-bit``):
            N/A

        video_size_max (``int`` ``64-bit``):
            N/A

        file_size_max (``int`` ``64-bit``):
            N/A

        video_upload_maxbitrate (``int`` ``32-bit``):
            N/A

        small_queue_active_operations_max (``int`` ``32-bit``):
            N/A

        large_queue_active_operations_max (``int`` ``32-bit``):
            N/A

        disabled (``bool``, *optional*):
            N/A

        video_preload_large (``bool``, *optional*):
            N/A

        audio_preload_next (``bool``, *optional*):
            N/A

        phonecalls_less_data (``bool``, *optional*):
            N/A

        stories_preload (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["photo_size_max", "video_size_max", "file_size_max", "video_upload_maxbitrate", "small_queue_active_operations_max", "large_queue_active_operations_max", "disabled", "video_preload_large", "audio_preload_next", "phonecalls_less_data", "stories_preload"]

    ID = 0xbaa57628
    QUALNAME = "types.AutoDownloadSettings"

    def __init__(self, *, photo_size_max: int, video_size_max: int, file_size_max: int, video_upload_maxbitrate: int, small_queue_active_operations_max: int, large_queue_active_operations_max: int, disabled: Optional[bool] = None, video_preload_large: Optional[bool] = None, audio_preload_next: Optional[bool] = None, phonecalls_less_data: Optional[bool] = None, stories_preload: Optional[bool] = None) -> None:
        self.photo_size_max = photo_size_max  # int
        self.video_size_max = video_size_max  # long
        self.file_size_max = file_size_max  # long
        self.video_upload_maxbitrate = video_upload_maxbitrate  # int
        self.small_queue_active_operations_max = small_queue_active_operations_max  # int
        self.large_queue_active_operations_max = large_queue_active_operations_max  # int
        self.disabled = disabled  # flags.0?true
        self.video_preload_large = video_preload_large  # flags.1?true
        self.audio_preload_next = audio_preload_next  # flags.2?true
        self.phonecalls_less_data = phonecalls_less_data  # flags.3?true
        self.stories_preload = stories_preload  # flags.4?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AutoDownloadSettings":
        
        flags = Int.read(b)
        
        disabled = True if flags & (1 << 0) else False
        video_preload_large = True if flags & (1 << 1) else False
        audio_preload_next = True if flags & (1 << 2) else False
        phonecalls_less_data = True if flags & (1 << 3) else False
        stories_preload = True if flags & (1 << 4) else False
        photo_size_max = Int.read(b)
        
        video_size_max = Long.read(b)
        
        file_size_max = Long.read(b)
        
        video_upload_maxbitrate = Int.read(b)
        
        small_queue_active_operations_max = Int.read(b)
        
        large_queue_active_operations_max = Int.read(b)
        
        return AutoDownloadSettings(photo_size_max=photo_size_max, video_size_max=video_size_max, file_size_max=file_size_max, video_upload_maxbitrate=video_upload_maxbitrate, small_queue_active_operations_max=small_queue_active_operations_max, large_queue_active_operations_max=large_queue_active_operations_max, disabled=disabled, video_preload_large=video_preload_large, audio_preload_next=audio_preload_next, phonecalls_less_data=phonecalls_less_data, stories_preload=stories_preload)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.disabled else 0
        flags |= (1 << 1) if self.video_preload_large else 0
        flags |= (1 << 2) if self.audio_preload_next else 0
        flags |= (1 << 3) if self.phonecalls_less_data else 0
        flags |= (1 << 4) if self.stories_preload else 0
        b.write(Int(flags))
        
        b.write(Int(self.photo_size_max))
        
        b.write(Long(self.video_size_max))
        
        b.write(Long(self.file_size_max))
        
        b.write(Int(self.video_upload_maxbitrate))
        
        b.write(Int(self.small_queue_active_operations_max))
        
        b.write(Int(self.large_queue_active_operations_max))
        
        return b.getvalue()
