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


class MediaAreaGeoPoint(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MediaArea`.

    Details:
        - Layer: ``228``
        - ID: ``CAD5452D``

    Parameters:
        coordinates (:obj:`MediaAreaCoordinates <pyrogram.raw.base.MediaAreaCoordinates>`):
            N/A

        geo (:obj:`GeoPoint <pyrogram.raw.base.GeoPoint>`):
            N/A

        address (:obj:`GeoPointAddress <pyrogram.raw.base.GeoPointAddress>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["coordinates", "geo", "address"]

    ID = 0xcad5452d
    QUALNAME = "types.MediaAreaGeoPoint"

    def __init__(self, *, coordinates: "raw.base.MediaAreaCoordinates", geo: "raw.base.GeoPoint", address: "raw.base.GeoPointAddress" = None) -> None:
        self.coordinates = coordinates  # MediaAreaCoordinates
        self.geo = geo  # GeoPoint
        self.address = address  # flags.0?GeoPointAddress

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MediaAreaGeoPoint":
        
        flags = Int.read(b)
        
        coordinates = TLObject.read(b)
        
        geo = TLObject.read(b)
        
        address = TLObject.read(b) if flags & (1 << 0) else None
        
        return MediaAreaGeoPoint(coordinates=coordinates, geo=geo, address=address)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.address is not None else 0
        b.write(Int(flags))
        
        b.write(self.coordinates.write())
        
        b.write(self.geo.write())
        
        if self.address is not None:
            b.write(self.address.write())
        
        return b.getvalue()
