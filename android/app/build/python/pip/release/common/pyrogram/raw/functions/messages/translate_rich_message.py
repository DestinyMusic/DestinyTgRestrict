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


class TranslateRichMessage(TLObject["raw.base.messages.TranslatedRichMessage"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``1A542004``

    Parameters:
        to_lang (``str``):
            N/A

        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            N/A

        id (List of ``int`` ``32-bit``, *optional*):
            N/A

        text (List of :obj:`InputRichMessage <pyrogram.raw.base.InputRichMessage>`, *optional*):
            N/A

        tone (``str``, *optional*):
            N/A

    Returns:
        :obj:`messages.TranslatedRichMessage <pyrogram.raw.base.messages.TranslatedRichMessage>`
    """

    __slots__: List[str] = ["to_lang", "peer", "id", "text", "tone"]

    ID = 0x1a542004
    QUALNAME = "functions.messages.TranslateRichMessage"

    def __init__(self, *, to_lang: str, peer: "raw.base.InputPeer" = None, id: Optional[List[int]] = None, text: Optional[List["raw.base.InputRichMessage"]] = None, tone: Optional[str] = None) -> None:
        self.to_lang = to_lang  # string
        self.peer = peer  # flags.0?InputPeer
        self.id = id  # flags.0?Vector<int>
        self.text = text  # flags.1?Vector<InputRichMessage>
        self.tone = tone  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TranslateRichMessage":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b) if flags & (1 << 0) else None
        
        id = TLObject.read(b, Int) if flags & (1 << 0) else []
        
        text = TLObject.read(b) if flags & (1 << 1) else []
        
        to_lang = String.read(b)
        
        tone = String.read(b) if flags & (1 << 2) else None
        return TranslateRichMessage(to_lang=to_lang, peer=peer, id=id, text=text, tone=tone)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.peer is not None else 0
        flags |= (1 << 0) if self.id else 0
        flags |= (1 << 1) if self.text else 0
        flags |= (1 << 2) if self.tone is not None else 0
        b.write(Int(flags))
        
        if self.peer is not None:
            b.write(self.peer.write())
        
        if self.id:
            b.write(Vector(self.id, Int))
        
        if self.text:
            b.write(Vector(self.text))
        
        b.write(String(self.to_lang))
        
        if self.tone is not None:
            b.write(String(self.tone))
        
        return b.getvalue()
