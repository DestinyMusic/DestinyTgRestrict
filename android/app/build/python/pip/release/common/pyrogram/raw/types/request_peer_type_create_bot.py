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


class RequestPeerTypeCreateBot(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.RequestPeerType`.

    Details:
        - Layer: ``228``
        - ID: ``3E81E078``

    Parameters:
        bot_managed (``bool``, *optional*):
            N/A

        suggested_name (``str``, *optional*):
            N/A

        suggested_username (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["bot_managed", "suggested_name", "suggested_username"]

    ID = 0x3e81e078
    QUALNAME = "types.RequestPeerTypeCreateBot"

    def __init__(self, *, bot_managed: Optional[bool] = None, suggested_name: Optional[str] = None, suggested_username: Optional[str] = None) -> None:
        self.bot_managed = bot_managed  # flags.0?true
        self.suggested_name = suggested_name  # flags.1?string
        self.suggested_username = suggested_username  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RequestPeerTypeCreateBot":
        
        flags = Int.read(b)
        
        bot_managed = True if flags & (1 << 0) else False
        suggested_name = String.read(b) if flags & (1 << 1) else None
        suggested_username = String.read(b) if flags & (1 << 2) else None
        return RequestPeerTypeCreateBot(bot_managed=bot_managed, suggested_name=suggested_name, suggested_username=suggested_username)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.bot_managed else 0
        flags |= (1 << 1) if self.suggested_name is not None else 0
        flags |= (1 << 2) if self.suggested_username is not None else 0
        b.write(Int(flags))
        
        if self.suggested_name is not None:
            b.write(String(self.suggested_name))
        
        if self.suggested_username is not None:
            b.write(String(self.suggested_username))
        
        return b.getvalue()
