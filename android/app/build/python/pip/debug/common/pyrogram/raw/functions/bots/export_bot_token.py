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


class ExportBotToken(TLObject["raw.base.bots.ExportedBotToken"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``BD0D99EB``

    Parameters:
        bot (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        revoke (``bool``):
            N/A

    Returns:
        :obj:`bots.ExportedBotToken <pyrogram.raw.base.bots.ExportedBotToken>`
    """

    __slots__: List[str] = ["bot", "revoke"]

    ID = 0xbd0d99eb
    QUALNAME = "functions.bots.ExportBotToken"

    def __init__(self, *, bot: "raw.base.InputUser", revoke: bool) -> None:
        self.bot = bot  # InputUser
        self.revoke = revoke  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportBotToken":
        # No flags
        
        bot = TLObject.read(b)
        
        revoke = Bool.read(b)
        
        return ExportBotToken(bot=bot, revoke=revoke)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.bot.write())
        
        b.write(Bool(self.revoke))
        
        return b.getvalue()
