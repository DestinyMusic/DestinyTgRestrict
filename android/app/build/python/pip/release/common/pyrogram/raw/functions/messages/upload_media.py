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


class UploadMedia(TLObject["raw.base.MessageMedia"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``14967978``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`):
            N/A

        business_connection_id (``str``, *optional*):
            N/A

    Returns:
        :obj:`MessageMedia <pyrogram.raw.base.MessageMedia>`
    """

    __slots__: List[str] = ["peer", "media", "business_connection_id"]

    ID = 0x14967978
    QUALNAME = "functions.messages.UploadMedia"

    def __init__(self, *, peer: "raw.base.InputPeer", media: "raw.base.InputMedia", business_connection_id: Optional[str] = None) -> None:
        self.peer = peer  # InputPeer
        self.media = media  # InputMedia
        self.business_connection_id = business_connection_id  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UploadMedia":
        
        flags = Int.read(b)
        
        business_connection_id = String.read(b) if flags & (1 << 0) else None
        peer = TLObject.read(b)
        
        media = TLObject.read(b)
        
        return UploadMedia(peer=peer, media=media, business_connection_id=business_connection_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.business_connection_id is not None else 0
        b.write(Int(flags))
        
        if self.business_connection_id is not None:
            b.write(String(self.business_connection_id))
        
        b.write(self.peer.write())
        
        b.write(self.media.write())
        
        return b.getvalue()
