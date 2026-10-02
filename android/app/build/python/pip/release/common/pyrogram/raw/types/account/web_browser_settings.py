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


class WebBrowserSettings(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.account.WebBrowserSettings`.

    Details:
        - Layer: ``228``
        - ID: ``79EB8CB3``

    Parameters:
        external_exceptions (List of :obj:`WebDomainException <pyrogram.raw.base.WebDomainException>`):
            N/A

        inapp_exceptions (List of :obj:`WebDomainException <pyrogram.raw.base.WebDomainException>`):
            N/A

        hash (``int`` ``64-bit``):
            N/A

        open_external_browser (``bool``, *optional*):
            N/A

        display_close_button (``bool``, *optional*):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetWebBrowserSettings
            account.UpdateWebBrowserSettings
            account.DeleteWebBrowserSettingsExceptions
    """

    __slots__: List[str] = ["external_exceptions", "inapp_exceptions", "hash", "open_external_browser", "display_close_button"]

    ID = 0x79eb8cb3
    QUALNAME = "types.account.WebBrowserSettings"

    def __init__(self, *, external_exceptions: List["raw.base.WebDomainException"], inapp_exceptions: List["raw.base.WebDomainException"], hash: int, open_external_browser: Optional[bool] = None, display_close_button: Optional[bool] = None) -> None:
        self.external_exceptions = external_exceptions  # Vector<WebDomainException>
        self.inapp_exceptions = inapp_exceptions  # Vector<WebDomainException>
        self.hash = hash  # long
        self.open_external_browser = open_external_browser  # flags.0?true
        self.display_close_button = display_close_button  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebBrowserSettings":
        
        flags = Int.read(b)
        
        open_external_browser = True if flags & (1 << 0) else False
        display_close_button = True if flags & (1 << 1) else False
        external_exceptions = TLObject.read(b)
        
        inapp_exceptions = TLObject.read(b)
        
        hash = Long.read(b)
        
        return WebBrowserSettings(external_exceptions=external_exceptions, inapp_exceptions=inapp_exceptions, hash=hash, open_external_browser=open_external_browser, display_close_button=display_close_button)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.open_external_browser else 0
        flags |= (1 << 1) if self.display_close_button else 0
        b.write(Int(flags))
        
        b.write(Vector(self.external_exceptions))
        
        b.write(Vector(self.inapp_exceptions))
        
        b.write(Long(self.hash))
        
        return b.getvalue()
