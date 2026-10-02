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


class GetStarGiftWithdrawalUrl(TLObject["raw.base.payments.StarGiftWithdrawalUrl"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``D06E93A8``

    Parameters:
        stargift (:obj:`InputSavedStarGift <pyrogram.raw.base.InputSavedStarGift>`):
            N/A

        password (:obj:`InputCheckPasswordSRP <pyrogram.raw.base.InputCheckPasswordSRP>`):
            N/A

    Returns:
        :obj:`payments.StarGiftWithdrawalUrl <pyrogram.raw.base.payments.StarGiftWithdrawalUrl>`
    """

    __slots__: List[str] = ["stargift", "password"]

    ID = 0xd06e93a8
    QUALNAME = "functions.payments.GetStarGiftWithdrawalUrl"

    def __init__(self, *, stargift: "raw.base.InputSavedStarGift", password: "raw.base.InputCheckPasswordSRP") -> None:
        self.stargift = stargift  # InputSavedStarGift
        self.password = password  # InputCheckPasswordSRP

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStarGiftWithdrawalUrl":
        # No flags
        
        stargift = TLObject.read(b)
        
        password = TLObject.read(b)
        
        return GetStarGiftWithdrawalUrl(stargift=stargift, password=password)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stargift.write())
        
        b.write(self.password.write())
        
        return b.getvalue()
