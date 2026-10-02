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


class MessageMediaDocument(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageMedia`.

    Details:
        - Layer: ``228``
        - ID: ``52D8CCD9``

    Parameters:
        nopremium (``bool``, *optional*):
            N/A

        spoiler (``bool``, *optional*):
            N/A

        video (``bool``, *optional*):
            N/A

        round (``bool``, *optional*):
            N/A

        voice (``bool``, *optional*):
            N/A

        document (:obj:`Document <pyrogram.raw.base.Document>`, *optional*):
            N/A

        alt_documents (List of :obj:`Document <pyrogram.raw.base.Document>`, *optional*):
            N/A

        video_cover (:obj:`Photo <pyrogram.raw.base.Photo>`, *optional*):
            N/A

        video_timestamp (``int`` ``32-bit``, *optional*):
            N/A

        ttl_seconds (``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.UploadMedia
            messages.UploadImportedMedia
    """

    __slots__: List[str] = ["nopremium", "spoiler", "video", "round", "voice", "document", "alt_documents", "video_cover", "video_timestamp", "ttl_seconds"]

    ID = 0x52d8ccd9
    QUALNAME = "types.MessageMediaDocument"

    def __init__(self, *, nopremium: Optional[bool] = None, spoiler: Optional[bool] = None, video: Optional[bool] = None, round: Optional[bool] = None, voice: Optional[bool] = None, document: "raw.base.Document" = None, alt_documents: Optional[List["raw.base.Document"]] = None, video_cover: "raw.base.Photo" = None, video_timestamp: Optional[int] = None, ttl_seconds: Optional[int] = None) -> None:
        self.nopremium = nopremium  # flags.3?true
        self.spoiler = spoiler  # flags.4?true
        self.video = video  # flags.6?true
        self.round = round  # flags.7?true
        self.voice = voice  # flags.8?true
        self.document = document  # flags.0?Document
        self.alt_documents = alt_documents  # flags.5?Vector<Document>
        self.video_cover = video_cover  # flags.9?Photo
        self.video_timestamp = video_timestamp  # flags.10?int
        self.ttl_seconds = ttl_seconds  # flags.2?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaDocument":
        
        flags = Int.read(b)
        
        nopremium = True if flags & (1 << 3) else False
        spoiler = True if flags & (1 << 4) else False
        video = True if flags & (1 << 6) else False
        round = True if flags & (1 << 7) else False
        voice = True if flags & (1 << 8) else False
        document = TLObject.read(b) if flags & (1 << 0) else None
        
        alt_documents = TLObject.read(b) if flags & (1 << 5) else []
        
        video_cover = TLObject.read(b) if flags & (1 << 9) else None
        
        video_timestamp = Int.read(b) if flags & (1 << 10) else None
        ttl_seconds = Int.read(b) if flags & (1 << 2) else None
        return MessageMediaDocument(nopremium=nopremium, spoiler=spoiler, video=video, round=round, voice=voice, document=document, alt_documents=alt_documents, video_cover=video_cover, video_timestamp=video_timestamp, ttl_seconds=ttl_seconds)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.nopremium else 0
        flags |= (1 << 4) if self.spoiler else 0
        flags |= (1 << 6) if self.video else 0
        flags |= (1 << 7) if self.round else 0
        flags |= (1 << 8) if self.voice else 0
        flags |= (1 << 0) if self.document is not None else 0
        flags |= (1 << 5) if self.alt_documents else 0
        flags |= (1 << 9) if self.video_cover is not None else 0
        flags |= (1 << 10) if self.video_timestamp is not None else 0
        flags |= (1 << 2) if self.ttl_seconds is not None else 0
        b.write(Int(flags))
        
        if self.document is not None:
            b.write(self.document.write())
        
        if self.alt_documents:
            b.write(Vector(self.alt_documents))
        
        if self.video_cover is not None:
            b.write(self.video_cover.write())
        
        if self.video_timestamp is not None:
            b.write(Int(self.video_timestamp))
        
        if self.ttl_seconds is not None:
            b.write(Int(self.ttl_seconds))
        
        return b.getvalue()
