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


class UpdateNewAuthorization(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``8951ABEF``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        unconfirmed (``bool``, *optional*):
            N/A

        date (``int`` ``32-bit``, *optional*):
            N/A

        device (``str``, *optional*):
            N/A

        location (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["hash", "unconfirmed", "date", "device", "location"]

    ID = 0x8951abef
    QUALNAME = "types.UpdateNewAuthorization"

    def __init__(self, *, hash: int, unconfirmed: Optional[bool] = None, date: Optional[int] = None, device: Optional[str] = None, location: Optional[str] = None) -> None:
        self.hash = hash  # long
        self.unconfirmed = unconfirmed  # flags.0?true
        self.date = date  # flags.0?int
        self.device = device  # flags.0?string
        self.location = location  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateNewAuthorization":
        
        flags = Int.read(b)
        
        unconfirmed = True if flags & (1 << 0) else False
        hash = Long.read(b)
        
        date = Int.read(b) if flags & (1 << 0) else None
        device = String.read(b) if flags & (1 << 0) else None
        location = String.read(b) if flags & (1 << 0) else None
        return UpdateNewAuthorization(hash=hash, unconfirmed=unconfirmed, date=date, device=device, location=location)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.unconfirmed else 0
        flags |= (1 << 0) if self.date is not None else 0
        flags |= (1 << 0) if self.device is not None else 0
        flags |= (1 << 0) if self.location is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.hash))
        
        if self.date is not None:
            b.write(Int(self.date))
        
        if self.device is not None:
            b.write(String(self.device))
        
        if self.location is not None:
            b.write(String(self.location))
        
        return b.getvalue()
