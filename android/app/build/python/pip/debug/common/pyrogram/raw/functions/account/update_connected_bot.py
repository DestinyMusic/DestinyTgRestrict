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


class UpdateConnectedBot(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``66A08C7E``

    Parameters:
        bot (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        recipients (:obj:`InputBusinessBotRecipients <pyrogram.raw.base.InputBusinessBotRecipients>`):
            N/A

        deleted (``bool``, *optional*):
            N/A

        rights (:obj:`BusinessBotRights <pyrogram.raw.base.BusinessBotRights>`, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["bot", "recipients", "deleted", "rights"]

    ID = 0x66a08c7e
    QUALNAME = "functions.account.UpdateConnectedBot"

    def __init__(self, *, bot: "raw.base.InputUser", recipients: "raw.base.InputBusinessBotRecipients", deleted: Optional[bool] = None, rights: "raw.base.BusinessBotRights" = None) -> None:
        self.bot = bot  # InputUser
        self.recipients = recipients  # InputBusinessBotRecipients
        self.deleted = deleted  # flags.1?true
        self.rights = rights  # flags.0?BusinessBotRights

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateConnectedBot":
        
        flags = Int.read(b)
        
        deleted = True if flags & (1 << 1) else False
        rights = TLObject.read(b) if flags & (1 << 0) else None
        
        bot = TLObject.read(b)
        
        recipients = TLObject.read(b)
        
        return UpdateConnectedBot(bot=bot, recipients=recipients, deleted=deleted, rights=rights)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.deleted else 0
        flags |= (1 << 0) if self.rights is not None else 0
        b.write(Int(flags))
        
        if self.rights is not None:
            b.write(self.rights.write())
        
        b.write(self.bot.write())
        
        b.write(self.recipients.write())
        
        return b.getvalue()
