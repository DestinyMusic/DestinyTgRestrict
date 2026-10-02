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


class MessageActionPrizeStars(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``B00C47A2``

    Parameters:
        stars (``int`` ``64-bit``):
            N/A

        transaction_id (``str``):
            N/A

        boost_peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        giveaway_msg_id (``int`` ``32-bit``):
            N/A

        unclaimed (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["stars", "transaction_id", "boost_peer", "giveaway_msg_id", "unclaimed"]

    ID = 0xb00c47a2
    QUALNAME = "types.MessageActionPrizeStars"

    def __init__(self, *, stars: int, transaction_id: str, boost_peer: "raw.base.Peer", giveaway_msg_id: int, unclaimed: Optional[bool] = None) -> None:
        self.stars = stars  # long
        self.transaction_id = transaction_id  # string
        self.boost_peer = boost_peer  # Peer
        self.giveaway_msg_id = giveaway_msg_id  # int
        self.unclaimed = unclaimed  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionPrizeStars":
        
        flags = Int.read(b)
        
        unclaimed = True if flags & (1 << 0) else False
        stars = Long.read(b)
        
        transaction_id = String.read(b)
        
        boost_peer = TLObject.read(b)
        
        giveaway_msg_id = Int.read(b)
        
        return MessageActionPrizeStars(stars=stars, transaction_id=transaction_id, boost_peer=boost_peer, giveaway_msg_id=giveaway_msg_id, unclaimed=unclaimed)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.unclaimed else 0
        b.write(Int(flags))
        
        b.write(Long(self.stars))
        
        b.write(String(self.transaction_id))
        
        b.write(self.boost_peer.write())
        
        b.write(Int(self.giveaway_msg_id))
        
        return b.getvalue()
