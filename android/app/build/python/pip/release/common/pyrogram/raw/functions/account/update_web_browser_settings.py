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


class UpdateWebBrowserSettings(TLObject["raw.base.account.WebBrowserSettings"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``9ADF82FE``

    Parameters:
        open_external_browser (``bool``, *optional*):
            N/A

        display_close_button (``bool``, *optional*):
            N/A

    Returns:
        :obj:`account.WebBrowserSettings <pyrogram.raw.base.account.WebBrowserSettings>`
    """

    __slots__: List[str] = ["open_external_browser", "display_close_button"]

    ID = 0x9adf82fe
    QUALNAME = "functions.account.UpdateWebBrowserSettings"

    def __init__(self, *, open_external_browser: Optional[bool] = None, display_close_button: Optional[bool] = None) -> None:
        self.open_external_browser = open_external_browser  # flags.0?true
        self.display_close_button = display_close_button  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateWebBrowserSettings":
        
        flags = Int.read(b)
        
        open_external_browser = True if flags & (1 << 0) else False
        display_close_button = True if flags & (1 << 1) else False
        return UpdateWebBrowserSettings(open_external_browser=open_external_browser, display_close_button=display_close_button)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.open_external_browser else 0
        flags |= (1 << 1) if self.display_close_button else 0
        b.write(Int(flags))
        
        return b.getvalue()
