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


class BotVerification(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.BotVerification`.

    Details:
        - Layer: ``228``
        - ID: ``F93CD45C``

    Parameters:
        bot_id (``int`` ``64-bit``):
            N/A

        icon (``int`` ``64-bit``):
            N/A

        description (``str``):
            N/A

    """

    __slots__: List[str] = ["bot_id", "icon", "description"]

    ID = 0xf93cd45c
    QUALNAME = "types.BotVerification"

    def __init__(self, *, bot_id: int, icon: int, description: str) -> None:
        self.bot_id = bot_id  # long
        self.icon = icon  # long
        self.description = description  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotVerification":
        # No flags
        
        bot_id = Long.read(b)
        
        icon = Long.read(b)
        
        description = String.read(b)
        
        return BotVerification(bot_id=bot_id, icon=icon, description=description)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.bot_id))
        
        b.write(Long(self.icon))
        
        b.write(String(self.description))
        
        return b.getvalue()
