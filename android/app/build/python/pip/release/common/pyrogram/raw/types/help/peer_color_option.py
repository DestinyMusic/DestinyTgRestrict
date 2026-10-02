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


class PeerColorOption(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.help.PeerColorOption`.

    Details:
        - Layer: ``228``
        - ID: ``ADEC6EBE``

    Parameters:
        color_id (``int`` ``32-bit``):
            N/A

        hidden (``bool``, *optional*):
            N/A

        colors (:obj:`help.PeerColorSet <pyrogram.raw.base.help.PeerColorSet>`, *optional*):
            N/A

        dark_colors (:obj:`help.PeerColorSet <pyrogram.raw.base.help.PeerColorSet>`, *optional*):
            N/A

        channel_min_level (``int`` ``32-bit``, *optional*):
            N/A

        group_min_level (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["color_id", "hidden", "colors", "dark_colors", "channel_min_level", "group_min_level"]

    ID = 0xadec6ebe
    QUALNAME = "types.help.PeerColorOption"

    def __init__(self, *, color_id: int, hidden: Optional[bool] = None, colors: "raw.base.help.PeerColorSet" = None, dark_colors: "raw.base.help.PeerColorSet" = None, channel_min_level: Optional[int] = None, group_min_level: Optional[int] = None) -> None:
        self.color_id = color_id  # int
        self.hidden = hidden  # flags.0?true
        self.colors = colors  # flags.1?help.PeerColorSet
        self.dark_colors = dark_colors  # flags.2?help.PeerColorSet
        self.channel_min_level = channel_min_level  # flags.3?int
        self.group_min_level = group_min_level  # flags.4?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerColorOption":
        
        flags = Int.read(b)
        
        hidden = True if flags & (1 << 0) else False
        color_id = Int.read(b)
        
        colors = TLObject.read(b) if flags & (1 << 1) else None
        
        dark_colors = TLObject.read(b) if flags & (1 << 2) else None
        
        channel_min_level = Int.read(b) if flags & (1 << 3) else None
        group_min_level = Int.read(b) if flags & (1 << 4) else None
        return PeerColorOption(color_id=color_id, hidden=hidden, colors=colors, dark_colors=dark_colors, channel_min_level=channel_min_level, group_min_level=group_min_level)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.hidden else 0
        flags |= (1 << 1) if self.colors is not None else 0
        flags |= (1 << 2) if self.dark_colors is not None else 0
        flags |= (1 << 3) if self.channel_min_level is not None else 0
        flags |= (1 << 4) if self.group_min_level is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.color_id))
        
        if self.colors is not None:
            b.write(self.colors.write())
        
        if self.dark_colors is not None:
            b.write(self.dark_colors.write())
        
        if self.channel_min_level is not None:
            b.write(Int(self.channel_min_level))
        
        if self.group_min_level is not None:
            b.write(Int(self.group_min_level))
        
        return b.getvalue()
