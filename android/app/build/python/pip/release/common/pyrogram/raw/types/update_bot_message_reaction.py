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


class UpdateBotMessageReaction(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``AC21D3CE``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        actor (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        old_reactions (List of :obj:`Reaction <pyrogram.raw.base.Reaction>`):
            N/A

        new_reactions (List of :obj:`Reaction <pyrogram.raw.base.Reaction>`):
            N/A

        qts (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["peer", "msg_id", "date", "actor", "old_reactions", "new_reactions", "qts"]

    ID = 0xac21d3ce
    QUALNAME = "types.UpdateBotMessageReaction"

    def __init__(self, *, peer: "raw.base.Peer", msg_id: int, date: int, actor: "raw.base.Peer", old_reactions: List["raw.base.Reaction"], new_reactions: List["raw.base.Reaction"], qts: int) -> None:
        self.peer = peer  # Peer
        self.msg_id = msg_id  # int
        self.date = date  # int
        self.actor = actor  # Peer
        self.old_reactions = old_reactions  # Vector<Reaction>
        self.new_reactions = new_reactions  # Vector<Reaction>
        self.qts = qts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotMessageReaction":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        date = Int.read(b)
        
        actor = TLObject.read(b)
        
        old_reactions = TLObject.read(b)
        
        new_reactions = TLObject.read(b)
        
        qts = Int.read(b)
        
        return UpdateBotMessageReaction(peer=peer, msg_id=msg_id, date=date, actor=actor, old_reactions=old_reactions, new_reactions=new_reactions, qts=qts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Int(self.date))
        
        b.write(self.actor.write())
        
        b.write(Vector(self.old_reactions))
        
        b.write(Vector(self.new_reactions))
        
        b.write(Int(self.qts))
        
        return b.getvalue()
