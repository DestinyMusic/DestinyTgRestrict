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


class SendMessage(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``68CBD09F``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        receiver_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        message (``str``):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

        query_id (``int`` ``64-bit``, *optional*):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup <pyrogram.raw.base.ReplyMarkup>`, *optional*):
            N/A

        rich_message (:obj:`InputRichMessage <pyrogram.raw.base.InputRichMessage>`, *optional*):
            N/A

        reply_to (:obj:`InputReplyTo <pyrogram.raw.base.InputReplyTo>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "receiver_id", "message", "random_id", "query_id", "entities", "media", "reply_markup", "rich_message", "reply_to"]

    ID = 0x68cbd09f
    QUALNAME = "functions.ephemeral.SendMessage"

    def __init__(self, *, peer: "raw.base.InputPeer", receiver_id: "raw.base.InputUser", message: str, random_id: int, query_id: Optional[int] = None, entities: Optional[List["raw.base.MessageEntity"]] = None, media: "raw.base.InputMedia" = None, reply_markup: "raw.base.ReplyMarkup" = None, rich_message: "raw.base.InputRichMessage" = None, reply_to: "raw.base.InputReplyTo" = None) -> None:
        self.peer = peer  # InputPeer
        self.receiver_id = receiver_id  # InputUser
        self.message = message  # string
        self.random_id = random_id  # long
        self.query_id = query_id  # flags.0?long
        self.entities = entities  # flags.1?Vector<MessageEntity>
        self.media = media  # flags.2?InputMedia
        self.reply_markup = reply_markup  # flags.3?ReplyMarkup
        self.rich_message = rich_message  # flags.4?InputRichMessage
        self.reply_to = reply_to  # flags.5?InputReplyTo

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMessage":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        receiver_id = TLObject.read(b)
        
        query_id = Long.read(b) if flags & (1 << 0) else None
        message = String.read(b)
        
        entities = TLObject.read(b) if flags & (1 << 1) else []
        
        media = TLObject.read(b) if flags & (1 << 2) else None
        
        reply_markup = TLObject.read(b) if flags & (1 << 3) else None
        
        rich_message = TLObject.read(b) if flags & (1 << 4) else None
        
        random_id = Long.read(b)
        
        reply_to = TLObject.read(b) if flags & (1 << 5) else None
        
        return SendMessage(peer=peer, receiver_id=receiver_id, message=message, random_id=random_id, query_id=query_id, entities=entities, media=media, reply_markup=reply_markup, rich_message=rich_message, reply_to=reply_to)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.query_id is not None else 0
        flags |= (1 << 1) if self.entities else 0
        flags |= (1 << 2) if self.media is not None else 0
        flags |= (1 << 3) if self.reply_markup is not None else 0
        flags |= (1 << 4) if self.rich_message is not None else 0
        flags |= (1 << 5) if self.reply_to is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(self.receiver_id.write())
        
        if self.query_id is not None:
            b.write(Long(self.query_id))
        
        b.write(String(self.message))
        
        if self.entities:
            b.write(Vector(self.entities))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.rich_message is not None:
            b.write(self.rich_message.write())
        
        b.write(Long(self.random_id))
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        return b.getvalue()
