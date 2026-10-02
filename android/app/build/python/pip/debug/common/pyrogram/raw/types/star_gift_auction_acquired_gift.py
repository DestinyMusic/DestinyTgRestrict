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


class StarGiftAuctionAcquiredGift(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarGiftAuctionAcquiredGift`.

    Details:
        - Layer: ``228``
        - ID: ``42B00348``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        date (``int`` ``32-bit``):
            N/A

        bid_amount (``int`` ``64-bit``):
            N/A

        round (``int`` ``32-bit``):
            N/A

        pos (``int`` ``32-bit``):
            N/A

        name_hidden (``bool``, *optional*):
            N/A

        message (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`, *optional*):
            N/A

        gift_num (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "date", "bid_amount", "round", "pos", "name_hidden", "message", "gift_num"]

    ID = 0x42b00348
    QUALNAME = "types.StarGiftAuctionAcquiredGift"

    def __init__(self, *, peer: "raw.base.Peer", date: int, bid_amount: int, round: int, pos: int, name_hidden: Optional[bool] = None, message: "raw.base.TextWithEntities" = None, gift_num: Optional[int] = None) -> None:
        self.peer = peer  # Peer
        self.date = date  # int
        self.bid_amount = bid_amount  # long
        self.round = round  # int
        self.pos = pos  # int
        self.name_hidden = name_hidden  # flags.0?true
        self.message = message  # flags.1?TextWithEntities
        self.gift_num = gift_num  # flags.2?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGiftAuctionAcquiredGift":
        
        flags = Int.read(b)
        
        name_hidden = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        date = Int.read(b)
        
        bid_amount = Long.read(b)
        
        round = Int.read(b)
        
        pos = Int.read(b)
        
        message = TLObject.read(b) if flags & (1 << 1) else None
        
        gift_num = Int.read(b) if flags & (1 << 2) else None
        return StarGiftAuctionAcquiredGift(peer=peer, date=date, bid_amount=bid_amount, round=round, pos=pos, name_hidden=name_hidden, message=message, gift_num=gift_num)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.name_hidden else 0
        flags |= (1 << 1) if self.message is not None else 0
        flags |= (1 << 2) if self.gift_num is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.date))
        
        b.write(Long(self.bid_amount))
        
        b.write(Int(self.round))
        
        b.write(Int(self.pos))
        
        if self.message is not None:
            b.write(self.message.write())
        
        if self.gift_num is not None:
            b.write(Int(self.gift_num))
        
        return b.getvalue()
