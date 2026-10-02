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


class CommunityPeer(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.CommunityPeer`.

    Details:
        - Layer: ``228``
        - ID: ``76141EBD``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        can_view_history (``bool``, *optional*):
            N/A

        visible (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "can_view_history", "visible"]

    ID = 0x76141ebd
    QUALNAME = "types.CommunityPeer"

    def __init__(self, *, peer: "raw.base.Peer", can_view_history: Optional[bool] = None, visible: Optional[bool] = None) -> None:
        self.peer = peer  # Peer
        self.can_view_history = can_view_history  # flags.2?true
        self.visible = visible  # flags.0?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CommunityPeer":
        
        flags = Int.read(b)
        
        can_view_history = True if flags & (1 << 2) else False
        visible = Bool.read(b) if flags & (1 << 0) else None
        peer = TLObject.read(b)
        
        return CommunityPeer(peer=peer, can_view_history=can_view_history, visible=visible)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.can_view_history else 0
        flags |= (1 << 0) if self.visible is not None else 0
        b.write(Int(flags))
        
        if self.visible is not None:
            b.write(Bool(self.visible))
        
        b.write(self.peer.write())
        
        return b.getvalue()
