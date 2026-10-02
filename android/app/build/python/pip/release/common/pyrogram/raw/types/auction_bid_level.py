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


class AuctionBidLevel(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.AuctionBidLevel`.

    Details:
        - Layer: ``228``
        - ID: ``310240CC``

    Parameters:
        pos (``int`` ``32-bit``):
            N/A

        amount (``int`` ``64-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["pos", "amount", "date"]

    ID = 0x310240cc
    QUALNAME = "types.AuctionBidLevel"

    def __init__(self, *, pos: int, amount: int, date: int) -> None:
        self.pos = pos  # int
        self.amount = amount  # long
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AuctionBidLevel":
        # No flags
        
        pos = Int.read(b)
        
        amount = Long.read(b)
        
        date = Int.read(b)
        
        return AuctionBidLevel(pos=pos, amount=amount, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.pos))
        
        b.write(Long(self.amount))
        
        b.write(Int(self.date))
        
        return b.getvalue()
