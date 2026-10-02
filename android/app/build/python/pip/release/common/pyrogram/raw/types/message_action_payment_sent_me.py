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


class MessageActionPaymentSentMe(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``FFA00CCC``

    Parameters:
        currency (``str``):
            N/A

        total_amount (``int`` ``64-bit``):
            N/A

        payload (``bytes``):
            N/A

        charge (:obj:`PaymentCharge <pyrogram.raw.base.PaymentCharge>`):
            N/A

        recurring_init (``bool``, *optional*):
            N/A

        recurring_used (``bool``, *optional*):
            N/A

        info (:obj:`PaymentRequestedInfo <pyrogram.raw.base.PaymentRequestedInfo>`, *optional*):
            N/A

        shipping_option_id (``str``, *optional*):
            N/A

        subscription_until_date (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["currency", "total_amount", "payload", "charge", "recurring_init", "recurring_used", "info", "shipping_option_id", "subscription_until_date"]

    ID = 0xffa00ccc
    QUALNAME = "types.MessageActionPaymentSentMe"

    def __init__(self, *, currency: str, total_amount: int, payload: bytes, charge: "raw.base.PaymentCharge", recurring_init: Optional[bool] = None, recurring_used: Optional[bool] = None, info: "raw.base.PaymentRequestedInfo" = None, shipping_option_id: Optional[str] = None, subscription_until_date: Optional[int] = None) -> None:
        self.currency = currency  # string
        self.total_amount = total_amount  # long
        self.payload = payload  # bytes
        self.charge = charge  # PaymentCharge
        self.recurring_init = recurring_init  # flags.2?true
        self.recurring_used = recurring_used  # flags.3?true
        self.info = info  # flags.0?PaymentRequestedInfo
        self.shipping_option_id = shipping_option_id  # flags.1?string
        self.subscription_until_date = subscription_until_date  # flags.4?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionPaymentSentMe":
        
        flags = Int.read(b)
        
        recurring_init = True if flags & (1 << 2) else False
        recurring_used = True if flags & (1 << 3) else False
        currency = String.read(b)
        
        total_amount = Long.read(b)
        
        payload = Bytes.read(b)
        
        info = TLObject.read(b) if flags & (1 << 0) else None
        
        shipping_option_id = String.read(b) if flags & (1 << 1) else None
        charge = TLObject.read(b)
        
        subscription_until_date = Int.read(b) if flags & (1 << 4) else None
        return MessageActionPaymentSentMe(currency=currency, total_amount=total_amount, payload=payload, charge=charge, recurring_init=recurring_init, recurring_used=recurring_used, info=info, shipping_option_id=shipping_option_id, subscription_until_date=subscription_until_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.recurring_init else 0
        flags |= (1 << 3) if self.recurring_used else 0
        flags |= (1 << 0) if self.info is not None else 0
        flags |= (1 << 1) if self.shipping_option_id is not None else 0
        flags |= (1 << 4) if self.subscription_until_date is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.currency))
        
        b.write(Long(self.total_amount))
        
        b.write(Bytes(self.payload))
        
        if self.info is not None:
            b.write(self.info.write())
        
        if self.shipping_option_id is not None:
            b.write(String(self.shipping_option_id))
        
        b.write(self.charge.write())
        
        if self.subscription_until_date is not None:
            b.write(Int(self.subscription_until_date))
        
        return b.getvalue()
