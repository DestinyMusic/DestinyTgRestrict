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


class RequestWebViewButton(TLObject["raw.base.bots.RequestedButton"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``31A2A35E``

    Parameters:
        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        button (:obj:`KeyboardButton <pyrogram.raw.base.KeyboardButton>`):
            N/A

    Returns:
        :obj:`bots.RequestedButton <pyrogram.raw.base.bots.RequestedButton>`
    """

    __slots__: List[str] = ["user_id", "button"]

    ID = 0x31a2a35e
    QUALNAME = "functions.bots.RequestWebViewButton"

    def __init__(self, *, user_id: "raw.base.InputUser", button: "raw.base.KeyboardButton") -> None:
        self.user_id = user_id  # InputUser
        self.button = button  # KeyboardButton

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RequestWebViewButton":
        # No flags
        
        user_id = TLObject.read(b)
        
        button = TLObject.read(b)
        
        return RequestWebViewButton(user_id=user_id, button=button)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(self.button.write())
        
        return b.getvalue()
