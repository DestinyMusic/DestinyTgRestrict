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


class StarsRating(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarsRating`.

    Details:
        - Layer: ``228``
        - ID: ``1B0E4F07``

    Parameters:
        level (``int`` ``32-bit``):
            N/A

        current_level_stars (``int`` ``64-bit``):
            N/A

        stars (``int`` ``64-bit``):
            N/A

        next_level_stars (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["level", "current_level_stars", "stars", "next_level_stars"]

    ID = 0x1b0e4f07
    QUALNAME = "types.StarsRating"

    def __init__(self, *, level: int, current_level_stars: int, stars: int, next_level_stars: Optional[int] = None) -> None:
        self.level = level  # int
        self.current_level_stars = current_level_stars  # long
        self.stars = stars  # long
        self.next_level_stars = next_level_stars  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsRating":
        
        flags = Int.read(b)
        
        level = Int.read(b)
        
        current_level_stars = Long.read(b)
        
        stars = Long.read(b)
        
        next_level_stars = Long.read(b) if flags & (1 << 0) else None
        return StarsRating(level=level, current_level_stars=current_level_stars, stars=stars, next_level_stars=next_level_stars)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.next_level_stars is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.level))
        
        b.write(Long(self.current_level_stars))
        
        b.write(Long(self.stars))
        
        if self.next_level_stars is not None:
            b.write(Long(self.next_level_stars))
        
        return b.getvalue()
