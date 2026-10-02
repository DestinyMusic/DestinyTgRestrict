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


class UpdateBotEditBusinessMessage(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``7DF587C``

    Parameters:
        connection_id (``str``):
            N/A

        message (:obj:`Message <pyrogram.raw.base.Message>`):
            N/A

        qts (``int`` ``32-bit``):
            N/A

        reply_to_message (:obj:`Message <pyrogram.raw.base.Message>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["connection_id", "message", "qts", "reply_to_message"]

    ID = 0x7df587c
    QUALNAME = "types.UpdateBotEditBusinessMessage"

    def __init__(self, *, connection_id: str, message: "raw.base.Message", qts: int, reply_to_message: "raw.base.Message" = None) -> None:
        self.connection_id = connection_id  # string
        self.message = message  # Message
        self.qts = qts  # int
        self.reply_to_message = reply_to_message  # flags.0?Message

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotEditBusinessMessage":
        
        flags = Int.read(b)
        
        connection_id = String.read(b)
        
        message = TLObject.read(b)
        
        reply_to_message = TLObject.read(b) if flags & (1 << 0) else None
        
        qts = Int.read(b)
        
        return UpdateBotEditBusinessMessage(connection_id=connection_id, message=message, qts=qts, reply_to_message=reply_to_message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.reply_to_message is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.connection_id))
        
        b.write(self.message.write())
        
        if self.reply_to_message is not None:
            b.write(self.reply_to_message.write())
        
        b.write(Int(self.qts))
        
        return b.getvalue()
