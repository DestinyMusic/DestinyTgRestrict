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


class StoryFwdHeader(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StoryFwdHeader`.

    Details:
        - Layer: ``228``
        - ID: ``B826E150``

    Parameters:
        modified (``bool``, *optional*):
            N/A

        from_peer (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        from_name (``str``, *optional*):
            N/A

        story_id (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["modified", "from_peer", "from_name", "story_id"]

    ID = 0xb826e150
    QUALNAME = "types.StoryFwdHeader"

    def __init__(self, *, modified: Optional[bool] = None, from_peer: "raw.base.Peer" = None, from_name: Optional[str] = None, story_id: Optional[int] = None) -> None:
        self.modified = modified  # flags.3?true
        self.from_peer = from_peer  # flags.0?Peer
        self.from_name = from_name  # flags.1?string
        self.story_id = story_id  # flags.2?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryFwdHeader":
        
        flags = Int.read(b)
        
        modified = True if flags & (1 << 3) else False
        from_peer = TLObject.read(b) if flags & (1 << 0) else None
        
        from_name = String.read(b) if flags & (1 << 1) else None
        story_id = Int.read(b) if flags & (1 << 2) else None
        return StoryFwdHeader(modified=modified, from_peer=from_peer, from_name=from_name, story_id=story_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.modified else 0
        flags |= (1 << 0) if self.from_peer is not None else 0
        flags |= (1 << 1) if self.from_name is not None else 0
        flags |= (1 << 2) if self.story_id is not None else 0
        b.write(Int(flags))
        
        if self.from_peer is not None:
            b.write(self.from_peer.write())
        
        if self.from_name is not None:
            b.write(String(self.from_name))
        
        if self.story_id is not None:
            b.write(Int(self.story_id))
        
        return b.getvalue()
