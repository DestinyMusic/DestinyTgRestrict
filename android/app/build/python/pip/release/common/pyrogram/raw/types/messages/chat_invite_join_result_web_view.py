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


class ChatInviteJoinResultWebView(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.messages.ChatInviteJoinResult`.

    Details:
        - Layer: ``228``
        - ID: ``61CA29D3``

    Parameters:
        bot_id (``int`` ``64-bit``):
            N/A

        query_id (``int`` ``64-bit``):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.ImportChatInvite
            channels.JoinChannel
    """

    __slots__: List[str] = ["bot_id", "query_id", "users"]

    ID = 0x61ca29d3
    QUALNAME = "types.messages.ChatInviteJoinResultWebView"

    def __init__(self, *, bot_id: int, query_id: int, users: List["raw.base.User"]) -> None:
        self.bot_id = bot_id  # long
        self.query_id = query_id  # long
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInviteJoinResultWebView":
        # No flags
        
        bot_id = Long.read(b)
        
        query_id = Long.read(b)
        
        users = TLObject.read(b)
        
        return ChatInviteJoinResultWebView(bot_id=bot_id, query_id=query_id, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.bot_id))
        
        b.write(Long(self.query_id))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
