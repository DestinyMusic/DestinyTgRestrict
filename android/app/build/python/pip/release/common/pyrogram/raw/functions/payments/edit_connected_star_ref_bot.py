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


class EditConnectedStarRefBot(TLObject["raw.base.payments.ConnectedStarRefBots"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``E4FCA4A3``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        link (``str``):
            N/A

        revoked (``bool``, *optional*):
            N/A

    Returns:
        :obj:`payments.ConnectedStarRefBots <pyrogram.raw.base.payments.ConnectedStarRefBots>`
    """

    __slots__: List[str] = ["peer", "link", "revoked"]

    ID = 0xe4fca4a3
    QUALNAME = "functions.payments.EditConnectedStarRefBot"

    def __init__(self, *, peer: "raw.base.InputPeer", link: str, revoked: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.link = link  # string
        self.revoked = revoked  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditConnectedStarRefBot":
        
        flags = Int.read(b)
        
        revoked = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        link = String.read(b)
        
        return EditConnectedStarRefBot(peer=peer, link=link, revoked=revoked)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.revoked else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(String(self.link))
        
        return b.getvalue()
