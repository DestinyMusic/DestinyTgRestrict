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


class ComposeRichMessageWithAI(TLObject["raw.base.messages.ComposedRichMessageWithAI"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``8D7AE6AF``

    Parameters:
        proofread (``bool``, *optional*):
            N/A

        emojify (``bool``, *optional*):
            N/A

        text (:obj:`InputRichMessage <pyrogram.raw.base.InputRichMessage>`, *optional*):
            N/A

        translate_to_lang (``str``, *optional*):
            N/A

        tone (:obj:`InputAiComposeTone <pyrogram.raw.base.InputAiComposeTone>`, *optional*):
            N/A

    Returns:
        :obj:`messages.ComposedRichMessageWithAI <pyrogram.raw.base.messages.ComposedRichMessageWithAI>`
    """

    __slots__: List[str] = ["proofread", "emojify", "text", "translate_to_lang", "tone"]

    ID = 0x8d7ae6af
    QUALNAME = "functions.messages.ComposeRichMessageWithAI"

    def __init__(self, *, proofread: Optional[bool] = None, emojify: Optional[bool] = None, text: "raw.base.InputRichMessage" = None, translate_to_lang: Optional[str] = None, tone: "raw.base.InputAiComposeTone" = None) -> None:
        self.proofread = proofread  # flags.0?true
        self.emojify = emojify  # flags.3?true
        self.text = text  # flags.4?InputRichMessage
        self.translate_to_lang = translate_to_lang  # flags.1?string
        self.tone = tone  # flags.2?InputAiComposeTone

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ComposeRichMessageWithAI":
        
        flags = Int.read(b)
        
        proofread = True if flags & (1 << 0) else False
        emojify = True if flags & (1 << 3) else False
        text = TLObject.read(b) if flags & (1 << 4) else None
        
        translate_to_lang = String.read(b) if flags & (1 << 1) else None
        tone = TLObject.read(b) if flags & (1 << 2) else None
        
        return ComposeRichMessageWithAI(proofread=proofread, emojify=emojify, text=text, translate_to_lang=translate_to_lang, tone=tone)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.proofread else 0
        flags |= (1 << 3) if self.emojify else 0
        flags |= (1 << 4) if self.text is not None else 0
        flags |= (1 << 1) if self.translate_to_lang is not None else 0
        flags |= (1 << 2) if self.tone is not None else 0
        b.write(Int(flags))
        
        if self.text is not None:
            b.write(self.text.write())
        
        if self.translate_to_lang is not None:
            b.write(String(self.translate_to_lang))
        
        if self.tone is not None:
            b.write(self.tone.write())
        
        return b.getvalue()
