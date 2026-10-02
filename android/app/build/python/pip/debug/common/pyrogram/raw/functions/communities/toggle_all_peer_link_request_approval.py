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


class ToggleAllPeerLinkRequestApproval(TLObject["raw.base.Bool"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``BFE3DD3D``

    Parameters:
        community (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            N/A

        reject (``bool``, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["community", "reject"]

    ID = 0xbfe3dd3d
    QUALNAME = "functions.communities.ToggleAllPeerLinkRequestApproval"

    def __init__(self, *, community: "raw.base.InputChannel", reject: Optional[bool] = None) -> None:
        self.community = community  # InputChannel
        self.reject = reject  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ToggleAllPeerLinkRequestApproval":
        
        flags = Int.read(b)
        
        reject = True if flags & (1 << 0) else False
        community = TLObject.read(b)
        
        return ToggleAllPeerLinkRequestApproval(community=community, reject=reject)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.reject else 0
        b.write(Int(flags))
        
        b.write(self.community.write())
        
        return b.getvalue()
