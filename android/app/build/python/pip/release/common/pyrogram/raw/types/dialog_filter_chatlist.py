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


class DialogFilterChatlist(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.DialogFilter`.

    Details:
        - Layer: ``228``
        - ID: ``96537BD7``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        title (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

        pinned_peers (List of :obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        include_peers (List of :obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        has_my_invites (``bool``, *optional*):
            N/A

        title_noanimate (``bool``, *optional*):
            N/A

        emoticon (``str``, *optional*):
            N/A

        color (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "title", "pinned_peers", "include_peers", "has_my_invites", "title_noanimate", "emoticon", "color"]

    ID = 0x96537bd7
    QUALNAME = "types.DialogFilterChatlist"

    def __init__(self, *, id: int, title: "raw.base.TextWithEntities", pinned_peers: List["raw.base.InputPeer"], include_peers: List["raw.base.InputPeer"], has_my_invites: Optional[bool] = None, title_noanimate: Optional[bool] = None, emoticon: Optional[str] = None, color: Optional[int] = None) -> None:
        self.id = id  # int
        self.title = title  # TextWithEntities
        self.pinned_peers = pinned_peers  # Vector<InputPeer>
        self.include_peers = include_peers  # Vector<InputPeer>
        self.has_my_invites = has_my_invites  # flags.26?true
        self.title_noanimate = title_noanimate  # flags.28?true
        self.emoticon = emoticon  # flags.25?string
        self.color = color  # flags.27?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DialogFilterChatlist":
        
        flags = Int.read(b)
        
        has_my_invites = True if flags & (1 << 26) else False
        title_noanimate = True if flags & (1 << 28) else False
        id = Int.read(b)
        
        title = TLObject.read(b)
        
        emoticon = String.read(b) if flags & (1 << 25) else None
        color = Int.read(b) if flags & (1 << 27) else None
        pinned_peers = TLObject.read(b)
        
        include_peers = TLObject.read(b)
        
        return DialogFilterChatlist(id=id, title=title, pinned_peers=pinned_peers, include_peers=include_peers, has_my_invites=has_my_invites, title_noanimate=title_noanimate, emoticon=emoticon, color=color)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 26) if self.has_my_invites else 0
        flags |= (1 << 28) if self.title_noanimate else 0
        flags |= (1 << 25) if self.emoticon is not None else 0
        flags |= (1 << 27) if self.color is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(self.title.write())
        
        if self.emoticon is not None:
            b.write(String(self.emoticon))
        
        if self.color is not None:
            b.write(Int(self.color))
        
        b.write(Vector(self.pinned_peers))
        
        b.write(Vector(self.include_peers))
        
        return b.getvalue()
