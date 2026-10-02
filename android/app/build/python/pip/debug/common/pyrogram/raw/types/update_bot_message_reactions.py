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


class UpdateBotMessageReactions(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``9CB7759``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        reactions (List of :obj:`ReactionCount <pyrogram.raw.base.ReactionCount>`):
            N/A

        qts (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["peer", "msg_id", "date", "reactions", "qts"]

    ID = 0x9cb7759
    QUALNAME = "types.UpdateBotMessageReactions"

    def __init__(self, *, peer: "raw.base.Peer", msg_id: int, date: int, reactions: List["raw.base.ReactionCount"], qts: int) -> None:
        self.peer = peer  # Peer
        self.msg_id = msg_id  # int
        self.date = date  # int
        self.reactions = reactions  # Vector<ReactionCount>
        self.qts = qts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotMessageReactions":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        date = Int.read(b)
        
        reactions = TLObject.read(b)
        
        qts = Int.read(b)
        
        return UpdateBotMessageReactions(peer=peer, msg_id=msg_id, date=date, reactions=reactions, qts=qts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Int(self.date))
        
        b.write(Vector(self.reactions))
        
        b.write(Int(self.qts))
        
        return b.getvalue()
