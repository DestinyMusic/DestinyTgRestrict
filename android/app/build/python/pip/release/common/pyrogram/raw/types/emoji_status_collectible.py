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


class EmojiStatusCollectible(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.EmojiStatus`.

    Details:
        - Layer: ``228``
        - ID: ``7184603B``

    Parameters:
        collectible_id (``int`` ``64-bit``):
            N/A

        document_id (``int`` ``64-bit``):
            N/A

        title (``str``):
            N/A

        slug (``str``):
            N/A

        pattern_document_id (``int`` ``64-bit``):
            N/A

        center_color (``int`` ``32-bit``):
            N/A

        edge_color (``int`` ``32-bit``):
            N/A

        pattern_color (``int`` ``32-bit``):
            N/A

        text_color (``int`` ``32-bit``):
            N/A

        until (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["collectible_id", "document_id", "title", "slug", "pattern_document_id", "center_color", "edge_color", "pattern_color", "text_color", "until"]

    ID = 0x7184603b
    QUALNAME = "types.EmojiStatusCollectible"

    def __init__(self, *, collectible_id: int, document_id: int, title: str, slug: str, pattern_document_id: int, center_color: int, edge_color: int, pattern_color: int, text_color: int, until: Optional[int] = None) -> None:
        self.collectible_id = collectible_id  # long
        self.document_id = document_id  # long
        self.title = title  # string
        self.slug = slug  # string
        self.pattern_document_id = pattern_document_id  # long
        self.center_color = center_color  # int
        self.edge_color = edge_color  # int
        self.pattern_color = pattern_color  # int
        self.text_color = text_color  # int
        self.until = until  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiStatusCollectible":
        
        flags = Int.read(b)
        
        collectible_id = Long.read(b)
        
        document_id = Long.read(b)
        
        title = String.read(b)
        
        slug = String.read(b)
        
        pattern_document_id = Long.read(b)
        
        center_color = Int.read(b)
        
        edge_color = Int.read(b)
        
        pattern_color = Int.read(b)
        
        text_color = Int.read(b)
        
        until = Int.read(b) if flags & (1 << 0) else None
        return EmojiStatusCollectible(collectible_id=collectible_id, document_id=document_id, title=title, slug=slug, pattern_document_id=pattern_document_id, center_color=center_color, edge_color=edge_color, pattern_color=pattern_color, text_color=text_color, until=until)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.until is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.collectible_id))
        
        b.write(Long(self.document_id))
        
        b.write(String(self.title))
        
        b.write(String(self.slug))
        
        b.write(Long(self.pattern_document_id))
        
        b.write(Int(self.center_color))
        
        b.write(Int(self.edge_color))
        
        b.write(Int(self.pattern_color))
        
        b.write(Int(self.text_color))
        
        if self.until is not None:
            b.write(Int(self.until))
        
        return b.getvalue()
