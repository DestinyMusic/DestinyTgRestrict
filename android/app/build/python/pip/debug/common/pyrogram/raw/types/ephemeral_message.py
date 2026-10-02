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


class EphemeralMessage(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.EphemeralMessage`.

    Details:
        - Layer: ``228``
        - ID: ``D9C6DC1A``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        from_id (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        peer_id (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        receiver_id (``int`` ``64-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        message (``str``):
            N/A

        out (``bool``, *optional*):
            N/A

        top_msg_id (``int`` ``32-bit``, *optional*):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

        media (:obj:`MessageMedia <pyrogram.raw.base.MessageMedia>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup <pyrogram.raw.base.ReplyMarkup>`, *optional*):
            N/A

        reply_to (:obj:`MessageReplyHeader <pyrogram.raw.base.MessageReplyHeader>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "from_id", "peer_id", "receiver_id", "date", "message", "out", "top_msg_id", "entities", "media", "reply_markup", "reply_to"]

    ID = 0xd9c6dc1a
    QUALNAME = "types.EphemeralMessage"

    def __init__(self, *, id: int, from_id: "raw.base.Peer", peer_id: "raw.base.Peer", receiver_id: int, date: int, message: str, out: Optional[bool] = None, top_msg_id: Optional[int] = None, entities: Optional[List["raw.base.MessageEntity"]] = None, media: "raw.base.MessageMedia" = None, reply_markup: "raw.base.ReplyMarkup" = None, reply_to: "raw.base.MessageReplyHeader" = None) -> None:
        self.id = id  # int
        self.from_id = from_id  # Peer
        self.peer_id = peer_id  # Peer
        self.receiver_id = receiver_id  # long
        self.date = date  # int
        self.message = message  # string
        self.out = out  # flags.0?true
        self.top_msg_id = top_msg_id  # flags.1?int
        self.entities = entities  # flags.2?Vector<MessageEntity>
        self.media = media  # flags.3?MessageMedia
        self.reply_markup = reply_markup  # flags.4?ReplyMarkup
        self.reply_to = reply_to  # flags.6?MessageReplyHeader

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EphemeralMessage":
        
        flags = Int.read(b)
        
        out = True if flags & (1 << 0) else False
        id = Int.read(b)
        
        from_id = TLObject.read(b)
        
        peer_id = TLObject.read(b)
        
        receiver_id = Long.read(b)
        
        top_msg_id = Int.read(b) if flags & (1 << 1) else None
        date = Int.read(b)
        
        message = String.read(b)
        
        entities = TLObject.read(b) if flags & (1 << 2) else []
        
        media = TLObject.read(b) if flags & (1 << 3) else None
        
        reply_markup = TLObject.read(b) if flags & (1 << 4) else None
        
        reply_to = TLObject.read(b) if flags & (1 << 6) else None
        
        return EphemeralMessage(id=id, from_id=from_id, peer_id=peer_id, receiver_id=receiver_id, date=date, message=message, out=out, top_msg_id=top_msg_id, entities=entities, media=media, reply_markup=reply_markup, reply_to=reply_to)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.out else 0
        flags |= (1 << 1) if self.top_msg_id is not None else 0
        flags |= (1 << 2) if self.entities else 0
        flags |= (1 << 3) if self.media is not None else 0
        flags |= (1 << 4) if self.reply_markup is not None else 0
        flags |= (1 << 6) if self.reply_to is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(self.from_id.write())
        
        b.write(self.peer_id.write())
        
        b.write(Long(self.receiver_id))
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        b.write(Int(self.date))
        
        b.write(String(self.message))
        
        if self.entities:
            b.write(Vector(self.entities))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        return b.getvalue()
