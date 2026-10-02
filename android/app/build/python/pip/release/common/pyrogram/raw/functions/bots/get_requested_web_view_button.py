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


class GetRequestedWebViewButton(TLObject["raw.base.KeyboardButton"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``BF25B7F3``

    Parameters:
        bot (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        webapp_req_id (``str``):
            N/A

    Returns:
        :obj:`KeyboardButton <pyrogram.raw.base.KeyboardButton>`
    """

    __slots__: List[str] = ["bot", "webapp_req_id"]

    ID = 0xbf25b7f3
    QUALNAME = "functions.bots.GetRequestedWebViewButton"

    def __init__(self, *, bot: "raw.base.InputUser", webapp_req_id: str) -> None:
        self.bot = bot  # InputUser
        self.webapp_req_id = webapp_req_id  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetRequestedWebViewButton":
        # No flags
        
        bot = TLObject.read(b)
        
        webapp_req_id = String.read(b)
        
        return GetRequestedWebViewButton(bot=bot, webapp_req_id=webapp_req_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.bot.write())
        
        b.write(String(self.webapp_req_id))
        
        return b.getvalue()
