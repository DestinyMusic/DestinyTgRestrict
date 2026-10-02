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


class MarkDialogUnread(TLObject["raw.base.Bool"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``8C5006F8``

    Parameters:
        peer (:obj:`InputDialogPeer <pyrogram.raw.base.InputDialogPeer>`):
            N/A

        unread (``bool``, *optional*):
            N/A

        parent_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "unread", "parent_peer"]

    ID = 0x8c5006f8
    QUALNAME = "functions.messages.MarkDialogUnread"

    def __init__(self, *, peer: "raw.base.InputDialogPeer", unread: Optional[bool] = None, parent_peer: "raw.base.InputPeer" = None) -> None:
        self.peer = peer  # InputDialogPeer
        self.unread = unread  # flags.0?true
        self.parent_peer = parent_peer  # flags.1?InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MarkDialogUnread":
        
        flags = Int.read(b)
        
        unread = True if flags & (1 << 0) else False
        parent_peer = TLObject.read(b) if flags & (1 << 1) else None
        
        peer = TLObject.read(b)
        
        return MarkDialogUnread(peer=peer, unread=unread, parent_peer=parent_peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.unread else 0
        flags |= (1 << 1) if self.parent_peer is not None else 0
        b.write(Int(flags))
        
        if self.parent_peer is not None:
            b.write(self.parent_peer.write())
        
        b.write(self.peer.write())
        
        return b.getvalue()
