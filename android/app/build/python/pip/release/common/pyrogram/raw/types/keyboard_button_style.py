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


class KeyboardButtonStyle(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.KeyboardButtonStyle`.

    Details:
        - Layer: ``228``
        - ID: ``4FDD3430``

    Parameters:
        bg_primary (``bool``, *optional*):
            N/A

        bg_danger (``bool``, *optional*):
            N/A

        bg_success (``bool``, *optional*):
            N/A

        icon (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["bg_primary", "bg_danger", "bg_success", "icon"]

    ID = 0x4fdd3430
    QUALNAME = "types.KeyboardButtonStyle"

    def __init__(self, *, bg_primary: Optional[bool] = None, bg_danger: Optional[bool] = None, bg_success: Optional[bool] = None, icon: Optional[int] = None) -> None:
        self.bg_primary = bg_primary  # flags.0?true
        self.bg_danger = bg_danger  # flags.1?true
        self.bg_success = bg_success  # flags.2?true
        self.icon = icon  # flags.3?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "KeyboardButtonStyle":
        
        flags = Int.read(b)
        
        bg_primary = True if flags & (1 << 0) else False
        bg_danger = True if flags & (1 << 1) else False
        bg_success = True if flags & (1 << 2) else False
        icon = Long.read(b) if flags & (1 << 3) else None
        return KeyboardButtonStyle(bg_primary=bg_primary, bg_danger=bg_danger, bg_success=bg_success, icon=icon)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.bg_primary else 0
        flags |= (1 << 1) if self.bg_danger else 0
        flags |= (1 << 2) if self.bg_success else 0
        flags |= (1 << 3) if self.icon is not None else 0
        b.write(Int(flags))
        
        if self.icon is not None:
            b.write(Long(self.icon))
        
        return b.getvalue()
