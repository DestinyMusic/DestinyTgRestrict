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


class Status(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.smsjobs.Status`.

    Details:
        - Layer: ``228``
        - ID: ``2AEE9191``

    Parameters:
        recent_sent (``int`` ``32-bit``):
            N/A

        recent_since (``int`` ``32-bit``):
            N/A

        recent_remains (``int`` ``32-bit``):
            N/A

        total_sent (``int`` ``32-bit``):
            N/A

        total_since (``int`` ``32-bit``):
            N/A

        terms_url (``str``):
            N/A

        allow_international (``bool``, *optional*):
            N/A

        last_gift_slug (``str``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            smsjobs.GetStatus
    """

    __slots__: List[str] = ["recent_sent", "recent_since", "recent_remains", "total_sent", "total_since", "terms_url", "allow_international", "last_gift_slug"]

    ID = 0x2aee9191
    QUALNAME = "types.smsjobs.Status"

    def __init__(self, *, recent_sent: int, recent_since: int, recent_remains: int, total_sent: int, total_since: int, terms_url: str, allow_international: Optional[bool] = None, last_gift_slug: Optional[str] = None) -> None:
        self.recent_sent = recent_sent  # int
        self.recent_since = recent_since  # int
        self.recent_remains = recent_remains  # int
        self.total_sent = total_sent  # int
        self.total_since = total_since  # int
        self.terms_url = terms_url  # string
        self.allow_international = allow_international  # flags.0?true
        self.last_gift_slug = last_gift_slug  # flags.1?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Status":
        
        flags = Int.read(b)
        
        allow_international = True if flags & (1 << 0) else False
        recent_sent = Int.read(b)
        
        recent_since = Int.read(b)
        
        recent_remains = Int.read(b)
        
        total_sent = Int.read(b)
        
        total_since = Int.read(b)
        
        last_gift_slug = String.read(b) if flags & (1 << 1) else None
        terms_url = String.read(b)
        
        return Status(recent_sent=recent_sent, recent_since=recent_since, recent_remains=recent_remains, total_sent=total_sent, total_since=total_since, terms_url=terms_url, allow_international=allow_international, last_gift_slug=last_gift_slug)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.allow_international else 0
        flags |= (1 << 1) if self.last_gift_slug is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.recent_sent))
        
        b.write(Int(self.recent_since))
        
        b.write(Int(self.recent_remains))
        
        b.write(Int(self.total_sent))
        
        b.write(Int(self.total_since))
        
        if self.last_gift_slug is not None:
            b.write(String(self.last_gift_slug))
        
        b.write(String(self.terms_url))
        
        return b.getvalue()
