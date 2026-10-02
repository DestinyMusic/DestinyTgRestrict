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


class GetSendAs(TLObject["raw.base.channels.SendAsPeers"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``E785A43F``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        for_paid_reactions (``bool``, *optional*):
            N/A

        for_live_stories (``bool``, *optional*):
            N/A

    Returns:
        :obj:`channels.SendAsPeers <pyrogram.raw.base.channels.SendAsPeers>`
    """

    __slots__: List[str] = ["peer", "for_paid_reactions", "for_live_stories"]

    ID = 0xe785a43f
    QUALNAME = "functions.channels.GetSendAs"

    def __init__(self, *, peer: "raw.base.InputPeer", for_paid_reactions: Optional[bool] = None, for_live_stories: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.for_paid_reactions = for_paid_reactions  # flags.0?true
        self.for_live_stories = for_live_stories  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetSendAs":
        
        flags = Int.read(b)
        
        for_paid_reactions = True if flags & (1 << 0) else False
        for_live_stories = True if flags & (1 << 1) else False
        peer = TLObject.read(b)
        
        return GetSendAs(peer=peer, for_paid_reactions=for_paid_reactions, for_live_stories=for_live_stories)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.for_paid_reactions else 0
        flags |= (1 << 1) if self.for_live_stories else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        return b.getvalue()
