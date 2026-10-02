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


class StarsRevenueStatus(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarsRevenueStatus`.

    Details:
        - Layer: ``228``
        - ID: ``FEBE5491``

    Parameters:
        current_balance (:obj:`StarsAmount <pyrogram.raw.base.StarsAmount>`):
            N/A

        available_balance (:obj:`StarsAmount <pyrogram.raw.base.StarsAmount>`):
            N/A

        overall_revenue (:obj:`StarsAmount <pyrogram.raw.base.StarsAmount>`):
            N/A

        withdrawal_enabled (``bool``, *optional*):
            N/A

        next_withdrawal_at (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["current_balance", "available_balance", "overall_revenue", "withdrawal_enabled", "next_withdrawal_at"]

    ID = 0xfebe5491
    QUALNAME = "types.StarsRevenueStatus"

    def __init__(self, *, current_balance: "raw.base.StarsAmount", available_balance: "raw.base.StarsAmount", overall_revenue: "raw.base.StarsAmount", withdrawal_enabled: Optional[bool] = None, next_withdrawal_at: Optional[int] = None) -> None:
        self.current_balance = current_balance  # StarsAmount
        self.available_balance = available_balance  # StarsAmount
        self.overall_revenue = overall_revenue  # StarsAmount
        self.withdrawal_enabled = withdrawal_enabled  # flags.0?true
        self.next_withdrawal_at = next_withdrawal_at  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsRevenueStatus":
        
        flags = Int.read(b)
        
        withdrawal_enabled = True if flags & (1 << 0) else False
        current_balance = TLObject.read(b)
        
        available_balance = TLObject.read(b)
        
        overall_revenue = TLObject.read(b)
        
        next_withdrawal_at = Int.read(b) if flags & (1 << 1) else None
        return StarsRevenueStatus(current_balance=current_balance, available_balance=available_balance, overall_revenue=overall_revenue, withdrawal_enabled=withdrawal_enabled, next_withdrawal_at=next_withdrawal_at)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.withdrawal_enabled else 0
        flags |= (1 << 1) if self.next_withdrawal_at is not None else 0
        b.write(Int(flags))
        
        b.write(self.current_balance.write())
        
        b.write(self.available_balance.write())
        
        b.write(self.overall_revenue.write())
        
        if self.next_withdrawal_at is not None:
            b.write(Int(self.next_withdrawal_at))
        
        return b.getvalue()
