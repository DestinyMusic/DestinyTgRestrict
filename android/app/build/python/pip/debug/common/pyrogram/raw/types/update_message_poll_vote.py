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


class UpdateMessagePollVote(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``7699F014``

    Parameters:
        poll_id (``int`` ``64-bit``):
            N/A

        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        options (List of ``bytes``):
            N/A

        positions (List of ``int`` ``32-bit``):
            N/A

        qts (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["poll_id", "peer", "options", "positions", "qts"]

    ID = 0x7699f014
    QUALNAME = "types.UpdateMessagePollVote"

    def __init__(self, *, poll_id: int, peer: "raw.base.Peer", options: List[bytes], positions: List[int], qts: int) -> None:
        self.poll_id = poll_id  # long
        self.peer = peer  # Peer
        self.options = options  # Vector<bytes>
        self.positions = positions  # Vector<int>
        self.qts = qts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateMessagePollVote":
        # No flags
        
        poll_id = Long.read(b)
        
        peer = TLObject.read(b)
        
        options = TLObject.read(b, Bytes)
        
        positions = TLObject.read(b, Int)
        
        qts = Int.read(b)
        
        return UpdateMessagePollVote(poll_id=poll_id, peer=peer, options=options, positions=positions, qts=qts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.poll_id))
        
        b.write(self.peer.write())
        
        b.write(Vector(self.options, Bytes))
        
        b.write(Vector(self.positions, Int))
        
        b.write(Int(self.qts))
        
        return b.getvalue()
