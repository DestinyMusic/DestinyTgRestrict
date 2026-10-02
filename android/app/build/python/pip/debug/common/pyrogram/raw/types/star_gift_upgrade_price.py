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


class StarGiftUpgradePrice(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarGiftUpgradePrice`.

    Details:
        - Layer: ``228``
        - ID: ``99EA331D``

    Parameters:
        date (``int`` ``32-bit``):
            N/A

        upgrade_stars (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["date", "upgrade_stars"]

    ID = 0x99ea331d
    QUALNAME = "types.StarGiftUpgradePrice"

    def __init__(self, *, date: int, upgrade_stars: int) -> None:
        self.date = date  # int
        self.upgrade_stars = upgrade_stars  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGiftUpgradePrice":
        # No flags
        
        date = Int.read(b)
        
        upgrade_stars = Long.read(b)
        
        return StarGiftUpgradePrice(date=date, upgrade_stars=upgrade_stars)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        b.write(Long(self.upgrade_stars))
        
        return b.getvalue()
