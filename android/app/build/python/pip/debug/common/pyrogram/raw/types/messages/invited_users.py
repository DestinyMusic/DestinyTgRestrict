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


class InvitedUsers(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.messages.InvitedUsers`.

    Details:
        - Layer: ``228``
        - ID: ``7F5DEFA6``

    Parameters:
        updates (:obj:`Updates <pyrogram.raw.base.Updates>`):
            N/A

        missing_invitees (List of :obj:`MissingInvitee <pyrogram.raw.base.MissingInvitee>`):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.AddChatUser
            messages.CreateChat
            channels.InviteToChannel
    """

    __slots__: List[str] = ["updates", "missing_invitees"]

    ID = 0x7f5defa6
    QUALNAME = "types.messages.InvitedUsers"

    def __init__(self, *, updates: "raw.base.Updates", missing_invitees: List["raw.base.MissingInvitee"]) -> None:
        self.updates = updates  # Updates
        self.missing_invitees = missing_invitees  # Vector<MissingInvitee>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InvitedUsers":
        # No flags
        
        updates = TLObject.read(b)
        
        missing_invitees = TLObject.read(b)
        
        return InvitedUsers(updates=updates, missing_invitees=missing_invitees)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.updates.write())
        
        b.write(Vector(self.missing_invitees))
        
        return b.getvalue()
