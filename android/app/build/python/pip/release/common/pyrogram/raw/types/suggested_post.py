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


class SuggestedPost(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.SuggestedPost`.

    Details:
        - Layer: ``228``
        - ID: ``E8E37E5``

    Parameters:
        accepted (``bool``, *optional*):
            N/A

        rejected (``bool``, *optional*):
            N/A

        price (:obj:`StarsAmount <pyrogram.raw.base.StarsAmount>`, *optional*):
            N/A

        schedule_date (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["accepted", "rejected", "price", "schedule_date"]

    ID = 0xe8e37e5
    QUALNAME = "types.SuggestedPost"

    def __init__(self, *, accepted: Optional[bool] = None, rejected: Optional[bool] = None, price: "raw.base.StarsAmount" = None, schedule_date: Optional[int] = None) -> None:
        self.accepted = accepted  # flags.1?true
        self.rejected = rejected  # flags.2?true
        self.price = price  # flags.3?StarsAmount
        self.schedule_date = schedule_date  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SuggestedPost":
        
        flags = Int.read(b)
        
        accepted = True if flags & (1 << 1) else False
        rejected = True if flags & (1 << 2) else False
        price = TLObject.read(b) if flags & (1 << 3) else None
        
        schedule_date = Int.read(b) if flags & (1 << 0) else None
        return SuggestedPost(accepted=accepted, rejected=rejected, price=price, schedule_date=schedule_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.accepted else 0
        flags |= (1 << 2) if self.rejected else 0
        flags |= (1 << 3) if self.price is not None else 0
        flags |= (1 << 0) if self.schedule_date is not None else 0
        b.write(Int(flags))
        
        if self.price is not None:
            b.write(self.price.write())
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        return b.getvalue()
