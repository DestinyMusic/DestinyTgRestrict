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


class GroupCallDonor(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.GroupCallDonor`.

    Details:
        - Layer: ``228``
        - ID: ``EE430C85``

    Parameters:
        stars (``int`` ``64-bit``):
            N/A

        top (``bool``, *optional*):
            N/A

        my (``bool``, *optional*):
            N/A

        peer_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["stars", "top", "my", "peer_id"]

    ID = 0xee430c85
    QUALNAME = "types.GroupCallDonor"

    def __init__(self, *, stars: int, top: Optional[bool] = None, my: Optional[bool] = None, peer_id: "raw.base.Peer" = None) -> None:
        self.stars = stars  # long
        self.top = top  # flags.0?true
        self.my = my  # flags.1?true
        self.peer_id = peer_id  # flags.3?Peer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GroupCallDonor":
        
        flags = Int.read(b)
        
        top = True if flags & (1 << 0) else False
        my = True if flags & (1 << 1) else False
        peer_id = TLObject.read(b) if flags & (1 << 3) else None
        
        stars = Long.read(b)
        
        return GroupCallDonor(stars=stars, top=top, my=my, peer_id=peer_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.top else 0
        flags |= (1 << 1) if self.my else 0
        flags |= (1 << 3) if self.peer_id is not None else 0
        b.write(Int(flags))
        
        if self.peer_id is not None:
            b.write(self.peer_id.write())
        
        b.write(Long(self.stars))
        
        return b.getvalue()
