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


class GetStarsTransactions(TLObject["raw.base.payments.StarsStatus"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``69DA4557``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        offset (``str``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

        inbound (``bool``, *optional*):
            N/A

        outbound (``bool``, *optional*):
            N/A

        ascending (``bool``, *optional*):
            N/A

        ton (``bool``, *optional*):
            N/A

        subscription_id (``str``, *optional*):
            N/A

    Returns:
        :obj:`payments.StarsStatus <pyrogram.raw.base.payments.StarsStatus>`
    """

    __slots__: List[str] = ["peer", "offset", "limit", "inbound", "outbound", "ascending", "ton", "subscription_id"]

    ID = 0x69da4557
    QUALNAME = "functions.payments.GetStarsTransactions"

    def __init__(self, *, peer: "raw.base.InputPeer", offset: str, limit: int, inbound: Optional[bool] = None, outbound: Optional[bool] = None, ascending: Optional[bool] = None, ton: Optional[bool] = None, subscription_id: Optional[str] = None) -> None:
        self.peer = peer  # InputPeer
        self.offset = offset  # string
        self.limit = limit  # int
        self.inbound = inbound  # flags.0?true
        self.outbound = outbound  # flags.1?true
        self.ascending = ascending  # flags.2?true
        self.ton = ton  # flags.4?true
        self.subscription_id = subscription_id  # flags.3?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStarsTransactions":
        
        flags = Int.read(b)
        
        inbound = True if flags & (1 << 0) else False
        outbound = True if flags & (1 << 1) else False
        ascending = True if flags & (1 << 2) else False
        ton = True if flags & (1 << 4) else False
        subscription_id = String.read(b) if flags & (1 << 3) else None
        peer = TLObject.read(b)
        
        offset = String.read(b)
        
        limit = Int.read(b)
        
        return GetStarsTransactions(peer=peer, offset=offset, limit=limit, inbound=inbound, outbound=outbound, ascending=ascending, ton=ton, subscription_id=subscription_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.inbound else 0
        flags |= (1 << 1) if self.outbound else 0
        flags |= (1 << 2) if self.ascending else 0
        flags |= (1 << 4) if self.ton else 0
        flags |= (1 << 3) if self.subscription_id is not None else 0
        b.write(Int(flags))
        
        if self.subscription_id is not None:
            b.write(String(self.subscription_id))
        
        b.write(self.peer.write())
        
        b.write(String(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
