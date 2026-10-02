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


class ToggleWebBrowserSettingsException(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``60ED4229``

    Parameters:
        url (``str``):
            N/A

        delete (``bool``, *optional*):
            N/A

        open_external_browser (``bool``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["url", "delete", "open_external_browser"]

    ID = 0x60ed4229
    QUALNAME = "functions.account.ToggleWebBrowserSettingsException"

    def __init__(self, *, url: str, delete: Optional[bool] = None, open_external_browser: Optional[bool] = None) -> None:
        self.url = url  # string
        self.delete = delete  # flags.1?true
        self.open_external_browser = open_external_browser  # flags.0?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ToggleWebBrowserSettingsException":
        
        flags = Int.read(b)
        
        delete = True if flags & (1 << 1) else False
        open_external_browser = Bool.read(b) if flags & (1 << 0) else None
        url = String.read(b)
        
        return ToggleWebBrowserSettingsException(url=url, delete=delete, open_external_browser=open_external_browser)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.delete else 0
        flags |= (1 << 0) if self.open_external_browser is not None else 0
        b.write(Int(flags))
        
        if self.open_external_browser is not None:
            b.write(Bool(self.open_external_browser))
        
        b.write(String(self.url))
        
        return b.getvalue()
