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


class ReportMessage(TLObject["raw.base.ReportResult"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``8704F2BF``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        id (``int`` ``32-bit``):
            N/A

        option (``bytes``):
            N/A

        message (``str``):
            N/A

    Returns:
        :obj:`ReportResult <pyrogram.raw.base.ReportResult>`
    """

    __slots__: List[str] = ["peer", "id", "option", "message"]

    ID = 0x8704f2bf
    QUALNAME = "functions.ephemeral.ReportMessage"

    def __init__(self, *, peer: "raw.base.InputPeer", id: int, option: bytes, message: str) -> None:
        self.peer = peer  # InputPeer
        self.id = id  # int
        self.option = option  # bytes
        self.message = message  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReportMessage":
        # No flags
        
        peer = TLObject.read(b)
        
        id = Int.read(b)
        
        option = Bytes.read(b)
        
        message = String.read(b)
        
        return ReportMessage(peer=peer, id=id, option=option, message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.id))
        
        b.write(Bytes(self.option))
        
        b.write(String(self.message))
        
        return b.getvalue()
