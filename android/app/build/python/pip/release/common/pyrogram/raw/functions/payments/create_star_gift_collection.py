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


class CreateStarGiftCollection(TLObject["raw.base.StarGiftCollection"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``1F4A0E87``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        title (``str``):
            N/A

        stargift (List of :obj:`InputSavedStarGift <pyrogram.raw.base.InputSavedStarGift>`):
            N/A

    Returns:
        :obj:`StarGiftCollection <pyrogram.raw.base.StarGiftCollection>`
    """

    __slots__: List[str] = ["peer", "title", "stargift"]

    ID = 0x1f4a0e87
    QUALNAME = "functions.payments.CreateStarGiftCollection"

    def __init__(self, *, peer: "raw.base.InputPeer", title: str, stargift: List["raw.base.InputSavedStarGift"]) -> None:
        self.peer = peer  # InputPeer
        self.title = title  # string
        self.stargift = stargift  # Vector<InputSavedStarGift>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CreateStarGiftCollection":
        # No flags
        
        peer = TLObject.read(b)
        
        title = String.read(b)
        
        stargift = TLObject.read(b)
        
        return CreateStarGiftCollection(peer=peer, title=title, stargift=stargift)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(String(self.title))
        
        b.write(Vector(self.stargift))
        
        return b.getvalue()
