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


class MessageFwdHeader(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageFwdHeader`.

    Details:
        - Layer: ``228``
        - ID: ``4E4DF4BB``

    Parameters:
        date (``int`` ``32-bit``):
            N/A

        imported (``bool``, *optional*):
            N/A

        saved_out (``bool``, *optional*):
            N/A

        from_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        from_name (``str``, *optional*):
            N/A

        channel_post (``int`` ``32-bit``, *optional*):
            N/A

        post_author (``str``, *optional*):
            N/A

        saved_from_peer (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        saved_from_msg_id (``int`` ``32-bit``, *optional*):
            N/A

        saved_from_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        saved_from_name (``str``, *optional*):
            N/A

        saved_date (``int`` ``32-bit``, *optional*):
            N/A

        psa_type (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["date", "imported", "saved_out", "from_id", "from_name", "channel_post", "post_author", "saved_from_peer", "saved_from_msg_id", "saved_from_id", "saved_from_name", "saved_date", "psa_type"]

    ID = 0x4e4df4bb
    QUALNAME = "types.MessageFwdHeader"

    def __init__(self, *, date: int, imported: Optional[bool] = None, saved_out: Optional[bool] = None, from_id: "raw.base.Peer" = None, from_name: Optional[str] = None, channel_post: Optional[int] = None, post_author: Optional[str] = None, saved_from_peer: "raw.base.Peer" = None, saved_from_msg_id: Optional[int] = None, saved_from_id: "raw.base.Peer" = None, saved_from_name: Optional[str] = None, saved_date: Optional[int] = None, psa_type: Optional[str] = None) -> None:
        self.date = date  # int
        self.imported = imported  # flags.7?true
        self.saved_out = saved_out  # flags.11?true
        self.from_id = from_id  # flags.0?Peer
        self.from_name = from_name  # flags.5?string
        self.channel_post = channel_post  # flags.2?int
        self.post_author = post_author  # flags.3?string
        self.saved_from_peer = saved_from_peer  # flags.4?Peer
        self.saved_from_msg_id = saved_from_msg_id  # flags.4?int
        self.saved_from_id = saved_from_id  # flags.8?Peer
        self.saved_from_name = saved_from_name  # flags.9?string
        self.saved_date = saved_date  # flags.10?int
        self.psa_type = psa_type  # flags.6?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageFwdHeader":
        
        flags = Int.read(b)
        
        imported = True if flags & (1 << 7) else False
        saved_out = True if flags & (1 << 11) else False
        from_id = TLObject.read(b) if flags & (1 << 0) else None
        
        from_name = String.read(b) if flags & (1 << 5) else None
        date = Int.read(b)
        
        channel_post = Int.read(b) if flags & (1 << 2) else None
        post_author = String.read(b) if flags & (1 << 3) else None
        saved_from_peer = TLObject.read(b) if flags & (1 << 4) else None
        
        saved_from_msg_id = Int.read(b) if flags & (1 << 4) else None
        saved_from_id = TLObject.read(b) if flags & (1 << 8) else None
        
        saved_from_name = String.read(b) if flags & (1 << 9) else None
        saved_date = Int.read(b) if flags & (1 << 10) else None
        psa_type = String.read(b) if flags & (1 << 6) else None
        return MessageFwdHeader(date=date, imported=imported, saved_out=saved_out, from_id=from_id, from_name=from_name, channel_post=channel_post, post_author=post_author, saved_from_peer=saved_from_peer, saved_from_msg_id=saved_from_msg_id, saved_from_id=saved_from_id, saved_from_name=saved_from_name, saved_date=saved_date, psa_type=psa_type)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 7) if self.imported else 0
        flags |= (1 << 11) if self.saved_out else 0
        flags |= (1 << 0) if self.from_id is not None else 0
        flags |= (1 << 5) if self.from_name is not None else 0
        flags |= (1 << 2) if self.channel_post is not None else 0
        flags |= (1 << 3) if self.post_author is not None else 0
        flags |= (1 << 4) if self.saved_from_peer is not None else 0
        flags |= (1 << 4) if self.saved_from_msg_id is not None else 0
        flags |= (1 << 8) if self.saved_from_id is not None else 0
        flags |= (1 << 9) if self.saved_from_name is not None else 0
        flags |= (1 << 10) if self.saved_date is not None else 0
        flags |= (1 << 6) if self.psa_type is not None else 0
        b.write(Int(flags))
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        if self.from_name is not None:
            b.write(String(self.from_name))
        
        b.write(Int(self.date))
        
        if self.channel_post is not None:
            b.write(Int(self.channel_post))
        
        if self.post_author is not None:
            b.write(String(self.post_author))
        
        if self.saved_from_peer is not None:
            b.write(self.saved_from_peer.write())
        
        if self.saved_from_msg_id is not None:
            b.write(Int(self.saved_from_msg_id))
        
        if self.saved_from_id is not None:
            b.write(self.saved_from_id.write())
        
        if self.saved_from_name is not None:
            b.write(String(self.saved_from_name))
        
        if self.saved_date is not None:
            b.write(Int(self.saved_date))
        
        if self.psa_type is not None:
            b.write(String(self.psa_type))
        
        return b.getvalue()
