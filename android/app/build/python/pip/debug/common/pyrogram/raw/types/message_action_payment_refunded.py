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


class MessageActionPaymentRefunded(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``41B3E202``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        currency (``str``):
            N/A

        total_amount (``int`` ``64-bit``):
            N/A

        charge (:obj:`PaymentCharge <pyrogram.raw.base.PaymentCharge>`):
            N/A

        payload (``bytes``, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "currency", "total_amount", "charge", "payload"]

    ID = 0x41b3e202
    QUALNAME = "types.MessageActionPaymentRefunded"

    def __init__(self, *, peer: "raw.base.Peer", currency: str, total_amount: int, charge: "raw.base.PaymentCharge", payload: Optional[bytes] = None) -> None:
        self.peer = peer  # Peer
        self.currency = currency  # string
        self.total_amount = total_amount  # long
        self.charge = charge  # PaymentCharge
        self.payload = payload  # flags.0?bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionPaymentRefunded":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        currency = String.read(b)
        
        total_amount = Long.read(b)
        
        payload = Bytes.read(b) if flags & (1 << 0) else None
        charge = TLObject.read(b)
        
        return MessageActionPaymentRefunded(peer=peer, currency=currency, total_amount=total_amount, charge=charge, payload=payload)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.payload is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(String(self.currency))
        
        b.write(Long(self.total_amount))
        
        if self.payload is not None:
            b.write(Bytes(self.payload))
        
        b.write(self.charge.write())
        
        return b.getvalue()
