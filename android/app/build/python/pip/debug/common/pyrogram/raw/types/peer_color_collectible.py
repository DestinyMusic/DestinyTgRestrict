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


class PeerColorCollectible(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PeerColor`.

    Details:
        - Layer: ``228``
        - ID: ``B9C0639A``

    Parameters:
        collectible_id (``int`` ``64-bit``):
            N/A

        gift_emoji_id (``int`` ``64-bit``):
            N/A

        background_emoji_id (``int`` ``64-bit``):
            N/A

        accent_color (``int`` ``32-bit``):
            N/A

        colors (List of ``int`` ``32-bit``):
            N/A

        dark_accent_color (``int`` ``32-bit``, *optional*):
            N/A

        dark_colors (List of ``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["collectible_id", "gift_emoji_id", "background_emoji_id", "accent_color", "colors", "dark_accent_color", "dark_colors"]

    ID = 0xb9c0639a
    QUALNAME = "types.PeerColorCollectible"

    def __init__(self, *, collectible_id: int, gift_emoji_id: int, background_emoji_id: int, accent_color: int, colors: List[int], dark_accent_color: Optional[int] = None, dark_colors: Optional[List[int]] = None) -> None:
        self.collectible_id = collectible_id  # long
        self.gift_emoji_id = gift_emoji_id  # long
        self.background_emoji_id = background_emoji_id  # long
        self.accent_color = accent_color  # int
        self.colors = colors  # Vector<int>
        self.dark_accent_color = dark_accent_color  # flags.0?int
        self.dark_colors = dark_colors  # flags.1?Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerColorCollectible":
        
        flags = Int.read(b)
        
        collectible_id = Long.read(b)
        
        gift_emoji_id = Long.read(b)
        
        background_emoji_id = Long.read(b)
        
        accent_color = Int.read(b)
        
        colors = TLObject.read(b, Int)
        
        dark_accent_color = Int.read(b) if flags & (1 << 0) else None
        dark_colors = TLObject.read(b, Int) if flags & (1 << 1) else []
        
        return PeerColorCollectible(collectible_id=collectible_id, gift_emoji_id=gift_emoji_id, background_emoji_id=background_emoji_id, accent_color=accent_color, colors=colors, dark_accent_color=dark_accent_color, dark_colors=dark_colors)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.dark_accent_color is not None else 0
        flags |= (1 << 1) if self.dark_colors else 0
        b.write(Int(flags))
        
        b.write(Long(self.collectible_id))
        
        b.write(Long(self.gift_emoji_id))
        
        b.write(Long(self.background_emoji_id))
        
        b.write(Int(self.accent_color))
        
        b.write(Vector(self.colors, Int))
        
        if self.dark_accent_color is not None:
            b.write(Int(self.dark_accent_color))
        
        if self.dark_colors:
            b.write(Vector(self.dark_colors, Int))
        
        return b.getvalue()
