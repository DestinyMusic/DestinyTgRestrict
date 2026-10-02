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


class GetPaidMessagesRevenue(TLObject["raw.base.account.PaidMessagesRevenue"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``19BA4A67``

    Parameters:
        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        parent_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            N/A

    Returns:
        :obj:`account.PaidMessagesRevenue <pyrogram.raw.base.account.PaidMessagesRevenue>`
    """

    __slots__: List[str] = ["user_id", "parent_peer"]

    ID = 0x19ba4a67
    QUALNAME = "functions.account.GetPaidMessagesRevenue"

    def __init__(self, *, user_id: "raw.base.InputUser", parent_peer: "raw.base.InputPeer" = None) -> None:
        self.user_id = user_id  # InputUser
        self.parent_peer = parent_peer  # flags.0?InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetPaidMessagesRevenue":
        
        flags = Int.read(b)
        
        parent_peer = TLObject.read(b) if flags & (1 << 0) else None
        
        user_id = TLObject.read(b)
        
        return GetPaidMessagesRevenue(user_id=user_id, parent_peer=parent_peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.parent_peer is not None else 0
        b.write(Int(flags))
        
        if self.parent_peer is not None:
            b.write(self.parent_peer.write())
        
        b.write(self.user_id.write())
        
        return b.getvalue()
