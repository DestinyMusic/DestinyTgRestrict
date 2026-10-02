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


class StarGiftAuctionRoundExtendable(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarGiftAuctionRound`.

    Details:
        - Layer: ``228``
        - ID: ``AA021E5``

    Parameters:
        num (``int`` ``32-bit``):
            N/A

        duration (``int`` ``32-bit``):
            N/A

        extend_top (``int`` ``32-bit``):
            N/A

        extend_window (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["num", "duration", "extend_top", "extend_window"]

    ID = 0xaa021e5
    QUALNAME = "types.StarGiftAuctionRoundExtendable"

    def __init__(self, *, num: int, duration: int, extend_top: int, extend_window: int) -> None:
        self.num = num  # int
        self.duration = duration  # int
        self.extend_top = extend_top  # int
        self.extend_window = extend_window  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGiftAuctionRoundExtendable":
        # No flags
        
        num = Int.read(b)
        
        duration = Int.read(b)
        
        extend_top = Int.read(b)
        
        extend_window = Int.read(b)
        
        return StarGiftAuctionRoundExtendable(num=num, duration=duration, extend_top=extend_top, extend_window=extend_window)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.num))
        
        b.write(Int(self.duration))
        
        b.write(Int(self.extend_top))
        
        b.write(Int(self.extend_window))
        
        return b.getvalue()
