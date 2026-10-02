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


class WebDomainException(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.WebDomainException`.

    Details:
        - Layer: ``228``
        - ID: ``933CA597``

    Parameters:
        domain (``str``):
            N/A

        url (``str``):
            N/A

        title (``str``):
            N/A

        favicon (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["domain", "url", "title", "favicon"]

    ID = 0x933ca597
    QUALNAME = "types.WebDomainException"

    def __init__(self, *, domain: str, url: str, title: str, favicon: Optional[int] = None) -> None:
        self.domain = domain  # string
        self.url = url  # string
        self.title = title  # string
        self.favicon = favicon  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebDomainException":
        
        flags = Int.read(b)
        
        domain = String.read(b)
        
        url = String.read(b)
        
        title = String.read(b)
        
        favicon = Long.read(b) if flags & (1 << 0) else None
        return WebDomainException(domain=domain, url=url, title=title, favicon=favicon)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.favicon is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.domain))
        
        b.write(String(self.url))
        
        b.write(String(self.title))
        
        if self.favicon is not None:
            b.write(Long(self.favicon))
        
        return b.getvalue()
