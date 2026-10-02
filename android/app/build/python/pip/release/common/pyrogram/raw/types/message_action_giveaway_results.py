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


class MessageActionGiveawayResults(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``87E2F155``

    Parameters:
        winners_count (``int`` ``32-bit``):
            N/A

        unclaimed_count (``int`` ``32-bit``):
            N/A

        stars (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["winners_count", "unclaimed_count", "stars"]

    ID = 0x87e2f155
    QUALNAME = "types.MessageActionGiveawayResults"

    def __init__(self, *, winners_count: int, unclaimed_count: int, stars: Optional[bool] = None) -> None:
        self.winners_count = winners_count  # int
        self.unclaimed_count = unclaimed_count  # int
        self.stars = stars  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionGiveawayResults":
        
        flags = Int.read(b)
        
        stars = True if flags & (1 << 0) else False
        winners_count = Int.read(b)
        
        unclaimed_count = Int.read(b)
        
        return MessageActionGiveawayResults(winners_count=winners_count, unclaimed_count=unclaimed_count, stars=stars)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.stars else 0
        b.write(Int(flags))
        
        b.write(Int(self.winners_count))
        
        b.write(Int(self.unclaimed_count))
        
        return b.getvalue()
