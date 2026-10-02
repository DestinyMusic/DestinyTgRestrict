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


class BusinessWeeklyOpen(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.BusinessWeeklyOpen`.

    Details:
        - Layer: ``228``
        - ID: ``120B1AB9``

    Parameters:
        start_minute (``int`` ``32-bit``):
            N/A

        end_minute (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["start_minute", "end_minute"]

    ID = 0x120b1ab9
    QUALNAME = "types.BusinessWeeklyOpen"

    def __init__(self, *, start_minute: int, end_minute: int) -> None:
        self.start_minute = start_minute  # int
        self.end_minute = end_minute  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BusinessWeeklyOpen":
        # No flags
        
        start_minute = Int.read(b)
        
        end_minute = Int.read(b)
        
        return BusinessWeeklyOpen(start_minute=start_minute, end_minute=end_minute)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.start_minute))
        
        b.write(Int(self.end_minute))
        
        return b.getvalue()
