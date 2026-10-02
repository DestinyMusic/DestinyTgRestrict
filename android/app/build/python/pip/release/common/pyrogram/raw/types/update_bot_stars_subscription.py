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


class UpdateBotStarsSubscription(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``6C0D8E23``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        payload (``bytes``):
            N/A

        qts (``int`` ``32-bit``):
            N/A

        canceled (``bool``, *optional*):
            N/A

        payment_failed (``bool``, *optional*):
            N/A

        restored (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["user_id", "payload", "qts", "canceled", "payment_failed", "restored"]

    ID = 0x6c0d8e23
    QUALNAME = "types.UpdateBotStarsSubscription"

    def __init__(self, *, user_id: int, payload: bytes, qts: int, canceled: Optional[bool] = None, payment_failed: Optional[bool] = None, restored: Optional[bool] = None) -> None:
        self.user_id = user_id  # long
        self.payload = payload  # bytes
        self.qts = qts  # int
        self.canceled = canceled  # flags.0?true
        self.payment_failed = payment_failed  # flags.1?true
        self.restored = restored  # flags.2?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotStarsSubscription":
        
        flags = Int.read(b)
        
        canceled = True if flags & (1 << 0) else False
        payment_failed = True if flags & (1 << 1) else False
        restored = True if flags & (1 << 2) else False
        user_id = Long.read(b)
        
        payload = Bytes.read(b)
        
        qts = Int.read(b)
        
        return UpdateBotStarsSubscription(user_id=user_id, payload=payload, qts=qts, canceled=canceled, payment_failed=payment_failed, restored=restored)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.canceled else 0
        flags |= (1 << 1) if self.payment_failed else 0
        flags |= (1 << 2) if self.restored else 0
        b.write(Int(flags))
        
        b.write(Long(self.user_id))
        
        b.write(Bytes(self.payload))
        
        b.write(Int(self.qts))
        
        return b.getvalue()
