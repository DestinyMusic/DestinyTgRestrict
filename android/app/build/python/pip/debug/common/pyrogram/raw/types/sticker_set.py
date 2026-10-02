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


class StickerSet(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StickerSet`.

    Details:
        - Layer: ``228``
        - ID: ``2DD14EDC``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        access_hash (``int`` ``64-bit``):
            N/A

        title (``str``):
            N/A

        short_name (``str``):
            N/A

        count (``int`` ``32-bit``):
            N/A

        hash (``int`` ``32-bit``):
            N/A

        archived (``bool``, *optional*):
            N/A

        official (``bool``, *optional*):
            N/A

        masks (``bool``, *optional*):
            N/A

        emojis (``bool``, *optional*):
            N/A

        text_color (``bool``, *optional*):
            N/A

        channel_emoji_status (``bool``, *optional*):
            N/A

        creator (``bool``, *optional*):
            N/A

        installed_date (``int`` ``32-bit``, *optional*):
            N/A

        thumbs (List of :obj:`PhotoSize <pyrogram.raw.base.PhotoSize>`, *optional*):
            N/A

        thumb_dc_id (``int`` ``32-bit``, *optional*):
            N/A

        thumb_version (``int`` ``32-bit``, *optional*):
            N/A

        thumb_document_id (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "access_hash", "title", "short_name", "count", "hash", "archived", "official", "masks", "emojis", "text_color", "channel_emoji_status", "creator", "installed_date", "thumbs", "thumb_dc_id", "thumb_version", "thumb_document_id"]

    ID = 0x2dd14edc
    QUALNAME = "types.StickerSet"

    def __init__(self, *, id: int, access_hash: int, title: str, short_name: str, count: int, hash: int, archived: Optional[bool] = None, official: Optional[bool] = None, masks: Optional[bool] = None, emojis: Optional[bool] = None, text_color: Optional[bool] = None, channel_emoji_status: Optional[bool] = None, creator: Optional[bool] = None, installed_date: Optional[int] = None, thumbs: Optional[List["raw.base.PhotoSize"]] = None, thumb_dc_id: Optional[int] = None, thumb_version: Optional[int] = None, thumb_document_id: Optional[int] = None) -> None:
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.title = title  # string
        self.short_name = short_name  # string
        self.count = count  # int
        self.hash = hash  # int
        self.archived = archived  # flags.1?true
        self.official = official  # flags.2?true
        self.masks = masks  # flags.3?true
        self.emojis = emojis  # flags.7?true
        self.text_color = text_color  # flags.9?true
        self.channel_emoji_status = channel_emoji_status  # flags.10?true
        self.creator = creator  # flags.11?true
        self.installed_date = installed_date  # flags.0?int
        self.thumbs = thumbs  # flags.4?Vector<PhotoSize>
        self.thumb_dc_id = thumb_dc_id  # flags.4?int
        self.thumb_version = thumb_version  # flags.4?int
        self.thumb_document_id = thumb_document_id  # flags.8?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StickerSet":
        
        flags = Int.read(b)
        
        archived = True if flags & (1 << 1) else False
        official = True if flags & (1 << 2) else False
        masks = True if flags & (1 << 3) else False
        emojis = True if flags & (1 << 7) else False
        text_color = True if flags & (1 << 9) else False
        channel_emoji_status = True if flags & (1 << 10) else False
        creator = True if flags & (1 << 11) else False
        installed_date = Int.read(b) if flags & (1 << 0) else None
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        title = String.read(b)
        
        short_name = String.read(b)
        
        thumbs = TLObject.read(b) if flags & (1 << 4) else []
        
        thumb_dc_id = Int.read(b) if flags & (1 << 4) else None
        thumb_version = Int.read(b) if flags & (1 << 4) else None
        thumb_document_id = Long.read(b) if flags & (1 << 8) else None
        count = Int.read(b)
        
        hash = Int.read(b)
        
        return StickerSet(id=id, access_hash=access_hash, title=title, short_name=short_name, count=count, hash=hash, archived=archived, official=official, masks=masks, emojis=emojis, text_color=text_color, channel_emoji_status=channel_emoji_status, creator=creator, installed_date=installed_date, thumbs=thumbs, thumb_dc_id=thumb_dc_id, thumb_version=thumb_version, thumb_document_id=thumb_document_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.archived else 0
        flags |= (1 << 2) if self.official else 0
        flags |= (1 << 3) if self.masks else 0
        flags |= (1 << 7) if self.emojis else 0
        flags |= (1 << 9) if self.text_color else 0
        flags |= (1 << 10) if self.channel_emoji_status else 0
        flags |= (1 << 11) if self.creator else 0
        flags |= (1 << 0) if self.installed_date is not None else 0
        flags |= (1 << 4) if self.thumbs else 0
        flags |= (1 << 4) if self.thumb_dc_id is not None else 0
        flags |= (1 << 4) if self.thumb_version is not None else 0
        flags |= (1 << 8) if self.thumb_document_id is not None else 0
        b.write(Int(flags))
        
        if self.installed_date is not None:
            b.write(Int(self.installed_date))
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(String(self.title))
        
        b.write(String(self.short_name))
        
        if self.thumbs:
            b.write(Vector(self.thumbs))
        
        if self.thumb_dc_id is not None:
            b.write(Int(self.thumb_dc_id))
        
        if self.thumb_version is not None:
            b.write(Int(self.thumb_version))
        
        if self.thumb_document_id is not None:
            b.write(Long(self.thumb_document_id))
        
        b.write(Int(self.count))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
