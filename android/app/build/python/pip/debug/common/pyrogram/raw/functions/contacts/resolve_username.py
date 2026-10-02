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


class ResolveUsername(TLObject["raw.base.contacts.ResolvedPeer"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``725AFBBC``

    Parameters:
        username (``str``):
            N/A

        referer (``str``, *optional*):
            N/A

    Returns:
        :obj:`contacts.ResolvedPeer <pyrogram.raw.base.contacts.ResolvedPeer>`
    """

    __slots__: List[str] = ["username", "referer"]

    ID = 0x725afbbc
    QUALNAME = "functions.contacts.ResolveUsername"

    def __init__(self, *, username: str, referer: Optional[str] = None) -> None:
        self.username = username  # string
        self.referer = referer  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ResolveUsername":
        
        flags = Int.read(b)
        
        username = String.read(b)
        
        referer = String.read(b) if flags & (1 << 0) else None
        return ResolveUsername(username=username, referer=referer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.referer is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.username))
        
        if self.referer is not None:
            b.write(String(self.referer))
        
        return b.getvalue()
