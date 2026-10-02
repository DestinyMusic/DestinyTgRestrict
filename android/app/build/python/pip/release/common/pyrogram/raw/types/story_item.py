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


class StoryItem(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StoryItem`.

    Details:
        - Layer: ``228``
        - ID: ``16A4B93C``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        expire_date (``int`` ``32-bit``):
            N/A

        media (:obj:`MessageMedia <pyrogram.raw.base.MessageMedia>`):
            N/A

        pinned (``bool``, *optional*):
            N/A

        public (``bool``, *optional*):
            N/A

        close_friends (``bool``, *optional*):
            N/A

        min (``bool``, *optional*):
            N/A

        noforwards (``bool``, *optional*):
            N/A

        edited (``bool``, *optional*):
            N/A

        contacts (``bool``, *optional*):
            N/A

        selected_contacts (``bool``, *optional*):
            N/A

        out (``bool``, *optional*):
            N/A

        from_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        fwd_from (:obj:`StoryFwdHeader <pyrogram.raw.base.StoryFwdHeader>`, *optional*):
            N/A

        caption (``str``, *optional*):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

        media_areas (List of :obj:`MediaArea <pyrogram.raw.base.MediaArea>`, *optional*):
            N/A

        privacy (List of :obj:`PrivacyRule <pyrogram.raw.base.PrivacyRule>`, *optional*):
            N/A

        views (:obj:`StoryViews <pyrogram.raw.base.StoryViews>`, *optional*):
            N/A

        sent_reaction (:obj:`Reaction <pyrogram.raw.base.Reaction>`, *optional*):
            N/A

        albums (List of ``int`` ``32-bit``, *optional*):
            N/A

        music (:obj:`Document <pyrogram.raw.base.Document>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "date", "expire_date", "media", "pinned", "public", "close_friends", "min", "noforwards", "edited", "contacts", "selected_contacts", "out", "from_id", "fwd_from", "caption", "entities", "media_areas", "privacy", "views", "sent_reaction", "albums", "music"]

    ID = 0x16a4b93c
    QUALNAME = "types.StoryItem"

    def __init__(self, *, id: int, date: int, expire_date: int, media: "raw.base.MessageMedia", pinned: Optional[bool] = None, public: Optional[bool] = None, close_friends: Optional[bool] = None, min: Optional[bool] = None, noforwards: Optional[bool] = None, edited: Optional[bool] = None, contacts: Optional[bool] = None, selected_contacts: Optional[bool] = None, out: Optional[bool] = None, from_id: "raw.base.Peer" = None, fwd_from: "raw.base.StoryFwdHeader" = None, caption: Optional[str] = None, entities: Optional[List["raw.base.MessageEntity"]] = None, media_areas: Optional[List["raw.base.MediaArea"]] = None, privacy: Optional[List["raw.base.PrivacyRule"]] = None, views: "raw.base.StoryViews" = None, sent_reaction: "raw.base.Reaction" = None, albums: Optional[List[int]] = None, music: "raw.base.Document" = None) -> None:
        self.id = id  # int
        self.date = date  # int
        self.expire_date = expire_date  # int
        self.media = media  # MessageMedia
        self.pinned = pinned  # flags.5?true
        self.public = public  # flags.7?true
        self.close_friends = close_friends  # flags.8?true
        self.min = min  # flags.9?true
        self.noforwards = noforwards  # flags.10?true
        self.edited = edited  # flags.11?true
        self.contacts = contacts  # flags.12?true
        self.selected_contacts = selected_contacts  # flags.13?true
        self.out = out  # flags.16?true
        self.from_id = from_id  # flags.18?Peer
        self.fwd_from = fwd_from  # flags.17?StoryFwdHeader
        self.caption = caption  # flags.0?string
        self.entities = entities  # flags.1?Vector<MessageEntity>
        self.media_areas = media_areas  # flags.14?Vector<MediaArea>
        self.privacy = privacy  # flags.2?Vector<PrivacyRule>
        self.views = views  # flags.3?StoryViews
        self.sent_reaction = sent_reaction  # flags.15?Reaction
        self.albums = albums  # flags.19?Vector<int>
        self.music = music  # flags.20?Document

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryItem":
        
        flags = Int.read(b)
        
        pinned = True if flags & (1 << 5) else False
        public = True if flags & (1 << 7) else False
        close_friends = True if flags & (1 << 8) else False
        min = True if flags & (1 << 9) else False
        noforwards = True if flags & (1 << 10) else False
        edited = True if flags & (1 << 11) else False
        contacts = True if flags & (1 << 12) else False
        selected_contacts = True if flags & (1 << 13) else False
        out = True if flags & (1 << 16) else False
        id = Int.read(b)
        
        date = Int.read(b)
        
        from_id = TLObject.read(b) if flags & (1 << 18) else None
        
        fwd_from = TLObject.read(b) if flags & (1 << 17) else None
        
        expire_date = Int.read(b)
        
        caption = String.read(b) if flags & (1 << 0) else None
        entities = TLObject.read(b) if flags & (1 << 1) else []
        
        media = TLObject.read(b)
        
        media_areas = TLObject.read(b) if flags & (1 << 14) else []
        
        privacy = TLObject.read(b) if flags & (1 << 2) else []
        
        views = TLObject.read(b) if flags & (1 << 3) else None
        
        sent_reaction = TLObject.read(b) if flags & (1 << 15) else None
        
        albums = TLObject.read(b, Int) if flags & (1 << 19) else []
        
        music = TLObject.read(b) if flags & (1 << 20) else None
        
        return StoryItem(id=id, date=date, expire_date=expire_date, media=media, pinned=pinned, public=public, close_friends=close_friends, min=min, noforwards=noforwards, edited=edited, contacts=contacts, selected_contacts=selected_contacts, out=out, from_id=from_id, fwd_from=fwd_from, caption=caption, entities=entities, media_areas=media_areas, privacy=privacy, views=views, sent_reaction=sent_reaction, albums=albums, music=music)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 5) if self.pinned else 0
        flags |= (1 << 7) if self.public else 0
        flags |= (1 << 8) if self.close_friends else 0
        flags |= (1 << 9) if self.min else 0
        flags |= (1 << 10) if self.noforwards else 0
        flags |= (1 << 11) if self.edited else 0
        flags |= (1 << 12) if self.contacts else 0
        flags |= (1 << 13) if self.selected_contacts else 0
        flags |= (1 << 16) if self.out else 0
        flags |= (1 << 18) if self.from_id is not None else 0
        flags |= (1 << 17) if self.fwd_from is not None else 0
        flags |= (1 << 0) if self.caption is not None else 0
        flags |= (1 << 1) if self.entities else 0
        flags |= (1 << 14) if self.media_areas else 0
        flags |= (1 << 2) if self.privacy else 0
        flags |= (1 << 3) if self.views is not None else 0
        flags |= (1 << 15) if self.sent_reaction is not None else 0
        flags |= (1 << 19) if self.albums else 0
        flags |= (1 << 20) if self.music is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(Int(self.date))
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        if self.fwd_from is not None:
            b.write(self.fwd_from.write())
        
        b.write(Int(self.expire_date))
        
        if self.caption is not None:
            b.write(String(self.caption))
        
        if self.entities:
            b.write(Vector(self.entities))
        
        b.write(self.media.write())
        
        if self.media_areas:
            b.write(Vector(self.media_areas))
        
        if self.privacy:
            b.write(Vector(self.privacy))
        
        if self.views is not None:
            b.write(self.views.write())
        
        if self.sent_reaction is not None:
            b.write(self.sent_reaction.write())
        
        if self.albums:
            b.write(Vector(self.albums, Int))
        
        if self.music is not None:
            b.write(self.music.write())
        
        return b.getvalue()
