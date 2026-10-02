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


class ResolvedBusinessChatLinks(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.account.ResolvedBusinessChatLinks`.

    Details:
        - Layer: ``228``
        - ID: ``9A23AF21``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        message (``str``):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.ResolveBusinessChatLink
    """

    __slots__: List[str] = ["peer", "message", "chats", "users", "entities"]

    ID = 0x9a23af21
    QUALNAME = "types.account.ResolvedBusinessChatLinks"

    def __init__(self, *, peer: "raw.base.Peer", message: str, chats: List["raw.base.Chat"], users: List["raw.base.User"], entities: Optional[List["raw.base.MessageEntity"]] = None) -> None:
        self.peer = peer  # Peer
        self.message = message  # string
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.entities = entities  # flags.0?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ResolvedBusinessChatLinks":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        message = String.read(b)
        
        entities = TLObject.read(b) if flags & (1 << 0) else []
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ResolvedBusinessChatLinks(peer=peer, message=message, chats=chats, users=users, entities=entities)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.entities else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(String(self.message))
        
        if self.entities:
            b.write(Vector(self.entities))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
