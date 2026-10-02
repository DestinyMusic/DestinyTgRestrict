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


class BoostsStatus(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.premium.BoostsStatus`.

    Details:
        - Layer: ``228``
        - ID: ``4959427A``

    Parameters:
        level (``int`` ``32-bit``):
            N/A

        current_level_boosts (``int`` ``32-bit``):
            N/A

        boosts (``int`` ``32-bit``):
            N/A

        boost_url (``str``):
            N/A

        my_boost (``bool``, *optional*):
            N/A

        gift_boosts (``int`` ``32-bit``, *optional*):
            N/A

        next_level_boosts (``int`` ``32-bit``, *optional*):
            N/A

        premium_audience (:obj:`StatsPercentValue <pyrogram.raw.base.StatsPercentValue>`, *optional*):
            N/A

        prepaid_giveaways (List of :obj:`PrepaidGiveaway <pyrogram.raw.base.PrepaidGiveaway>`, *optional*):
            N/A

        my_boost_slots (List of ``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            premium.GetBoostsStatus
    """

    __slots__: List[str] = ["level", "current_level_boosts", "boosts", "boost_url", "my_boost", "gift_boosts", "next_level_boosts", "premium_audience", "prepaid_giveaways", "my_boost_slots"]

    ID = 0x4959427a
    QUALNAME = "types.premium.BoostsStatus"

    def __init__(self, *, level: int, current_level_boosts: int, boosts: int, boost_url: str, my_boost: Optional[bool] = None, gift_boosts: Optional[int] = None, next_level_boosts: Optional[int] = None, premium_audience: "raw.base.StatsPercentValue" = None, prepaid_giveaways: Optional[List["raw.base.PrepaidGiveaway"]] = None, my_boost_slots: Optional[List[int]] = None) -> None:
        self.level = level  # int
        self.current_level_boosts = current_level_boosts  # int
        self.boosts = boosts  # int
        self.boost_url = boost_url  # string
        self.my_boost = my_boost  # flags.2?true
        self.gift_boosts = gift_boosts  # flags.4?int
        self.next_level_boosts = next_level_boosts  # flags.0?int
        self.premium_audience = premium_audience  # flags.1?StatsPercentValue
        self.prepaid_giveaways = prepaid_giveaways  # flags.3?Vector<PrepaidGiveaway>
        self.my_boost_slots = my_boost_slots  # flags.2?Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BoostsStatus":
        
        flags = Int.read(b)
        
        my_boost = True if flags & (1 << 2) else False
        level = Int.read(b)
        
        current_level_boosts = Int.read(b)
        
        boosts = Int.read(b)
        
        gift_boosts = Int.read(b) if flags & (1 << 4) else None
        next_level_boosts = Int.read(b) if flags & (1 << 0) else None
        premium_audience = TLObject.read(b) if flags & (1 << 1) else None
        
        boost_url = String.read(b)
        
        prepaid_giveaways = TLObject.read(b) if flags & (1 << 3) else []
        
        my_boost_slots = TLObject.read(b, Int) if flags & (1 << 2) else []
        
        return BoostsStatus(level=level, current_level_boosts=current_level_boosts, boosts=boosts, boost_url=boost_url, my_boost=my_boost, gift_boosts=gift_boosts, next_level_boosts=next_level_boosts, premium_audience=premium_audience, prepaid_giveaways=prepaid_giveaways, my_boost_slots=my_boost_slots)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.my_boost else 0
        flags |= (1 << 4) if self.gift_boosts is not None else 0
        flags |= (1 << 0) if self.next_level_boosts is not None else 0
        flags |= (1 << 1) if self.premium_audience is not None else 0
        flags |= (1 << 3) if self.prepaid_giveaways else 0
        flags |= (1 << 2) if self.my_boost_slots else 0
        b.write(Int(flags))
        
        b.write(Int(self.level))
        
        b.write(Int(self.current_level_boosts))
        
        b.write(Int(self.boosts))
        
        if self.gift_boosts is not None:
            b.write(Int(self.gift_boosts))
        
        if self.next_level_boosts is not None:
            b.write(Int(self.next_level_boosts))
        
        if self.premium_audience is not None:
            b.write(self.premium_audience.write())
        
        b.write(String(self.boost_url))
        
        if self.prepaid_giveaways:
            b.write(Vector(self.prepaid_giveaways))
        
        if self.my_boost_slots:
            b.write(Vector(self.my_boost_slots, Int))
        
        return b.getvalue()
