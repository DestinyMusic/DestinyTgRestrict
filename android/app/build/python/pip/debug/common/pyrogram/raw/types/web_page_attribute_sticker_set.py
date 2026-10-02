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


class WebPageAttributeStickerSet(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.WebPageAttribute`.

    Details:
        - Layer: ``228``
        - ID: ``50CC03D3``

    Parameters:
        stickers (List of :obj:`Document <pyrogram.raw.base.Document>`):
            N/A

        emojis (``bool``, *optional*):
            N/A

        text_color (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["stickers", "emojis", "text_color"]

    ID = 0x50cc03d3
    QUALNAME = "types.WebPageAttributeStickerSet"

    def __init__(self, *, stickers: List["raw.base.Document"], emojis: Optional[bool] = None, text_color: Optional[bool] = None) -> None:
        self.stickers = stickers  # Vector<Document>
        self.emojis = emojis  # flags.0?true
        self.text_color = text_color  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebPageAttributeStickerSet":
        
        flags = Int.read(b)
        
        emojis = True if flags & (1 << 0) else False
        text_color = True if flags & (1 << 1) else False
        stickers = TLObject.read(b)
        
        return WebPageAttributeStickerSet(stickers=stickers, emojis=emojis, text_color=text_color)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.emojis else 0
        flags |= (1 << 1) if self.text_color else 0
        b.write(Int(flags))
        
        b.write(Vector(self.stickers))
        
        return b.getvalue()
