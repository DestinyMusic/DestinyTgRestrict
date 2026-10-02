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


class RequestChatJoinWebView(TLObject["raw.base.WebViewResult"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``BA9EE679``

    Parameters:
        query_id (``int`` ``64-bit``):
            N/A

        platform (``str``):
            N/A

        theme_params (:obj:`DataJSON <pyrogram.raw.base.DataJSON>`, *optional*):
            N/A

    Returns:
        :obj:`WebViewResult <pyrogram.raw.base.WebViewResult>`
    """

    __slots__: List[str] = ["query_id", "platform", "theme_params"]

    ID = 0xba9ee679
    QUALNAME = "functions.messages.RequestChatJoinWebView"

    def __init__(self, *, query_id: int, platform: str, theme_params: "raw.base.DataJSON" = None) -> None:
        self.query_id = query_id  # long
        self.platform = platform  # string
        self.theme_params = theme_params  # flags.0?DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RequestChatJoinWebView":
        
        flags = Int.read(b)
        
        query_id = Long.read(b)
        
        theme_params = TLObject.read(b) if flags & (1 << 0) else None
        
        platform = String.read(b)
        
        return RequestChatJoinWebView(query_id=query_id, platform=platform, theme_params=theme_params)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.theme_params is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.query_id))
        
        if self.theme_params is not None:
            b.write(self.theme_params.write())
        
        b.write(String(self.platform))
        
        return b.getvalue()
