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


class GiveawayInfoResults(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.GiveawayInfo`.

    Details:
        - Layer: ``228``
        - ID: ``E175E66F``

    Parameters:
        start_date (``int`` ``32-bit``):
            N/A

        finish_date (``int`` ``32-bit``):
            N/A

        winners_count (``int`` ``32-bit``):
            N/A

        winner (``bool``, *optional*):
            N/A

        refunded (``bool``, *optional*):
            N/A

        gift_code_slug (``str``, *optional*):
            N/A

        stars_prize (``int`` ``64-bit``, *optional*):
            N/A

        activated_count (``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetGiveawayInfo
    """

    __slots__: List[str] = ["start_date", "finish_date", "winners_count", "winner", "refunded", "gift_code_slug", "stars_prize", "activated_count"]

    ID = 0xe175e66f
    QUALNAME = "types.payments.GiveawayInfoResults"

    def __init__(self, *, start_date: int, finish_date: int, winners_count: int, winner: Optional[bool] = None, refunded: Optional[bool] = None, gift_code_slug: Optional[str] = None, stars_prize: Optional[int] = None, activated_count: Optional[int] = None) -> None:
        self.start_date = start_date  # int
        self.finish_date = finish_date  # int
        self.winners_count = winners_count  # int
        self.winner = winner  # flags.0?true
        self.refunded = refunded  # flags.1?true
        self.gift_code_slug = gift_code_slug  # flags.3?string
        self.stars_prize = stars_prize  # flags.4?long
        self.activated_count = activated_count  # flags.2?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GiveawayInfoResults":
        
        flags = Int.read(b)
        
        winner = True if flags & (1 << 0) else False
        refunded = True if flags & (1 << 1) else False
        start_date = Int.read(b)
        
        gift_code_slug = String.read(b) if flags & (1 << 3) else None
        stars_prize = Long.read(b) if flags & (1 << 4) else None
        finish_date = Int.read(b)
        
        winners_count = Int.read(b)
        
        activated_count = Int.read(b) if flags & (1 << 2) else None
        return GiveawayInfoResults(start_date=start_date, finish_date=finish_date, winners_count=winners_count, winner=winner, refunded=refunded, gift_code_slug=gift_code_slug, stars_prize=stars_prize, activated_count=activated_count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.winner else 0
        flags |= (1 << 1) if self.refunded else 0
        flags |= (1 << 3) if self.gift_code_slug is not None else 0
        flags |= (1 << 4) if self.stars_prize is not None else 0
        flags |= (1 << 2) if self.activated_count is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.start_date))
        
        if self.gift_code_slug is not None:
            b.write(String(self.gift_code_slug))
        
        if self.stars_prize is not None:
            b.write(Long(self.stars_prize))
        
        b.write(Int(self.finish_date))
        
        b.write(Int(self.winners_count))
        
        if self.activated_count is not None:
            b.write(Int(self.activated_count))
        
        return b.getvalue()
