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


class InputInvoiceStarGiftPrepaidUpgrade(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputInvoice`.

    Details:
        - Layer: ``228``
        - ID: ``9A0B48B8``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        hash (``str``):
            N/A

    """

    __slots__: List[str] = ["peer", "hash"]

    ID = 0x9a0b48b8
    QUALNAME = "types.InputInvoiceStarGiftPrepaidUpgrade"

    def __init__(self, *, peer: "raw.base.InputPeer", hash: str) -> None:
        self.peer = peer  # InputPeer
        self.hash = hash  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputInvoiceStarGiftPrepaidUpgrade":
        # No flags
        
        peer = TLObject.read(b)
        
        hash = String.read(b)
        
        return InputInvoiceStarGiftPrepaidUpgrade(peer=peer, hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(String(self.hash))
        
        return b.getvalue()
