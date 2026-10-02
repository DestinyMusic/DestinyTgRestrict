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


class SetChatAvailableReactions(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``864B2581``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        available_reactions (:obj:`ChatReactions <pyrogram.raw.base.ChatReactions>`):
            N/A

        reactions_limit (``int`` ``32-bit``, *optional*):
            N/A

        paid_enabled (``bool``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "available_reactions", "reactions_limit", "paid_enabled"]

    ID = 0x864b2581
    QUALNAME = "functions.messages.SetChatAvailableReactions"

    def __init__(self, *, peer: "raw.base.InputPeer", available_reactions: "raw.base.ChatReactions", reactions_limit: Optional[int] = None, paid_enabled: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.available_reactions = available_reactions  # ChatReactions
        self.reactions_limit = reactions_limit  # flags.0?int
        self.paid_enabled = paid_enabled  # flags.1?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetChatAvailableReactions":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        available_reactions = TLObject.read(b)
        
        reactions_limit = Int.read(b) if flags & (1 << 0) else None
        paid_enabled = Bool.read(b) if flags & (1 << 1) else None
        return SetChatAvailableReactions(peer=peer, available_reactions=available_reactions, reactions_limit=reactions_limit, paid_enabled=paid_enabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.reactions_limit is not None else 0
        flags |= (1 << 1) if self.paid_enabled is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(self.available_reactions.write())
        
        if self.reactions_limit is not None:
            b.write(Int(self.reactions_limit))
        
        if self.paid_enabled is not None:
            b.write(Bool(self.paid_enabled))
        
        return b.getvalue()
