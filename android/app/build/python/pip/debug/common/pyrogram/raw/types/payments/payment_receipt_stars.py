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


class PaymentReceiptStars(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.PaymentReceipt`.

    Details:
        - Layer: ``228``
        - ID: ``DABBF83A``

    Parameters:
        date (``int`` ``32-bit``):
            N/A

        bot_id (``int`` ``64-bit``):
            N/A

        title (``str``):
            N/A

        description (``str``):
            N/A

        invoice (:obj:`Invoice <pyrogram.raw.base.Invoice>`):
            N/A

        currency (``str``):
            N/A

        total_amount (``int`` ``64-bit``):
            N/A

        transaction_id (``str``):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        photo (:obj:`WebDocument <pyrogram.raw.base.WebDocument>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetPaymentReceipt
    """

    __slots__: List[str] = ["date", "bot_id", "title", "description", "invoice", "currency", "total_amount", "transaction_id", "users", "photo"]

    ID = 0xdabbf83a
    QUALNAME = "types.payments.PaymentReceiptStars"

    def __init__(self, *, date: int, bot_id: int, title: str, description: str, invoice: "raw.base.Invoice", currency: str, total_amount: int, transaction_id: str, users: List["raw.base.User"], photo: "raw.base.WebDocument" = None) -> None:
        self.date = date  # int
        self.bot_id = bot_id  # long
        self.title = title  # string
        self.description = description  # string
        self.invoice = invoice  # Invoice
        self.currency = currency  # string
        self.total_amount = total_amount  # long
        self.transaction_id = transaction_id  # string
        self.users = users  # Vector<User>
        self.photo = photo  # flags.2?WebDocument

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PaymentReceiptStars":
        
        flags = Int.read(b)
        
        date = Int.read(b)
        
        bot_id = Long.read(b)
        
        title = String.read(b)
        
        description = String.read(b)
        
        photo = TLObject.read(b) if flags & (1 << 2) else None
        
        invoice = TLObject.read(b)
        
        currency = String.read(b)
        
        total_amount = Long.read(b)
        
        transaction_id = String.read(b)
        
        users = TLObject.read(b)
        
        return PaymentReceiptStars(date=date, bot_id=bot_id, title=title, description=description, invoice=invoice, currency=currency, total_amount=total_amount, transaction_id=transaction_id, users=users, photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.photo is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.date))
        
        b.write(Long(self.bot_id))
        
        b.write(String(self.title))
        
        b.write(String(self.description))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        b.write(self.invoice.write())
        
        b.write(String(self.currency))
        
        b.write(Long(self.total_amount))
        
        b.write(String(self.transaction_id))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
