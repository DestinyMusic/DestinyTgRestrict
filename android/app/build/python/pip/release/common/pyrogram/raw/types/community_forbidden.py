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


class CommunityForbidden(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Chat`.

    Details:
        - Layer: ``228``
        - ID: ``FD3CDAB8``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        title (``str``):
            N/A

        access_hash (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "title", "access_hash"]

    ID = 0xfd3cdab8
    QUALNAME = "types.CommunityForbidden"

    def __init__(self, *, id: int, title: str, access_hash: Optional[int] = None) -> None:
        self.id = id  # long
        self.title = title  # string
        self.access_hash = access_hash  # flags.13?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CommunityForbidden":
        
        flags = Int.read(b)
        
        id = Long.read(b)
        
        access_hash = Long.read(b) if flags & (1 << 13) else None
        title = String.read(b)
        
        return CommunityForbidden(id=id, title=title, access_hash=access_hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 13) if self.access_hash is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.id))
        
        if self.access_hash is not None:
            b.write(Long(self.access_hash))
        
        b.write(String(self.title))
        
        return b.getvalue()
