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


class DisallowedGiftsSettings(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.DisallowedGiftsSettings`.

    Details:
        - Layer: ``228``
        - ID: ``71F276C4``

    Parameters:
        disallow_unlimited_stargifts (``bool``, *optional*):
            N/A

        disallow_limited_stargifts (``bool``, *optional*):
            N/A

        disallow_unique_stargifts (``bool``, *optional*):
            N/A

        disallow_premium_gifts (``bool``, *optional*):
            N/A

        disallow_stargifts_from_channels (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["disallow_unlimited_stargifts", "disallow_limited_stargifts", "disallow_unique_stargifts", "disallow_premium_gifts", "disallow_stargifts_from_channels"]

    ID = 0x71f276c4
    QUALNAME = "types.DisallowedGiftsSettings"

    def __init__(self, *, disallow_unlimited_stargifts: Optional[bool] = None, disallow_limited_stargifts: Optional[bool] = None, disallow_unique_stargifts: Optional[bool] = None, disallow_premium_gifts: Optional[bool] = None, disallow_stargifts_from_channels: Optional[bool] = None) -> None:
        self.disallow_unlimited_stargifts = disallow_unlimited_stargifts  # flags.0?true
        self.disallow_limited_stargifts = disallow_limited_stargifts  # flags.1?true
        self.disallow_unique_stargifts = disallow_unique_stargifts  # flags.2?true
        self.disallow_premium_gifts = disallow_premium_gifts  # flags.3?true
        self.disallow_stargifts_from_channels = disallow_stargifts_from_channels  # flags.4?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DisallowedGiftsSettings":
        
        flags = Int.read(b)
        
        disallow_unlimited_stargifts = True if flags & (1 << 0) else False
        disallow_limited_stargifts = True if flags & (1 << 1) else False
        disallow_unique_stargifts = True if flags & (1 << 2) else False
        disallow_premium_gifts = True if flags & (1 << 3) else False
        disallow_stargifts_from_channels = True if flags & (1 << 4) else False
        return DisallowedGiftsSettings(disallow_unlimited_stargifts=disallow_unlimited_stargifts, disallow_limited_stargifts=disallow_limited_stargifts, disallow_unique_stargifts=disallow_unique_stargifts, disallow_premium_gifts=disallow_premium_gifts, disallow_stargifts_from_channels=disallow_stargifts_from_channels)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.disallow_unlimited_stargifts else 0
        flags |= (1 << 1) if self.disallow_limited_stargifts else 0
        flags |= (1 << 2) if self.disallow_unique_stargifts else 0
        flags |= (1 << 3) if self.disallow_premium_gifts else 0
        flags |= (1 << 4) if self.disallow_stargifts_from_channels else 0
        b.write(Int(flags))
        
        return b.getvalue()
