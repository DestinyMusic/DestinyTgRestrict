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


class Birthday(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Birthday`.

    Details:
        - Layer: ``228``
        - ID: ``6C8E1E06``

    Parameters:
        day (``int`` ``32-bit``):
            N/A

        month (``int`` ``32-bit``):
            N/A

        year (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["day", "month", "year"]

    ID = 0x6c8e1e06
    QUALNAME = "types.Birthday"

    def __init__(self, *, day: int, month: int, year: Optional[int] = None) -> None:
        self.day = day  # int
        self.month = month  # int
        self.year = year  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Birthday":
        
        flags = Int.read(b)
        
        day = Int.read(b)
        
        month = Int.read(b)
        
        year = Int.read(b) if flags & (1 << 0) else None
        return Birthday(day=day, month=month, year=year)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.year is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.day))
        
        b.write(Int(self.month))
        
        if self.year is not None:
            b.write(Int(self.year))
        
        return b.getvalue()
