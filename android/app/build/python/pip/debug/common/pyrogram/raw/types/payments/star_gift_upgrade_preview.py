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


class StarGiftUpgradePreview(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.StarGiftUpgradePreview`.

    Details:
        - Layer: ``228``
        - ID: ``3DE1DFED``

    Parameters:
        sample_attributes (List of :obj:`StarGiftAttribute <pyrogram.raw.base.StarGiftAttribute>`):
            N/A

        prices (List of :obj:`StarGiftUpgradePrice <pyrogram.raw.base.StarGiftUpgradePrice>`):
            N/A

        next_prices (List of :obj:`StarGiftUpgradePrice <pyrogram.raw.base.StarGiftUpgradePrice>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetStarGiftUpgradePreview
    """

    __slots__: List[str] = ["sample_attributes", "prices", "next_prices"]

    ID = 0x3de1dfed
    QUALNAME = "types.payments.StarGiftUpgradePreview"

    def __init__(self, *, sample_attributes: List["raw.base.StarGiftAttribute"], prices: List["raw.base.StarGiftUpgradePrice"], next_prices: List["raw.base.StarGiftUpgradePrice"]) -> None:
        self.sample_attributes = sample_attributes  # Vector<StarGiftAttribute>
        self.prices = prices  # Vector<StarGiftUpgradePrice>
        self.next_prices = next_prices  # Vector<StarGiftUpgradePrice>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGiftUpgradePreview":
        # No flags
        
        sample_attributes = TLObject.read(b)
        
        prices = TLObject.read(b)
        
        next_prices = TLObject.read(b)
        
        return StarGiftUpgradePreview(sample_attributes=sample_attributes, prices=prices, next_prices=next_prices)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.sample_attributes))
        
        b.write(Vector(self.prices))
        
        b.write(Vector(self.next_prices))
        
        return b.getvalue()
