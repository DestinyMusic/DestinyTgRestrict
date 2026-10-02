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


class InputStorePaymentAuthCode(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputStorePaymentPurpose`.

    Details:
        - Layer: ``228``
        - ID: ``3FC18057``

    Parameters:
        phone_number (``str``):
            N/A

        phone_code_hash (``str``):
            N/A

        premium_days (``int`` ``32-bit``):
            N/A

        currency (``str``):
            N/A

        amount (``int`` ``64-bit``):
            N/A

        restore (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["phone_number", "phone_code_hash", "premium_days", "currency", "amount", "restore"]

    ID = 0x3fc18057
    QUALNAME = "types.InputStorePaymentAuthCode"

    def __init__(self, *, phone_number: str, phone_code_hash: str, premium_days: int, currency: str, amount: int, restore: Optional[bool] = None) -> None:
        self.phone_number = phone_number  # string
        self.phone_code_hash = phone_code_hash  # string
        self.premium_days = premium_days  # int
        self.currency = currency  # string
        self.amount = amount  # long
        self.restore = restore  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputStorePaymentAuthCode":
        
        flags = Int.read(b)
        
        restore = True if flags & (1 << 0) else False
        phone_number = String.read(b)
        
        phone_code_hash = String.read(b)
        
        premium_days = Int.read(b)
        
        currency = String.read(b)
        
        amount = Long.read(b)
        
        return InputStorePaymentAuthCode(phone_number=phone_number, phone_code_hash=phone_code_hash, premium_days=premium_days, currency=currency, amount=amount, restore=restore)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.restore else 0
        b.write(Int(flags))
        
        b.write(String(self.phone_number))
        
        b.write(String(self.phone_code_hash))
        
        b.write(Int(self.premium_days))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        return b.getvalue()
