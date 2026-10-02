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


class UpdatePaidMessagesPrice(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``4B12327B``

    Parameters:
        channel (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            N/A

        send_paid_messages_stars (``int`` ``64-bit``):
            N/A

        broadcast_messages_allowed (``bool``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["channel", "send_paid_messages_stars", "broadcast_messages_allowed"]

    ID = 0x4b12327b
    QUALNAME = "functions.channels.UpdatePaidMessagesPrice"

    def __init__(self, *, channel: "raw.base.InputChannel", send_paid_messages_stars: int, broadcast_messages_allowed: Optional[bool] = None) -> None:
        self.channel = channel  # InputChannel
        self.send_paid_messages_stars = send_paid_messages_stars  # long
        self.broadcast_messages_allowed = broadcast_messages_allowed  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdatePaidMessagesPrice":
        
        flags = Int.read(b)
        
        broadcast_messages_allowed = True if flags & (1 << 0) else False
        channel = TLObject.read(b)
        
        send_paid_messages_stars = Long.read(b)
        
        return UpdatePaidMessagesPrice(channel=channel, send_paid_messages_stars=send_paid_messages_stars, broadcast_messages_allowed=broadcast_messages_allowed)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.broadcast_messages_allowed else 0
        b.write(Int(flags))
        
        b.write(self.channel.write())
        
        b.write(Long(self.send_paid_messages_stars))
        
        return b.getvalue()
