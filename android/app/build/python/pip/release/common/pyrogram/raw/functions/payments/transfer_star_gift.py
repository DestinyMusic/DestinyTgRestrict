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


class TransferStarGift(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``7F18176A``

    Parameters:
        stargift (:obj:`InputSavedStarGift <pyrogram.raw.base.InputSavedStarGift>`):
            N/A

        to_id (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["stargift", "to_id"]

    ID = 0x7f18176a
    QUALNAME = "functions.payments.TransferStarGift"

    def __init__(self, *, stargift: "raw.base.InputSavedStarGift", to_id: "raw.base.InputPeer") -> None:
        self.stargift = stargift  # InputSavedStarGift
        self.to_id = to_id  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TransferStarGift":
        # No flags
        
        stargift = TLObject.read(b)
        
        to_id = TLObject.read(b)
        
        return TransferStarGift(stargift=stargift, to_id=to_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stargift.write())
        
        b.write(self.to_id.write())
        
        return b.getvalue()
