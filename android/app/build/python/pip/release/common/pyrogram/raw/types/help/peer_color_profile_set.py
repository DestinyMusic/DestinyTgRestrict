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


class PeerColorProfileSet(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.help.PeerColorSet`.

    Details:
        - Layer: ``228``
        - ID: ``767D61EB``

    Parameters:
        palette_colors (List of ``int`` ``32-bit``):
            N/A

        bg_colors (List of ``int`` ``32-bit``):
            N/A

        story_colors (List of ``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["palette_colors", "bg_colors", "story_colors"]

    ID = 0x767d61eb
    QUALNAME = "types.help.PeerColorProfileSet"

    def __init__(self, *, palette_colors: List[int], bg_colors: List[int], story_colors: List[int]) -> None:
        self.palette_colors = palette_colors  # Vector<int>
        self.bg_colors = bg_colors  # Vector<int>
        self.story_colors = story_colors  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerColorProfileSet":
        # No flags
        
        palette_colors = TLObject.read(b, Int)
        
        bg_colors = TLObject.read(b, Int)
        
        story_colors = TLObject.read(b, Int)
        
        return PeerColorProfileSet(palette_colors=palette_colors, bg_colors=bg_colors, story_colors=story_colors)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.palette_colors, Int))
        
        b.write(Vector(self.bg_colors, Int))
        
        b.write(Vector(self.story_colors, Int))
        
        return b.getvalue()
