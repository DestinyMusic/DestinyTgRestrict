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


class PeerColor(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PeerColor`.

    Details:
        - Layer: ``228``
        - ID: ``B54B5ACF``

    Parameters:
        color (``int`` ``32-bit``, *optional*):
            N/A

        background_emoji_id (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["color", "background_emoji_id"]

    ID = 0xb54b5acf
    QUALNAME = "types.PeerColor"

    def __init__(self, *, color: Optional[int] = None, background_emoji_id: Optional[int] = None) -> None:
        self.color = color  # flags.0?int
        self.background_emoji_id = background_emoji_id  # flags.1?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerColor":
        
        flags = Int.read(b)
        
        color = Int.read(b) if flags & (1 << 0) else None
        background_emoji_id = Long.read(b) if flags & (1 << 1) else None
        return PeerColor(color=color, background_emoji_id=background_emoji_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.color is not None else 0
        flags |= (1 << 1) if self.background_emoji_id is not None else 0
        b.write(Int(flags))
        
        if self.color is not None:
            b.write(Int(self.color))
        
        if self.background_emoji_id is not None:
            b.write(Long(self.background_emoji_id))
        
        return b.getvalue()
