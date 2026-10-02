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


class ChangeStarsSubscription(TLObject["raw.base.Bool"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``C7770878``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        subscription_id (``str``):
            N/A

        canceled (``bool``, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "subscription_id", "canceled"]

    ID = 0xc7770878
    QUALNAME = "functions.payments.ChangeStarsSubscription"

    def __init__(self, *, peer: "raw.base.InputPeer", subscription_id: str, canceled: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.subscription_id = subscription_id  # string
        self.canceled = canceled  # flags.0?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChangeStarsSubscription":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        subscription_id = String.read(b)
        
        canceled = Bool.read(b) if flags & (1 << 0) else None
        return ChangeStarsSubscription(peer=peer, subscription_id=subscription_id, canceled=canceled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.canceled is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(String(self.subscription_id))
        
        if self.canceled is not None:
            b.write(Bool(self.canceled))
        
        return b.getvalue()
