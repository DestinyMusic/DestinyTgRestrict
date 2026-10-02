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


class UpdateEphemeralBotCallbackQuery(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``9B380762``

    Parameters:
        query_id (``int`` ``64-bit``):
            N/A

        user_id (``int`` ``64-bit``):
            N/A

        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        data (``bytes``):
            N/A

        message (:obj:`EphemeralMessage <pyrogram.raw.base.EphemeralMessage>`):
            N/A

    """

    __slots__: List[str] = ["query_id", "user_id", "peer", "msg_id", "data", "message"]

    ID = 0x9b380762
    QUALNAME = "types.UpdateEphemeralBotCallbackQuery"

    def __init__(self, *, query_id: int, user_id: int, peer: "raw.base.Peer", msg_id: int, data: bytes, message: "raw.base.EphemeralMessage") -> None:
        self.query_id = query_id  # long
        self.user_id = user_id  # long
        self.peer = peer  # Peer
        self.msg_id = msg_id  # int
        self.data = data  # bytes
        self.message = message  # EphemeralMessage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateEphemeralBotCallbackQuery":
        # No flags
        
        query_id = Long.read(b)
        
        user_id = Long.read(b)
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        data = Bytes.read(b)
        
        message = TLObject.read(b)
        
        return UpdateEphemeralBotCallbackQuery(query_id=query_id, user_id=user_id, peer=peer, msg_id=msg_id, data=data, message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.query_id))
        
        b.write(Long(self.user_id))
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Bytes(self.data))
        
        b.write(self.message.write())
        
        return b.getvalue()
