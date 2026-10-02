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


class InputRichMessageMarkdown(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputRichMessage`.

    Details:
        - Layer: ``228``
        - ID: ``4B572C``

    Parameters:
        markdown (``str``):
            N/A

        rtl (``bool``, *optional*):
            N/A

        noautolink (``bool``, *optional*):
            N/A

        files (List of :obj:`InputRichFile <pyrogram.raw.base.InputRichFile>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["markdown", "rtl", "noautolink", "files"]

    ID = 0x4b572c
    QUALNAME = "types.InputRichMessageMarkdown"

    def __init__(self, *, markdown: str, rtl: Optional[bool] = None, noautolink: Optional[bool] = None, files: Optional[List["raw.base.InputRichFile"]] = None) -> None:
        self.markdown = markdown  # string
        self.rtl = rtl  # flags.0?true
        self.noautolink = noautolink  # flags.1?true
        self.files = files  # flags.2?Vector<InputRichFile>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputRichMessageMarkdown":
        
        flags = Int.read(b)
        
        rtl = True if flags & (1 << 0) else False
        noautolink = True if flags & (1 << 1) else False
        markdown = String.read(b)
        
        files = TLObject.read(b) if flags & (1 << 2) else []
        
        return InputRichMessageMarkdown(markdown=markdown, rtl=rtl, noautolink=noautolink, files=files)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.rtl else 0
        flags |= (1 << 1) if self.noautolink else 0
        flags |= (1 << 2) if self.files else 0
        b.write(Int(flags))
        
        b.write(String(self.markdown))
        
        if self.files:
            b.write(Vector(self.files))
        
        return b.getvalue()
