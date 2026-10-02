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


class CreateBot(TLObject["raw.base.User"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``E5B17F2B``

    Parameters:
        name (``str``):
            N/A

        username (``str``):
            N/A

        manager_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        via_deeplink (``bool``, *optional*):
            N/A

    Returns:
        :obj:`User <pyrogram.raw.base.User>`
    """

    __slots__: List[str] = ["name", "username", "manager_id", "via_deeplink"]

    ID = 0xe5b17f2b
    QUALNAME = "functions.bots.CreateBot"

    def __init__(self, *, name: str, username: str, manager_id: "raw.base.InputUser", via_deeplink: Optional[bool] = None) -> None:
        self.name = name  # string
        self.username = username  # string
        self.manager_id = manager_id  # InputUser
        self.via_deeplink = via_deeplink  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CreateBot":
        
        flags = Int.read(b)
        
        via_deeplink = True if flags & (1 << 0) else False
        name = String.read(b)
        
        username = String.read(b)
        
        manager_id = TLObject.read(b)
        
        return CreateBot(name=name, username=username, manager_id=manager_id, via_deeplink=via_deeplink)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.via_deeplink else 0
        b.write(Int(flags))
        
        b.write(String(self.name))
        
        b.write(String(self.username))
        
        b.write(self.manager_id.write())
        
        return b.getvalue()
