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


class ChannelAdminLogEventActionParticipantEditRank(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.ChannelAdminLogEventAction`.

    Details:
        - Layer: ``228``
        - ID: ``5806B4EC``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        prev_rank (``str``):
            N/A

        new_rank (``str``):
            N/A

    """

    __slots__: List[str] = ["user_id", "prev_rank", "new_rank"]

    ID = 0x5806b4ec
    QUALNAME = "types.ChannelAdminLogEventActionParticipantEditRank"

    def __init__(self, *, user_id: int, prev_rank: str, new_rank: str) -> None:
        self.user_id = user_id  # long
        self.prev_rank = prev_rank  # string
        self.new_rank = new_rank  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionParticipantEditRank":
        # No flags
        
        user_id = Long.read(b)
        
        prev_rank = String.read(b)
        
        new_rank = String.read(b)
        
        return ChannelAdminLogEventActionParticipantEditRank(user_id=user_id, prev_rank=prev_rank, new_rank=new_rank)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(String(self.prev_rank))
        
        b.write(String(self.new_rank))
        
        return b.getvalue()
