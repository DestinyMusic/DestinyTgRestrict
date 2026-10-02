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


class ChatThemeUniqueGift(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.ChatTheme`.

    Details:
        - Layer: ``228``
        - ID: ``3458F9C8``

    Parameters:
        gift (:obj:`StarGift <pyrogram.raw.base.StarGift>`):
            N/A

        theme_settings (List of :obj:`ThemeSettings <pyrogram.raw.base.ThemeSettings>`):
            N/A

    """

    __slots__: List[str] = ["gift", "theme_settings"]

    ID = 0x3458f9c8
    QUALNAME = "types.ChatThemeUniqueGift"

    def __init__(self, *, gift: "raw.base.StarGift", theme_settings: List["raw.base.ThemeSettings"]) -> None:
        self.gift = gift  # StarGift
        self.theme_settings = theme_settings  # Vector<ThemeSettings>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatThemeUniqueGift":
        # No flags
        
        gift = TLObject.read(b)
        
        theme_settings = TLObject.read(b)
        
        return ChatThemeUniqueGift(gift=gift, theme_settings=theme_settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.gift.write())
        
        b.write(Vector(self.theme_settings))
        
        return b.getvalue()
