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


class DraftMessage(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.DraftMessage`.

    Details:
        - Layer: ``228``
        - ID: ``60FE3294``

    Parameters:
        message (``str``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        no_webpage (``bool``, *optional*):
            N/A

        invert_media (``bool``, *optional*):
            N/A

        reply_to (:obj:`InputReplyTo <pyrogram.raw.base.InputReplyTo>`, *optional*):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`, *optional*):
            N/A

        effect (``int`` ``64-bit``, *optional*):
            N/A

        suggested_post (:obj:`SuggestedPost <pyrogram.raw.base.SuggestedPost>`, *optional*):
            N/A

        rich_message (:obj:`RichMessage <pyrogram.raw.base.RichMessage>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["message", "date", "no_webpage", "invert_media", "reply_to", "entities", "media", "effect", "suggested_post", "rich_message"]

    ID = 0x60fe3294
    QUALNAME = "types.DraftMessage"

    def __init__(self, *, message: str, date: int, no_webpage: Optional[bool] = None, invert_media: Optional[bool] = None, reply_to: "raw.base.InputReplyTo" = None, entities: Optional[List["raw.base.MessageEntity"]] = None, media: "raw.base.InputMedia" = None, effect: Optional[int] = None, suggested_post: "raw.base.SuggestedPost" = None, rich_message: "raw.base.RichMessage" = None) -> None:
        self.message = message  # string
        self.date = date  # int
        self.no_webpage = no_webpage  # flags.1?true
        self.invert_media = invert_media  # flags.6?true
        self.reply_to = reply_to  # flags.4?InputReplyTo
        self.entities = entities  # flags.3?Vector<MessageEntity>
        self.media = media  # flags.5?InputMedia
        self.effect = effect  # flags.7?long
        self.suggested_post = suggested_post  # flags.8?SuggestedPost
        self.rich_message = rich_message  # flags.9?RichMessage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DraftMessage":
        
        flags = Int.read(b)
        
        no_webpage = True if flags & (1 << 1) else False
        invert_media = True if flags & (1 << 6) else False
        reply_to = TLObject.read(b) if flags & (1 << 4) else None
        
        message = String.read(b)
        
        entities = TLObject.read(b) if flags & (1 << 3) else []
        
        media = TLObject.read(b) if flags & (1 << 5) else None
        
        date = Int.read(b)
        
        effect = Long.read(b) if flags & (1 << 7) else None
        suggested_post = TLObject.read(b) if flags & (1 << 8) else None
        
        rich_message = TLObject.read(b) if flags & (1 << 9) else None
        
        return DraftMessage(message=message, date=date, no_webpage=no_webpage, invert_media=invert_media, reply_to=reply_to, entities=entities, media=media, effect=effect, suggested_post=suggested_post, rich_message=rich_message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.no_webpage else 0
        flags |= (1 << 6) if self.invert_media else 0
        flags |= (1 << 4) if self.reply_to is not None else 0
        flags |= (1 << 3) if self.entities else 0
        flags |= (1 << 5) if self.media is not None else 0
        flags |= (1 << 7) if self.effect is not None else 0
        flags |= (1 << 8) if self.suggested_post is not None else 0
        flags |= (1 << 9) if self.rich_message is not None else 0
        b.write(Int(flags))
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        b.write(String(self.message))
        
        if self.entities:
            b.write(Vector(self.entities))
        
        if self.media is not None:
            b.write(self.media.write())
        
        b.write(Int(self.date))
        
        if self.effect is not None:
            b.write(Long(self.effect))
        
        if self.suggested_post is not None:
            b.write(self.suggested_post.write())
        
        if self.rich_message is not None:
            b.write(self.rich_message.write())
        
        return b.getvalue()
