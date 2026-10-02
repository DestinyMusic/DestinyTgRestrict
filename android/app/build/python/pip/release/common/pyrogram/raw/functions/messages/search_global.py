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


class SearchGlobal(TLObject["raw.base.messages.Messages"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``6126A43C``

    Parameters:
        q (``str``):
            N/A

        filter (:obj:`MessagesFilter <pyrogram.raw.base.MessagesFilter>`):
            N/A

        min_date (``int`` ``32-bit``):
            N/A

        max_date (``int`` ``32-bit``):
            N/A

        offset_rate (``int`` ``32-bit``):
            N/A

        offset_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        offset_id (``int`` ``32-bit``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

        broadcasts_only (``bool``, *optional*):
            N/A

        groups_only (``bool``, *optional*):
            N/A

        users_only (``bool``, *optional*):
            N/A

        folder_id (``int`` ``32-bit``, *optional*):
            N/A

        community (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`, *optional*):
            N/A

    Returns:
        :obj:`messages.Messages <pyrogram.raw.base.messages.Messages>`
    """

    __slots__: List[str] = ["q", "filter", "min_date", "max_date", "offset_rate", "offset_peer", "offset_id", "limit", "broadcasts_only", "groups_only", "users_only", "folder_id", "community"]

    ID = 0x6126a43c
    QUALNAME = "functions.messages.SearchGlobal"

    def __init__(self, *, q: str, filter: "raw.base.MessagesFilter", min_date: int, max_date: int, offset_rate: int, offset_peer: "raw.base.InputPeer", offset_id: int, limit: int, broadcasts_only: Optional[bool] = None, groups_only: Optional[bool] = None, users_only: Optional[bool] = None, folder_id: Optional[int] = None, community: "raw.base.InputChannel" = None) -> None:
        self.q = q  # string
        self.filter = filter  # MessagesFilter
        self.min_date = min_date  # int
        self.max_date = max_date  # int
        self.offset_rate = offset_rate  # int
        self.offset_peer = offset_peer  # InputPeer
        self.offset_id = offset_id  # int
        self.limit = limit  # int
        self.broadcasts_only = broadcasts_only  # flags.1?true
        self.groups_only = groups_only  # flags.2?true
        self.users_only = users_only  # flags.3?true
        self.folder_id = folder_id  # flags.0?int
        self.community = community  # flags.4?InputChannel

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchGlobal":
        
        flags = Int.read(b)
        
        broadcasts_only = True if flags & (1 << 1) else False
        groups_only = True if flags & (1 << 2) else False
        users_only = True if flags & (1 << 3) else False
        folder_id = Int.read(b) if flags & (1 << 0) else None
        community = TLObject.read(b) if flags & (1 << 4) else None
        
        q = String.read(b)
        
        filter = TLObject.read(b)
        
        min_date = Int.read(b)
        
        max_date = Int.read(b)
        
        offset_rate = Int.read(b)
        
        offset_peer = TLObject.read(b)
        
        offset_id = Int.read(b)
        
        limit = Int.read(b)
        
        return SearchGlobal(q=q, filter=filter, min_date=min_date, max_date=max_date, offset_rate=offset_rate, offset_peer=offset_peer, offset_id=offset_id, limit=limit, broadcasts_only=broadcasts_only, groups_only=groups_only, users_only=users_only, folder_id=folder_id, community=community)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.broadcasts_only else 0
        flags |= (1 << 2) if self.groups_only else 0
        flags |= (1 << 3) if self.users_only else 0
        flags |= (1 << 0) if self.folder_id is not None else 0
        flags |= (1 << 4) if self.community is not None else 0
        b.write(Int(flags))
        
        if self.folder_id is not None:
            b.write(Int(self.folder_id))
        
        if self.community is not None:
            b.write(self.community.write())
        
        b.write(String(self.q))
        
        b.write(self.filter.write())
        
        b.write(Int(self.min_date))
        
        b.write(Int(self.max_date))
        
        b.write(Int(self.offset_rate))
        
        b.write(self.offset_peer.write())
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
