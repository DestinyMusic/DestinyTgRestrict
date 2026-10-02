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


class GetConnectedStarRefBots(TLObject["raw.base.payments.ConnectedStarRefBots"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``5869A553``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        limit (``int`` ``32-bit``):
            N/A

        offset_date (``int`` ``32-bit``, *optional*):
            N/A

        offset_link (``str``, *optional*):
            N/A

    Returns:
        :obj:`payments.ConnectedStarRefBots <pyrogram.raw.base.payments.ConnectedStarRefBots>`
    """

    __slots__: List[str] = ["peer", "limit", "offset_date", "offset_link"]

    ID = 0x5869a553
    QUALNAME = "functions.payments.GetConnectedStarRefBots"

    def __init__(self, *, peer: "raw.base.InputPeer", limit: int, offset_date: Optional[int] = None, offset_link: Optional[str] = None) -> None:
        self.peer = peer  # InputPeer
        self.limit = limit  # int
        self.offset_date = offset_date  # flags.2?int
        self.offset_link = offset_link  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetConnectedStarRefBots":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        offset_date = Int.read(b) if flags & (1 << 2) else None
        offset_link = String.read(b) if flags & (1 << 2) else None
        limit = Int.read(b)
        
        return GetConnectedStarRefBots(peer=peer, limit=limit, offset_date=offset_date, offset_link=offset_link)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.offset_date is not None else 0
        flags |= (1 << 2) if self.offset_link is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        if self.offset_date is not None:
            b.write(Int(self.offset_date))
        
        if self.offset_link is not None:
            b.write(String(self.offset_link))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
