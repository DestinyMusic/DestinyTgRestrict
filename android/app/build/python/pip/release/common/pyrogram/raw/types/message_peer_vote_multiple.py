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


class MessagePeerVoteMultiple(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessagePeerVote`.

    Details:
        - Layer: ``228``
        - ID: ``4628F6E6``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        options (List of ``bytes``):
            N/A

        date (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["peer", "options", "date"]

    ID = 0x4628f6e6
    QUALNAME = "types.MessagePeerVoteMultiple"

    def __init__(self, *, peer: "raw.base.Peer", options: List[bytes], date: int) -> None:
        self.peer = peer  # Peer
        self.options = options  # Vector<bytes>
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessagePeerVoteMultiple":
        # No flags
        
        peer = TLObject.read(b)
        
        options = TLObject.read(b, Bytes)
        
        date = Int.read(b)
        
        return MessagePeerVoteMultiple(peer=peer, options=options, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.options, Bytes))
        
        b.write(Int(self.date))
        
        return b.getvalue()
