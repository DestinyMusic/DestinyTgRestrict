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


class PageListOrderedItemText(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PageListOrderedItem`.

    Details:
        - Layer: ``228``
        - ID: ``15031189``

    Parameters:
        text (:obj:`RichText <pyrogram.raw.base.RichText>`):
            N/A

        checkbox (``bool``, *optional*):
            N/A

        checked (``bool``, *optional*):
            N/A

        num (``str``, *optional*):
            N/A

        value (``int`` ``32-bit``, *optional*):
            N/A

        type (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["text", "checkbox", "checked", "num", "value", "type"]

    ID = 0x15031189
    QUALNAME = "types.PageListOrderedItemText"

    def __init__(self, *, text: "raw.base.RichText", checkbox: Optional[bool] = None, checked: Optional[bool] = None, num: Optional[str] = None, value: Optional[int] = None, type: Optional[str] = None) -> None:
        self.text = text  # RichText
        self.checkbox = checkbox  # flags.0?true
        self.checked = checked  # flags.1?true
        self.num = num  # flags.2?string
        self.value = value  # flags.3?int
        self.type = type  # flags.4?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageListOrderedItemText":
        
        flags = Int.read(b)
        
        checkbox = True if flags & (1 << 0) else False
        checked = True if flags & (1 << 1) else False
        num = String.read(b) if flags & (1 << 2) else None
        text = TLObject.read(b)
        
        value = Int.read(b) if flags & (1 << 3) else None
        type = String.read(b) if flags & (1 << 4) else None
        return PageListOrderedItemText(text=text, checkbox=checkbox, checked=checked, num=num, value=value, type=type)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.checkbox else 0
        flags |= (1 << 1) if self.checked else 0
        flags |= (1 << 2) if self.num is not None else 0
        flags |= (1 << 3) if self.value is not None else 0
        flags |= (1 << 4) if self.type is not None else 0
        b.write(Int(flags))
        
        if self.num is not None:
            b.write(String(self.num))
        
        b.write(self.text.write())
        
        if self.value is not None:
            b.write(Int(self.value))
        
        if self.type is not None:
            b.write(String(self.type))
        
        return b.getvalue()
