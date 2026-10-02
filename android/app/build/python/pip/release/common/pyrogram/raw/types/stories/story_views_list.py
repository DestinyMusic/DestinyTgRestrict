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


class StoryViewsList(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.stories.StoryViewsList`.

    Details:
        - Layer: ``228``
        - ID: ``59D78FC5``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        views_count (``int`` ``32-bit``):
            N/A

        forwards_count (``int`` ``32-bit``):
            N/A

        reactions_count (``int`` ``32-bit``):
            N/A

        views (List of :obj:`StoryView <pyrogram.raw.base.StoryView>`):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        next_offset (``str``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            stories.GetStoryViewsList
    """

    __slots__: List[str] = ["count", "views_count", "forwards_count", "reactions_count", "views", "chats", "users", "next_offset"]

    ID = 0x59d78fc5
    QUALNAME = "types.stories.StoryViewsList"

    def __init__(self, *, count: int, views_count: int, forwards_count: int, reactions_count: int, views: List["raw.base.StoryView"], chats: List["raw.base.Chat"], users: List["raw.base.User"], next_offset: Optional[str] = None) -> None:
        self.count = count  # int
        self.views_count = views_count  # int
        self.forwards_count = forwards_count  # int
        self.reactions_count = reactions_count  # int
        self.views = views  # Vector<StoryView>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.next_offset = next_offset  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryViewsList":
        
        flags = Int.read(b)
        
        count = Int.read(b)
        
        views_count = Int.read(b)
        
        forwards_count = Int.read(b)
        
        reactions_count = Int.read(b)
        
        views = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        next_offset = String.read(b) if flags & (1 << 0) else None
        return StoryViewsList(count=count, views_count=views_count, forwards_count=forwards_count, reactions_count=reactions_count, views=views, chats=chats, users=users, next_offset=next_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.next_offset is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.count))
        
        b.write(Int(self.views_count))
        
        b.write(Int(self.forwards_count))
        
        b.write(Int(self.reactions_count))
        
        b.write(Vector(self.views))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        return b.getvalue()
