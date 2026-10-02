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


class Timezone(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Timezone`.

    Details:
        - Layer: ``228``
        - ID: ``FF9289F5``

    Parameters:
        id (``str``):
            N/A

        name (``str``):
            N/A

        utc_offset (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["id", "name", "utc_offset"]

    ID = 0xff9289f5
    QUALNAME = "types.Timezone"

    def __init__(self, *, id: str, name: str, utc_offset: int) -> None:
        self.id = id  # string
        self.name = name  # string
        self.utc_offset = utc_offset  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Timezone":
        # No flags
        
        id = String.read(b)
        
        name = String.read(b)
        
        utc_offset = Int.read(b)
        
        return Timezone(id=id, name=name, utc_offset=utc_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(String(self.name))
        
        b.write(Int(self.utc_offset))
        
        return b.getvalue()
