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


class EditAccessSettings(TLObject["raw.base.Bool"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``31813CD8``

    Parameters:
        bot (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        restricted (``bool``, *optional*):
            N/A

        add_users (List of :obj:`InputUser <pyrogram.raw.base.InputUser>`, *optional*):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["bot", "restricted", "add_users"]

    ID = 0x31813cd8
    QUALNAME = "functions.bots.EditAccessSettings"

    def __init__(self, *, bot: "raw.base.InputUser", restricted: Optional[bool] = None, add_users: Optional[List["raw.base.InputUser"]] = None) -> None:
        self.bot = bot  # InputUser
        self.restricted = restricted  # flags.0?true
        self.add_users = add_users  # flags.1?Vector<InputUser>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditAccessSettings":
        
        flags = Int.read(b)
        
        restricted = True if flags & (1 << 0) else False
        bot = TLObject.read(b)
        
        add_users = TLObject.read(b) if flags & (1 << 1) else []
        
        return EditAccessSettings(bot=bot, restricted=restricted, add_users=add_users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.restricted else 0
        flags |= (1 << 1) if self.add_users else 0
        b.write(Int(flags))
        
        b.write(self.bot.write())
        
        if self.add_users:
            b.write(Vector(self.add_users))
        
        return b.getvalue()
