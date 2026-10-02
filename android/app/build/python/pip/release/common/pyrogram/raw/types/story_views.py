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


class StoryViews(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StoryViews`.

    Details:
        - Layer: ``228``
        - ID: ``8D595CD6``

    Parameters:
        views_count (``int`` ``32-bit``):
            N/A

        has_viewers (``bool``, *optional*):
            N/A

        forwards_count (``int`` ``32-bit``, *optional*):
            N/A

        reactions (List of :obj:`ReactionCount <pyrogram.raw.base.ReactionCount>`, *optional*):
            N/A

        reactions_count (``int`` ``32-bit``, *optional*):
            N/A

        recent_viewers (List of ``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["views_count", "has_viewers", "forwards_count", "reactions", "reactions_count", "recent_viewers"]

    ID = 0x8d595cd6
    QUALNAME = "types.StoryViews"

    def __init__(self, *, views_count: int, has_viewers: Optional[bool] = None, forwards_count: Optional[int] = None, reactions: Optional[List["raw.base.ReactionCount"]] = None, reactions_count: Optional[int] = None, recent_viewers: Optional[List[int]] = None) -> None:
        self.views_count = views_count  # int
        self.has_viewers = has_viewers  # flags.1?true
        self.forwards_count = forwards_count  # flags.2?int
        self.reactions = reactions  # flags.3?Vector<ReactionCount>
        self.reactions_count = reactions_count  # flags.4?int
        self.recent_viewers = recent_viewers  # flags.0?Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryViews":
        
        flags = Int.read(b)
        
        has_viewers = True if flags & (1 << 1) else False
        views_count = Int.read(b)
        
        forwards_count = Int.read(b) if flags & (1 << 2) else None
        reactions = TLObject.read(b) if flags & (1 << 3) else []
        
        reactions_count = Int.read(b) if flags & (1 << 4) else None
        recent_viewers = TLObject.read(b, Long) if flags & (1 << 0) else []
        
        return StoryViews(views_count=views_count, has_viewers=has_viewers, forwards_count=forwards_count, reactions=reactions, reactions_count=reactions_count, recent_viewers=recent_viewers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.has_viewers else 0
        flags |= (1 << 2) if self.forwards_count is not None else 0
        flags |= (1 << 3) if self.reactions else 0
        flags |= (1 << 4) if self.reactions_count is not None else 0
        flags |= (1 << 0) if self.recent_viewers else 0
        b.write(Int(flags))
        
        b.write(Int(self.views_count))
        
        if self.forwards_count is not None:
            b.write(Int(self.forwards_count))
        
        if self.reactions:
            b.write(Vector(self.reactions))
        
        if self.reactions_count is not None:
            b.write(Int(self.reactions_count))
        
        if self.recent_viewers:
            b.write(Vector(self.recent_viewers, Long))
        
        return b.getvalue()
