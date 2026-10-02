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


class MonoForumDialog(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.SavedDialog`.

    Details:
        - Layer: ``228``
        - ID: ``64407EA7``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        top_message (``int`` ``32-bit``):
            N/A

        read_inbox_max_id (``int`` ``32-bit``):
            N/A

        read_outbox_max_id (``int`` ``32-bit``):
            N/A

        unread_count (``int`` ``32-bit``):
            N/A

        unread_reactions_count (``int`` ``32-bit``):
            N/A

        unread_mark (``bool``, *optional*):
            N/A

        nopaid_messages_exception (``bool``, *optional*):
            N/A

        draft (:obj:`DraftMessage <pyrogram.raw.base.DraftMessage>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "top_message", "read_inbox_max_id", "read_outbox_max_id", "unread_count", "unread_reactions_count", "unread_mark", "nopaid_messages_exception", "draft"]

    ID = 0x64407ea7
    QUALNAME = "types.MonoForumDialog"

    def __init__(self, *, peer: "raw.base.Peer", top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_reactions_count: int, unread_mark: Optional[bool] = None, nopaid_messages_exception: Optional[bool] = None, draft: "raw.base.DraftMessage" = None) -> None:
        self.peer = peer  # Peer
        self.top_message = top_message  # int
        self.read_inbox_max_id = read_inbox_max_id  # int
        self.read_outbox_max_id = read_outbox_max_id  # int
        self.unread_count = unread_count  # int
        self.unread_reactions_count = unread_reactions_count  # int
        self.unread_mark = unread_mark  # flags.3?true
        self.nopaid_messages_exception = nopaid_messages_exception  # flags.4?true
        self.draft = draft  # flags.1?DraftMessage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MonoForumDialog":
        
        flags = Int.read(b)
        
        unread_mark = True if flags & (1 << 3) else False
        nopaid_messages_exception = True if flags & (1 << 4) else False
        peer = TLObject.read(b)
        
        top_message = Int.read(b)
        
        read_inbox_max_id = Int.read(b)
        
        read_outbox_max_id = Int.read(b)
        
        unread_count = Int.read(b)
        
        unread_reactions_count = Int.read(b)
        
        draft = TLObject.read(b) if flags & (1 << 1) else None
        
        return MonoForumDialog(peer=peer, top_message=top_message, read_inbox_max_id=read_inbox_max_id, read_outbox_max_id=read_outbox_max_id, unread_count=unread_count, unread_reactions_count=unread_reactions_count, unread_mark=unread_mark, nopaid_messages_exception=nopaid_messages_exception, draft=draft)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.unread_mark else 0
        flags |= (1 << 4) if self.nopaid_messages_exception else 0
        flags |= (1 << 1) if self.draft is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.top_message))
        
        b.write(Int(self.read_inbox_max_id))
        
        b.write(Int(self.read_outbox_max_id))
        
        b.write(Int(self.unread_count))
        
        b.write(Int(self.unread_reactions_count))
        
        if self.draft is not None:
            b.write(self.draft.write())
        
        return b.getvalue()
