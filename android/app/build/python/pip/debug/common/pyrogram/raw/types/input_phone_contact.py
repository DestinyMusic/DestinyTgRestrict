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


class InputPhoneContact(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputContact`.

    Details:
        - Layer: ``228``
        - ID: ``6A1DC4BE``

    Parameters:
        client_id (``int`` ``64-bit``):
            N/A

        phone (``str``):
            N/A

        first_name (``str``):
            N/A

        last_name (``str``):
            N/A

        note (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["client_id", "phone", "first_name", "last_name", "note"]

    ID = 0x6a1dc4be
    QUALNAME = "types.InputPhoneContact"

    def __init__(self, *, client_id: int, phone: str, first_name: str, last_name: str, note: "raw.base.TextWithEntities" = None) -> None:
        self.client_id = client_id  # long
        self.phone = phone  # string
        self.first_name = first_name  # string
        self.last_name = last_name  # string
        self.note = note  # flags.0?TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPhoneContact":
        
        flags = Int.read(b)
        
        client_id = Long.read(b)
        
        phone = String.read(b)
        
        first_name = String.read(b)
        
        last_name = String.read(b)
        
        note = TLObject.read(b) if flags & (1 << 0) else None
        
        return InputPhoneContact(client_id=client_id, phone=phone, first_name=first_name, last_name=last_name, note=note)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.note is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.client_id))
        
        b.write(String(self.phone))
        
        b.write(String(self.first_name))
        
        b.write(String(self.last_name))
        
        if self.note is not None:
            b.write(self.note.write())
        
        return b.getvalue()
