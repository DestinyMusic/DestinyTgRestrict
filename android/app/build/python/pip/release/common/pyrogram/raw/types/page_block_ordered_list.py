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


class PageBlockOrderedList(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PageBlock`.

    Details:
        - Layer: ``228``
        - ID: ``1FD6F6C1``

    Parameters:
        items (List of :obj:`PageListOrderedItem <pyrogram.raw.base.PageListOrderedItem>`):
            N/A

        reversed (``bool``, *optional*):
            N/A

        start (``int`` ``32-bit``, *optional*):
            N/A

        type (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["items", "reversed", "start", "type"]

    ID = 0x1fd6f6c1
    QUALNAME = "types.PageBlockOrderedList"

    def __init__(self, *, items: List["raw.base.PageListOrderedItem"], reversed: Optional[bool] = None, start: Optional[int] = None, type: Optional[str] = None) -> None:
        self.items = items  # Vector<PageListOrderedItem>
        self.reversed = reversed  # flags.2?true
        self.start = start  # flags.0?int
        self.type = type  # flags.1?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockOrderedList":
        
        flags = Int.read(b)
        
        reversed = True if flags & (1 << 2) else False
        items = TLObject.read(b)
        
        start = Int.read(b) if flags & (1 << 0) else None
        type = String.read(b) if flags & (1 << 1) else None
        return PageBlockOrderedList(items=items, reversed=reversed, start=start, type=type)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.reversed else 0
        flags |= (1 << 0) if self.start is not None else 0
        flags |= (1 << 1) if self.type is not None else 0
        b.write(Int(flags))
        
        b.write(Vector(self.items))
        
        if self.start is not None:
            b.write(Int(self.start))
        
        if self.type is not None:
            b.write(String(self.type))
        
        return b.getvalue()
