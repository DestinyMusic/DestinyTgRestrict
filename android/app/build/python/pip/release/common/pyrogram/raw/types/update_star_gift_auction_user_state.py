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


class UpdateStarGiftAuctionUserState(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``DC58F31E``

    Parameters:
        gift_id (``int`` ``64-bit``):
            N/A

        user_state (:obj:`StarGiftAuctionUserState <pyrogram.raw.base.StarGiftAuctionUserState>`):
            N/A

    """

    __slots__: List[str] = ["gift_id", "user_state"]

    ID = 0xdc58f31e
    QUALNAME = "types.UpdateStarGiftAuctionUserState"

    def __init__(self, *, gift_id: int, user_state: "raw.base.StarGiftAuctionUserState") -> None:
        self.gift_id = gift_id  # long
        self.user_state = user_state  # StarGiftAuctionUserState

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateStarGiftAuctionUserState":
        # No flags
        
        gift_id = Long.read(b)
        
        user_state = TLObject.read(b)
        
        return UpdateStarGiftAuctionUserState(gift_id=gift_id, user_state=user_state)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.gift_id))
        
        b.write(self.user_state.write())
        
        return b.getvalue()
