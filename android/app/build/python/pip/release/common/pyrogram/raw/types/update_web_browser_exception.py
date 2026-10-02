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


class UpdateWebBrowserException(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``140502D1``

    Parameters:
        exception (:obj:`WebDomainException <pyrogram.raw.base.WebDomainException>`):
            N/A

        delete (``bool``, *optional*):
            N/A

        open_external_browser (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["exception", "delete", "open_external_browser"]

    ID = 0x140502d1
    QUALNAME = "types.UpdateWebBrowserException"

    def __init__(self, *, exception: "raw.base.WebDomainException", delete: Optional[bool] = None, open_external_browser: Optional[bool] = None) -> None:
        self.exception = exception  # WebDomainException
        self.delete = delete  # flags.1?true
        self.open_external_browser = open_external_browser  # flags.0?Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateWebBrowserException":
        
        flags = Int.read(b)
        
        delete = True if flags & (1 << 1) else False
        open_external_browser = Bool.read(b) if flags & (1 << 0) else None
        exception = TLObject.read(b)
        
        return UpdateWebBrowserException(exception=exception, delete=delete, open_external_browser=open_external_browser)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.delete else 0
        flags |= (1 << 0) if self.open_external_browser is not None else 0
        b.write(Int(flags))
        
        if self.open_external_browser is not None:
            b.write(Bool(self.open_external_browser))
        
        b.write(self.exception.write())
        
        return b.getvalue()
