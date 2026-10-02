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


class GetStoryViewsList(TLObject["raw.base.stories.StoryViewsList"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``7ED23C57``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        id (``int`` ``32-bit``):
            N/A

        offset (``str``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

        just_contacts (``bool``, *optional*):
            N/A

        reactions_first (``bool``, *optional*):
            N/A

        forwards_first (``bool``, *optional*):
            N/A

        q (``str``, *optional*):
            N/A

    Returns:
        :obj:`stories.StoryViewsList <pyrogram.raw.base.stories.StoryViewsList>`
    """

    __slots__: List[str] = ["peer", "id", "offset", "limit", "just_contacts", "reactions_first", "forwards_first", "q"]

    ID = 0x7ed23c57
    QUALNAME = "functions.stories.GetStoryViewsList"

    def __init__(self, *, peer: "raw.base.InputPeer", id: int, offset: str, limit: int, just_contacts: Optional[bool] = None, reactions_first: Optional[bool] = None, forwards_first: Optional[bool] = None, q: Optional[str] = None) -> None:
        self.peer = peer  # InputPeer
        self.id = id  # int
        self.offset = offset  # string
        self.limit = limit  # int
        self.just_contacts = just_contacts  # flags.0?true
        self.reactions_first = reactions_first  # flags.2?true
        self.forwards_first = forwards_first  # flags.3?true
        self.q = q  # flags.1?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStoryViewsList":
        
        flags = Int.read(b)
        
        just_contacts = True if flags & (1 << 0) else False
        reactions_first = True if flags & (1 << 2) else False
        forwards_first = True if flags & (1 << 3) else False
        peer = TLObject.read(b)
        
        q = String.read(b) if flags & (1 << 1) else None
        id = Int.read(b)
        
        offset = String.read(b)
        
        limit = Int.read(b)
        
        return GetStoryViewsList(peer=peer, id=id, offset=offset, limit=limit, just_contacts=just_contacts, reactions_first=reactions_first, forwards_first=forwards_first, q=q)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.just_contacts else 0
        flags |= (1 << 2) if self.reactions_first else 0
        flags |= (1 << 3) if self.forwards_first else 0
        flags |= (1 << 1) if self.q is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        if self.q is not None:
            b.write(String(self.q))
        
        b.write(Int(self.id))
        
        b.write(String(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
