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


class GetMessagePublicForwards(TLObject["raw.base.stats.PublicForwards"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``5F150144``

    Parameters:
        channel (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        offset (``str``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`stats.PublicForwards <pyrogram.raw.base.stats.PublicForwards>`
    """

    __slots__: List[str] = ["channel", "msg_id", "offset", "limit"]

    ID = 0x5f150144
    QUALNAME = "functions.stats.GetMessagePublicForwards"

    def __init__(self, *, channel: "raw.base.InputChannel", msg_id: int, offset: str, limit: int) -> None:
        self.channel = channel  # InputChannel
        self.msg_id = msg_id  # int
        self.offset = offset  # string
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetMessagePublicForwards":
        # No flags
        
        channel = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        offset = String.read(b)
        
        limit = Int.read(b)
        
        return GetMessagePublicForwards(channel=channel, msg_id=msg_id, offset=offset, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Int(self.msg_id))
        
        b.write(String(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
