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


class WebPageAttributeStory(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.WebPageAttribute`.

    Details:
        - Layer: ``228``
        - ID: ``2E94C3E7``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        id (``int`` ``32-bit``):
            N/A

        story (:obj:`StoryItem <pyrogram.raw.base.StoryItem>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "id", "story"]

    ID = 0x2e94c3e7
    QUALNAME = "types.WebPageAttributeStory"

    def __init__(self, *, peer: "raw.base.Peer", id: int, story: "raw.base.StoryItem" = None) -> None:
        self.peer = peer  # Peer
        self.id = id  # int
        self.story = story  # flags.0?StoryItem

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebPageAttributeStory":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        id = Int.read(b)
        
        story = TLObject.read(b) if flags & (1 << 0) else None
        
        return WebPageAttributeStory(peer=peer, id=id, story=story)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.story is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.id))
        
        if self.story is not None:
            b.write(self.story.write())
        
        return b.getvalue()
