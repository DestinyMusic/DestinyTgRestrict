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


class RequestAppWebView(TLObject["raw.base.WebViewResult"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``53618BCE``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        app (:obj:`InputBotApp <pyrogram.raw.base.InputBotApp>`):
            N/A

        platform (``str``):
            N/A

        write_allowed (``bool``, *optional*):
            N/A

        compact (``bool``, *optional*):
            N/A

        fullscreen (``bool``, *optional*):
            N/A

        start_param (``str``, *optional*):
            N/A

        theme_params (:obj:`DataJSON <pyrogram.raw.base.DataJSON>`, *optional*):
            N/A

    Returns:
        :obj:`WebViewResult <pyrogram.raw.base.WebViewResult>`
    """

    __slots__: List[str] = ["peer", "app", "platform", "write_allowed", "compact", "fullscreen", "start_param", "theme_params"]

    ID = 0x53618bce
    QUALNAME = "functions.messages.RequestAppWebView"

    def __init__(self, *, peer: "raw.base.InputPeer", app: "raw.base.InputBotApp", platform: str, write_allowed: Optional[bool] = None, compact: Optional[bool] = None, fullscreen: Optional[bool] = None, start_param: Optional[str] = None, theme_params: "raw.base.DataJSON" = None) -> None:
        self.peer = peer  # InputPeer
        self.app = app  # InputBotApp
        self.platform = platform  # string
        self.write_allowed = write_allowed  # flags.0?true
        self.compact = compact  # flags.7?true
        self.fullscreen = fullscreen  # flags.8?true
        self.start_param = start_param  # flags.1?string
        self.theme_params = theme_params  # flags.2?DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RequestAppWebView":
        
        flags = Int.read(b)
        
        write_allowed = True if flags & (1 << 0) else False
        compact = True if flags & (1 << 7) else False
        fullscreen = True if flags & (1 << 8) else False
        peer = TLObject.read(b)
        
        app = TLObject.read(b)
        
        start_param = String.read(b) if flags & (1 << 1) else None
        theme_params = TLObject.read(b) if flags & (1 << 2) else None
        
        platform = String.read(b)
        
        return RequestAppWebView(peer=peer, app=app, platform=platform, write_allowed=write_allowed, compact=compact, fullscreen=fullscreen, start_param=start_param, theme_params=theme_params)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.write_allowed else 0
        flags |= (1 << 7) if self.compact else 0
        flags |= (1 << 8) if self.fullscreen else 0
        flags |= (1 << 1) if self.start_param is not None else 0
        flags |= (1 << 2) if self.theme_params is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(self.app.write())
        
        if self.start_param is not None:
            b.write(String(self.start_param))
        
        if self.theme_params is not None:
            b.write(self.theme_params.write())
        
        b.write(String(self.platform))
        
        return b.getvalue()
