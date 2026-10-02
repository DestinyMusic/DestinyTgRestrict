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


class CommunityPeerRequest(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.CommunityPeerRequest`.

    Details:
        - Layer: ``228``
        - ID: ``7BEAFA85``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        requested_by (``int`` ``64-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        visible (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "requested_by", "date", "visible"]

    ID = 0x7beafa85
    QUALNAME = "types.CommunityPeerRequest"

    def __init__(self, *, peer: "raw.base.Peer", requested_by: int, date: int, visible: Optional[bool] = None) -> None:
        self.peer = peer  # Peer
        self.requested_by = requested_by  # long
        self.date = date  # int
        self.visible = visible  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CommunityPeerRequest":
        
        flags = Int.read(b)
        
        visible = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        requested_by = Long.read(b)
        
        date = Int.read(b)
        
        return CommunityPeerRequest(peer=peer, requested_by=requested_by, date=date, visible=visible)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.visible else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Long(self.requested_by))
        
        b.write(Int(self.date))
        
        return b.getvalue()
