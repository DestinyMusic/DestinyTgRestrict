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


class StarGiftAuctionUserState(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarGiftAuctionUserState`.

    Details:
        - Layer: ``228``
        - ID: ``2EEED1C4``

    Parameters:
        acquired_count (``int`` ``32-bit``):
            N/A

        returned (``bool``, *optional*):
            N/A

        bid_amount (``int`` ``64-bit``, *optional*):
            N/A

        bid_date (``int`` ``32-bit``, *optional*):
            N/A

        min_bid_amount (``int`` ``64-bit``, *optional*):
            N/A

        bid_peer (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["acquired_count", "returned", "bid_amount", "bid_date", "min_bid_amount", "bid_peer"]

    ID = 0x2eeed1c4
    QUALNAME = "types.StarGiftAuctionUserState"

    def __init__(self, *, acquired_count: int, returned: Optional[bool] = None, bid_amount: Optional[int] = None, bid_date: Optional[int] = None, min_bid_amount: Optional[int] = None, bid_peer: "raw.base.Peer" = None) -> None:
        self.acquired_count = acquired_count  # int
        self.returned = returned  # flags.1?true
        self.bid_amount = bid_amount  # flags.0?long
        self.bid_date = bid_date  # flags.0?int
        self.min_bid_amount = min_bid_amount  # flags.0?long
        self.bid_peer = bid_peer  # flags.0?Peer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGiftAuctionUserState":
        
        flags = Int.read(b)
        
        returned = True if flags & (1 << 1) else False
        bid_amount = Long.read(b) if flags & (1 << 0) else None
        bid_date = Int.read(b) if flags & (1 << 0) else None
        min_bid_amount = Long.read(b) if flags & (1 << 0) else None
        bid_peer = TLObject.read(b) if flags & (1 << 0) else None
        
        acquired_count = Int.read(b)
        
        return StarGiftAuctionUserState(acquired_count=acquired_count, returned=returned, bid_amount=bid_amount, bid_date=bid_date, min_bid_amount=min_bid_amount, bid_peer=bid_peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.returned else 0
        flags |= (1 << 0) if self.bid_amount is not None else 0
        flags |= (1 << 0) if self.bid_date is not None else 0
        flags |= (1 << 0) if self.min_bid_amount is not None else 0
        flags |= (1 << 0) if self.bid_peer is not None else 0
        b.write(Int(flags))
        
        if self.bid_amount is not None:
            b.write(Long(self.bid_amount))
        
        if self.bid_date is not None:
            b.write(Int(self.bid_date))
        
        if self.min_bid_amount is not None:
            b.write(Long(self.min_bid_amount))
        
        if self.bid_peer is not None:
            b.write(self.bid_peer.write())
        
        b.write(Int(self.acquired_count))
        
        return b.getvalue()
