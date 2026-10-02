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


class MediaAreaWeather(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MediaArea`.

    Details:
        - Layer: ``228``
        - ID: ``49A6549C``

    Parameters:
        coordinates (:obj:`MediaAreaCoordinates <pyrogram.raw.base.MediaAreaCoordinates>`):
            N/A

        emoji (``str``):
            N/A

        temperature_c (``float`` ``64-bit``):
            N/A

        color (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["coordinates", "emoji", "temperature_c", "color"]

    ID = 0x49a6549c
    QUALNAME = "types.MediaAreaWeather"

    def __init__(self, *, coordinates: "raw.base.MediaAreaCoordinates", emoji: str, temperature_c: float, color: int) -> None:
        self.coordinates = coordinates  # MediaAreaCoordinates
        self.emoji = emoji  # string
        self.temperature_c = temperature_c  # double
        self.color = color  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MediaAreaWeather":
        # No flags
        
        coordinates = TLObject.read(b)
        
        emoji = String.read(b)
        
        temperature_c = Double.read(b)
        
        color = Int.read(b)
        
        return MediaAreaWeather(coordinates=coordinates, emoji=emoji, temperature_c=temperature_c, color=color)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.coordinates.write())
        
        b.write(String(self.emoji))
        
        b.write(Double(self.temperature_c))
        
        b.write(Int(self.color))
        
        return b.getvalue()
