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


class BusinessLocation(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.BusinessLocation`.

    Details:
        - Layer: ``228``
        - ID: ``AC5C1AF7``

    Parameters:
        address (``str``):
            N/A

        geo_point (:obj:`GeoPoint <pyrogram.raw.base.GeoPoint>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["address", "geo_point"]

    ID = 0xac5c1af7
    QUALNAME = "types.BusinessLocation"

    def __init__(self, *, address: str, geo_point: "raw.base.GeoPoint" = None) -> None:
        self.address = address  # string
        self.geo_point = geo_point  # flags.0?GeoPoint

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BusinessLocation":
        
        flags = Int.read(b)
        
        geo_point = TLObject.read(b) if flags & (1 << 0) else None
        
        address = String.read(b)
        
        return BusinessLocation(address=address, geo_point=geo_point)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.geo_point is not None else 0
        b.write(Int(flags))
        
        if self.geo_point is not None:
            b.write(self.geo_point.write())
        
        b.write(String(self.address))
        
        return b.getvalue()
