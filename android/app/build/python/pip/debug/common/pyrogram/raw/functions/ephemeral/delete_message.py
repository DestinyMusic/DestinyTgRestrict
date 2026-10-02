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


class DeleteMessage(TLObject["raw.base.Bool"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``A3C0D511``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        receiver_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        id (``int`` ``32-bit``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "receiver_id", "id"]

    ID = 0xa3c0d511
    QUALNAME = "functions.ephemeral.DeleteMessage"

    def __init__(self, *, peer: "raw.base.InputPeer", receiver_id: "raw.base.InputUser", id: int) -> None:
        self.peer = peer  # InputPeer
        self.receiver_id = receiver_id  # InputUser
        self.id = id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteMessage":
        # No flags
        
        peer = TLObject.read(b)
        
        receiver_id = TLObject.read(b)
        
        id = Int.read(b)
        
        return DeleteMessage(peer=peer, receiver_id=receiver_id, id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.receiver_id.write())
        
        b.write(Int(self.id))
        
        return b.getvalue()
