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


class PollAnswer(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PollAnswer`.

    Details:
        - Layer: ``228``
        - ID: ``4B7D786A``

    Parameters:
        text (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

        option (``bytes``):
            N/A

        media (:obj:`MessageMedia <pyrogram.raw.base.MessageMedia>`, *optional*):
            N/A

        added_by (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        date (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["text", "option", "media", "added_by", "date"]

    ID = 0x4b7d786a
    QUALNAME = "types.PollAnswer"

    def __init__(self, *, text: "raw.base.TextWithEntities", option: bytes, media: "raw.base.MessageMedia" = None, added_by: "raw.base.Peer" = None, date: Optional[int] = None) -> None:
        self.text = text  # TextWithEntities
        self.option = option  # bytes
        self.media = media  # flags.0?MessageMedia
        self.added_by = added_by  # flags.1?Peer
        self.date = date  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PollAnswer":
        
        flags = Int.read(b)
        
        text = TLObject.read(b)
        
        option = Bytes.read(b)
        
        media = TLObject.read(b) if flags & (1 << 0) else None
        
        added_by = TLObject.read(b) if flags & (1 << 1) else None
        
        date = Int.read(b) if flags & (1 << 1) else None
        return PollAnswer(text=text, option=option, media=media, added_by=added_by, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.media is not None else 0
        flags |= (1 << 1) if self.added_by is not None else 0
        flags |= (1 << 1) if self.date is not None else 0
        b.write(Int(flags))
        
        b.write(self.text.write())
        
        b.write(Bytes(self.option))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.added_by is not None:
            b.write(self.added_by.write())
        
        if self.date is not None:
            b.write(Int(self.date))
        
        return b.getvalue()
