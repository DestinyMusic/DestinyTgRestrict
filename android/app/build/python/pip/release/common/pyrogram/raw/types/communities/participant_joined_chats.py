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


class ParticipantJoinedChats(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.communities.ParticipantJoinedChats`.

    Details:
        - Layer: ``228``
        - ID: ``8D78512A``

    Parameters:
        creator_chat_ids (List of ``int`` ``64-bit``):
            N/A

        joined_chat_ids (List of ``int`` ``64-bit``):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            communities.GetParticipantJoinedChats
    """

    __slots__: List[str] = ["creator_chat_ids", "joined_chat_ids", "chats", "users"]

    ID = 0x8d78512a
    QUALNAME = "types.communities.ParticipantJoinedChats"

    def __init__(self, *, creator_chat_ids: List[int], joined_chat_ids: List[int], chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.creator_chat_ids = creator_chat_ids  # Vector<long>
        self.joined_chat_ids = joined_chat_ids  # Vector<long>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ParticipantJoinedChats":
        # No flags
        
        creator_chat_ids = TLObject.read(b, Long)
        
        joined_chat_ids = TLObject.read(b, Long)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ParticipantJoinedChats(creator_chat_ids=creator_chat_ids, joined_chat_ids=joined_chat_ids, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.creator_chat_ids, Long))
        
        b.write(Vector(self.joined_chat_ids, Long))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
