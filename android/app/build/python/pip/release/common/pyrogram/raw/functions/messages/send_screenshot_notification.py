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


class SendScreenshotNotification(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``A1405817``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        reply_to (:obj:`InputReplyTo <pyrogram.raw.base.InputReplyTo>`):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "reply_to", "random_id"]

    ID = 0xa1405817
    QUALNAME = "functions.messages.SendScreenshotNotification"

    def __init__(self, *, peer: "raw.base.InputPeer", reply_to: "raw.base.InputReplyTo", random_id: int) -> None:
        self.peer = peer  # InputPeer
        self.reply_to = reply_to  # InputReplyTo
        self.random_id = random_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendScreenshotNotification":
        # No flags
        
        peer = TLObject.read(b)
        
        reply_to = TLObject.read(b)
        
        random_id = Long.read(b)
        
        return SendScreenshotNotification(peer=peer, reply_to=reply_to, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.reply_to.write())
        
        b.write(Long(self.random_id))
        
        return b.getvalue()
