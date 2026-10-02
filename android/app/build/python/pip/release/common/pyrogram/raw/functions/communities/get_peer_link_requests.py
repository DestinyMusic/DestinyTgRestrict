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


class GetPeerLinkRequests(TLObject["raw.base.communities.PeerLinkRequests"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``93773344``

    Parameters:
        community (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            N/A

        offset (``str``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`communities.PeerLinkRequests <pyrogram.raw.base.communities.PeerLinkRequests>`
    """

    __slots__: List[str] = ["community", "offset", "limit"]

    ID = 0x93773344
    QUALNAME = "functions.communities.GetPeerLinkRequests"

    def __init__(self, *, community: "raw.base.InputChannel", offset: str, limit: int) -> None:
        self.community = community  # InputChannel
        self.offset = offset  # string
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetPeerLinkRequests":
        # No flags
        
        community = TLObject.read(b)
        
        offset = String.read(b)
        
        limit = Int.read(b)
        
        return GetPeerLinkRequests(community=community, offset=offset, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.community.write())
        
        b.write(String(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
