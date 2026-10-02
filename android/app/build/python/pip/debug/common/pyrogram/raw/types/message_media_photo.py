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


class MessageMediaPhoto(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageMedia`.

    Details:
        - Layer: ``228``
        - ID: ``E216EB63``

    Parameters:
        spoiler (``bool``, *optional*):
            N/A

        live_photo (``bool``, *optional*):
            N/A

        photo (:obj:`Photo <pyrogram.raw.base.Photo>`, *optional*):
            N/A

        ttl_seconds (``int`` ``32-bit``, *optional*):
            N/A

        video (:obj:`Document <pyrogram.raw.base.Document>`, *optional*):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.UploadMedia
            messages.UploadImportedMedia
    """

    __slots__: List[str] = ["spoiler", "live_photo", "photo", "ttl_seconds", "video"]

    ID = 0xe216eb63
    QUALNAME = "types.MessageMediaPhoto"

    def __init__(self, *, spoiler: Optional[bool] = None, live_photo: Optional[bool] = None, photo: "raw.base.Photo" = None, ttl_seconds: Optional[int] = None, video: "raw.base.Document" = None) -> None:
        self.spoiler = spoiler  # flags.3?true
        self.live_photo = live_photo  # flags.4?true
        self.photo = photo  # flags.0?Photo
        self.ttl_seconds = ttl_seconds  # flags.2?int
        self.video = video  # flags.4?Document

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaPhoto":
        
        flags = Int.read(b)
        
        spoiler = True if flags & (1 << 3) else False
        live_photo = True if flags & (1 << 4) else False
        photo = TLObject.read(b) if flags & (1 << 0) else None
        
        ttl_seconds = Int.read(b) if flags & (1 << 2) else None
        video = TLObject.read(b) if flags & (1 << 4) else None
        
        return MessageMediaPhoto(spoiler=spoiler, live_photo=live_photo, photo=photo, ttl_seconds=ttl_seconds, video=video)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.spoiler else 0
        flags |= (1 << 4) if self.live_photo else 0
        flags |= (1 << 0) if self.photo is not None else 0
        flags |= (1 << 2) if self.ttl_seconds is not None else 0
        flags |= (1 << 4) if self.video is not None else 0
        b.write(Int(flags))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        if self.ttl_seconds is not None:
            b.write(Int(self.ttl_seconds))
        
        if self.video is not None:
            b.write(self.video.write())
        
        return b.getvalue()
