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


class StarGiftAttributeOriginalDetails(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarGiftAttribute`.

    Details:
        - Layer: ``228``
        - ID: ``E0BFF26C``

    Parameters:
        recipient_id (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        date (``int`` ``32-bit``):
            N/A

        sender_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        message (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["recipient_id", "date", "sender_id", "message"]

    ID = 0xe0bff26c
    QUALNAME = "types.StarGiftAttributeOriginalDetails"

    def __init__(self, *, recipient_id: "raw.base.Peer", date: int, sender_id: "raw.base.Peer" = None, message: "raw.base.TextWithEntities" = None) -> None:
        self.recipient_id = recipient_id  # Peer
        self.date = date  # int
        self.sender_id = sender_id  # flags.0?Peer
        self.message = message  # flags.1?TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarGiftAttributeOriginalDetails":
        
        flags = Int.read(b)
        
        sender_id = TLObject.read(b) if flags & (1 << 0) else None
        
        recipient_id = TLObject.read(b)
        
        date = Int.read(b)
        
        message = TLObject.read(b) if flags & (1 << 1) else None
        
        return StarGiftAttributeOriginalDetails(recipient_id=recipient_id, date=date, sender_id=sender_id, message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.sender_id is not None else 0
        flags |= (1 << 1) if self.message is not None else 0
        b.write(Int(flags))
        
        if self.sender_id is not None:
            b.write(self.sender_id.write())
        
        b.write(self.recipient_id.write())
        
        b.write(Int(self.date))
        
        if self.message is not None:
            b.write(self.message.write())
        
        return b.getvalue()
