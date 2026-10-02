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


class MessageActionRequestedPeerSentMe(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``93B31848``

    Parameters:
        button_id (``int`` ``32-bit``):
            N/A

        peers (List of :obj:`RequestedPeer <pyrogram.raw.base.RequestedPeer>`):
            N/A

    """

    __slots__: List[str] = ["button_id", "peers"]

    ID = 0x93b31848
    QUALNAME = "types.MessageActionRequestedPeerSentMe"

    def __init__(self, *, button_id: int, peers: List["raw.base.RequestedPeer"]) -> None:
        self.button_id = button_id  # int
        self.peers = peers  # Vector<RequestedPeer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionRequestedPeerSentMe":
        # No flags
        
        button_id = Int.read(b)
        
        peers = TLObject.read(b)
        
        return MessageActionRequestedPeerSentMe(button_id=button_id, peers=peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.button_id))
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
