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


class CheckSearchPostsFlood(TLObject["raw.base.SearchPostsFlood"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``22567115``

    Parameters:
        query (``str``, *optional*):
            N/A

    Returns:
        :obj:`SearchPostsFlood <pyrogram.raw.base.SearchPostsFlood>`
    """

    __slots__: List[str] = ["query"]

    ID = 0x22567115
    QUALNAME = "functions.channels.CheckSearchPostsFlood"

    def __init__(self, *, query: Optional[str] = None) -> None:
        self.query = query  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckSearchPostsFlood":
        
        flags = Int.read(b)
        
        query = String.read(b) if flags & (1 << 0) else None
        return CheckSearchPostsFlood(query=query)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.query is not None else 0
        b.write(Int(flags))
        
        if self.query is not None:
            b.write(String(self.query))
        
        return b.getvalue()
