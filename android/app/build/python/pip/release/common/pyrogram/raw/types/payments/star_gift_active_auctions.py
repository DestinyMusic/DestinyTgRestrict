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


class StarGiftActiveAuctions(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.StarGiftActiveAuctions`.

    Details:
        - Layer: ``228``
        - ID: ``AEF6ABBC``

    Parameters:
        auctions (List of :obj:`StarGiftActiveAuctionState <pyrogram.raw.base.StarGiftActiveAuctionState>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetStarGiftActiveAuctions
    """

    __slots__: List[str] = ["auctions", "users", "chats"]

    ID = 0xaef6abbc
    QUALNAME = "types.payments.StarGiftActiveAuctions"

    def __init__(self, *, auctions: List["raw.base.StarGiftActiveAuctionState"], users: List["raw.base.User"], chats: List["raw.base.Chat"]) -> None:
        self.auctions = auctions  # Vector<StarGiftActiveAuctionState>
        self.users = users  # Vector<User>
        self.chats = chats  # Vector<Chat>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGiftActiveAuctions":
        # No flags
        
        auctions = TLObject.read(b)
        
        users = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        return StarGiftActiveAuctions(auctions=auctions, users=users, chats=chats)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.auctions))
        
        b.write(Vector(self.users))
        
        b.write(Vector(self.chats))
        
        return b.getvalue()
