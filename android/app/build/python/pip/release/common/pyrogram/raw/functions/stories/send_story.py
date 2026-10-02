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


class SendStory(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``8F9E6898``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`):
            N/A

        privacy_rules (List of :obj:`InputPrivacyRule <pyrogram.raw.base.InputPrivacyRule>`):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

        pinned (``bool``, *optional*):
            N/A

        noforwards (``bool``, *optional*):
            N/A

        fwd_modified (``bool``, *optional*):
            N/A

        media_areas (List of :obj:`MediaArea <pyrogram.raw.base.MediaArea>`, *optional*):
            N/A

        caption (``str``, *optional*):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

        period (``int`` ``32-bit``, *optional*):
            N/A

        fwd_from_id (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            N/A

        fwd_from_story (``int`` ``32-bit``, *optional*):
            N/A

        albums (List of ``int`` ``32-bit``, *optional*):
            N/A

        music (:obj:`InputDocument <pyrogram.raw.base.InputDocument>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "media", "privacy_rules", "random_id", "pinned", "noforwards", "fwd_modified", "media_areas", "caption", "entities", "period", "fwd_from_id", "fwd_from_story", "albums", "music"]

    ID = 0x8f9e6898
    QUALNAME = "functions.stories.SendStory"

    def __init__(self, *, peer: "raw.base.InputPeer", media: "raw.base.InputMedia", privacy_rules: List["raw.base.InputPrivacyRule"], random_id: int, pinned: Optional[bool] = None, noforwards: Optional[bool] = None, fwd_modified: Optional[bool] = None, media_areas: Optional[List["raw.base.MediaArea"]] = None, caption: Optional[str] = None, entities: Optional[List["raw.base.MessageEntity"]] = None, period: Optional[int] = None, fwd_from_id: "raw.base.InputPeer" = None, fwd_from_story: Optional[int] = None, albums: Optional[List[int]] = None, music: "raw.base.InputDocument" = None) -> None:
        self.peer = peer  # InputPeer
        self.media = media  # InputMedia
        self.privacy_rules = privacy_rules  # Vector<InputPrivacyRule>
        self.random_id = random_id  # long
        self.pinned = pinned  # flags.2?true
        self.noforwards = noforwards  # flags.4?true
        self.fwd_modified = fwd_modified  # flags.7?true
        self.media_areas = media_areas  # flags.5?Vector<MediaArea>
        self.caption = caption  # flags.0?string
        self.entities = entities  # flags.1?Vector<MessageEntity>
        self.period = period  # flags.3?int
        self.fwd_from_id = fwd_from_id  # flags.6?InputPeer
        self.fwd_from_story = fwd_from_story  # flags.6?int
        self.albums = albums  # flags.8?Vector<int>
        self.music = music  # flags.9?InputDocument

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendStory":
        
        flags = Int.read(b)
        
        pinned = True if flags & (1 << 2) else False
        noforwards = True if flags & (1 << 4) else False
        fwd_modified = True if flags & (1 << 7) else False
        peer = TLObject.read(b)
        
        media = TLObject.read(b)
        
        media_areas = TLObject.read(b) if flags & (1 << 5) else []
        
        caption = String.read(b) if flags & (1 << 0) else None
        entities = TLObject.read(b) if flags & (1 << 1) else []
        
        privacy_rules = TLObject.read(b)
        
        random_id = Long.read(b)
        
        period = Int.read(b) if flags & (1 << 3) else None
        fwd_from_id = TLObject.read(b) if flags & (1 << 6) else None
        
        fwd_from_story = Int.read(b) if flags & (1 << 6) else None
        albums = TLObject.read(b, Int) if flags & (1 << 8) else []
        
        music = TLObject.read(b) if flags & (1 << 9) else None
        
        return SendStory(peer=peer, media=media, privacy_rules=privacy_rules, random_id=random_id, pinned=pinned, noforwards=noforwards, fwd_modified=fwd_modified, media_areas=media_areas, caption=caption, entities=entities, period=period, fwd_from_id=fwd_from_id, fwd_from_story=fwd_from_story, albums=albums, music=music)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.pinned else 0
        flags |= (1 << 4) if self.noforwards else 0
        flags |= (1 << 7) if self.fwd_modified else 0
        flags |= (1 << 5) if self.media_areas else 0
        flags |= (1 << 0) if self.caption is not None else 0
        flags |= (1 << 1) if self.entities else 0
        flags |= (1 << 3) if self.period is not None else 0
        flags |= (1 << 6) if self.fwd_from_id is not None else 0
        flags |= (1 << 6) if self.fwd_from_story is not None else 0
        flags |= (1 << 8) if self.albums else 0
        flags |= (1 << 9) if self.music is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(self.media.write())
        
        if self.media_areas:
            b.write(Vector(self.media_areas))
        
        if self.caption is not None:
            b.write(String(self.caption))
        
        if self.entities:
            b.write(Vector(self.entities))
        
        b.write(Vector(self.privacy_rules))
        
        b.write(Long(self.random_id))
        
        if self.period is not None:
            b.write(Int(self.period))
        
        if self.fwd_from_id is not None:
            b.write(self.fwd_from_id.write())
        
        if self.fwd_from_story is not None:
            b.write(Int(self.fwd_from_story))
        
        if self.albums:
            b.write(Vector(self.albums, Int))
        
        if self.music is not None:
            b.write(self.music.write())
        
        return b.getvalue()
