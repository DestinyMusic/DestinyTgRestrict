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


class Stories(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.stories.Stories`.

    Details:
        - Layer: ``228``
        - ID: ``63C3DD0A``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        stories (List of :obj:`StoryItem <pyrogram.raw.base.StoryItem>`):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        pinned_to_top (List of ``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 4 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            stories.GetPinnedStories
            stories.GetStoriesArchive
            stories.GetStoriesByID
            stories.GetAlbumStories
    """

    __slots__: List[str] = ["count", "stories", "chats", "users", "pinned_to_top"]

    ID = 0x63c3dd0a
    QUALNAME = "types.stories.Stories"

    def __init__(self, *, count: int, stories: List["raw.base.StoryItem"], chats: List["raw.base.Chat"], users: List["raw.base.User"], pinned_to_top: Optional[List[int]] = None) -> None:
        self.count = count  # int
        self.stories = stories  # Vector<StoryItem>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.pinned_to_top = pinned_to_top  # flags.0?Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Stories":
        
        flags = Int.read(b)
        
        count = Int.read(b)
        
        stories = TLObject.read(b)
        
        pinned_to_top = TLObject.read(b, Int) if flags & (1 << 0) else []
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return Stories(count=count, stories=stories, chats=chats, users=users, pinned_to_top=pinned_to_top)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.pinned_to_top else 0
        b.write(Int(flags))
        
        b.write(Int(self.count))
        
        b.write(Vector(self.stories))
        
        if self.pinned_to_top:
            b.write(Vector(self.pinned_to_top, Int))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
