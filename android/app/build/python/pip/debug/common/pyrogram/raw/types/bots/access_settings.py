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


class AccessSettings(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.bots.AccessSettings`.

    Details:
        - Layer: ``228``
        - ID: ``DD1FBF93``

    Parameters:
        restricted (``bool``, *optional*):
            N/A

        add_users (List of :obj:`User <pyrogram.raw.base.User>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            bots.GetAccessSettings
    """

    __slots__: List[str] = ["restricted", "add_users"]

    ID = 0xdd1fbf93
    QUALNAME = "types.bots.AccessSettings"

    def __init__(self, *, restricted: Optional[bool] = None, add_users: Optional[List["raw.base.User"]] = None) -> None:
        self.restricted = restricted  # flags.0?true
        self.add_users = add_users  # flags.1?Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AccessSettings":
        
        flags = Int.read(b)
        
        restricted = True if flags & (1 << 0) else False
        add_users = TLObject.read(b) if flags & (1 << 1) else []
        
        return AccessSettings(restricted=restricted, add_users=add_users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.restricted else 0
        flags |= (1 << 1) if self.add_users else 0
        b.write(Int(flags))
        
        if self.add_users:
            b.write(Vector(self.add_users))
        
        return b.getvalue()
