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


class StoryView(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StoryView`.

    Details:
        - Layer: ``228``
        - ID: ``B0BDEAC5``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        blocked (``bool``, *optional*):
            N/A

        blocked_my_stories_from (``bool``, *optional*):
            N/A

        reaction (:obj:`Reaction <pyrogram.raw.base.Reaction>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["user_id", "date", "blocked", "blocked_my_stories_from", "reaction"]

    ID = 0xb0bdeac5
    QUALNAME = "types.StoryView"

    def __init__(self, *, user_id: int, date: int, blocked: Optional[bool] = None, blocked_my_stories_from: Optional[bool] = None, reaction: "raw.base.Reaction" = None) -> None:
        self.user_id = user_id  # long
        self.date = date  # int
        self.blocked = blocked  # flags.0?true
        self.blocked_my_stories_from = blocked_my_stories_from  # flags.1?true
        self.reaction = reaction  # flags.2?Reaction

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryView":
        
        flags = Int.read(b)
        
        blocked = True if flags & (1 << 0) else False
        blocked_my_stories_from = True if flags & (1 << 1) else False
        user_id = Long.read(b)
        
        date = Int.read(b)
        
        reaction = TLObject.read(b) if flags & (1 << 2) else None
        
        return StoryView(user_id=user_id, date=date, blocked=blocked, blocked_my_stories_from=blocked_my_stories_from, reaction=reaction)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.blocked else 0
        flags |= (1 << 1) if self.blocked_my_stories_from else 0
        flags |= (1 << 2) if self.reaction is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.user_id))
        
        b.write(Int(self.date))
        
        if self.reaction is not None:
            b.write(self.reaction.write())
        
        return b.getvalue()
