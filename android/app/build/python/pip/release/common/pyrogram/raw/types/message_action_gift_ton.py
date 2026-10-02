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


class MessageActionGiftTon(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``A8A3C699``

    Parameters:
        currency (``str``):
            N/A

        amount (``int`` ``64-bit``):
            N/A

        crypto_currency (``str``):
            N/A

        crypto_amount (``int`` ``64-bit``):
            N/A

        transaction_id (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["currency", "amount", "crypto_currency", "crypto_amount", "transaction_id"]

    ID = 0xa8a3c699
    QUALNAME = "types.MessageActionGiftTon"

    def __init__(self, *, currency: str, amount: int, crypto_currency: str, crypto_amount: int, transaction_id: Optional[str] = None) -> None:
        self.currency = currency  # string
        self.amount = amount  # long
        self.crypto_currency = crypto_currency  # string
        self.crypto_amount = crypto_amount  # long
        self.transaction_id = transaction_id  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionGiftTon":
        
        flags = Int.read(b)
        
        currency = String.read(b)
        
        amount = Long.read(b)
        
        crypto_currency = String.read(b)
        
        crypto_amount = Long.read(b)
        
        transaction_id = String.read(b) if flags & (1 << 0) else None
        return MessageActionGiftTon(currency=currency, amount=amount, crypto_currency=crypto_currency, crypto_amount=crypto_amount, transaction_id=transaction_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.transaction_id is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        b.write(String(self.crypto_currency))
        
        b.write(Long(self.crypto_amount))
        
        if self.transaction_id is not None:
            b.write(String(self.transaction_id))
        
        return b.getvalue()
