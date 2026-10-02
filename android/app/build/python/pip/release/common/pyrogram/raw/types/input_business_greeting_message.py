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


class InputBusinessGreetingMessage(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputBusinessGreetingMessage`.

    Details:
        - Layer: ``228``
        - ID: ``194CB3B``

    Parameters:
        shortcut_id (``int`` ``32-bit``):
            N/A

        recipients (:obj:`InputBusinessRecipients <pyrogram.raw.base.InputBusinessRecipients>`):
            N/A

        no_activity_days (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["shortcut_id", "recipients", "no_activity_days"]

    ID = 0x194cb3b
    QUALNAME = "types.InputBusinessGreetingMessage"

    def __init__(self, *, shortcut_id: int, recipients: "raw.base.InputBusinessRecipients", no_activity_days: int) -> None:
        self.shortcut_id = shortcut_id  # int
        self.recipients = recipients  # InputBusinessRecipients
        self.no_activity_days = no_activity_days  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputBusinessGreetingMessage":
        # No flags
        
        shortcut_id = Int.read(b)
        
        recipients = TLObject.read(b)
        
        no_activity_days = Int.read(b)
        
        return InputBusinessGreetingMessage(shortcut_id=shortcut_id, recipients=recipients, no_activity_days=no_activity_days)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.shortcut_id))
        
        b.write(self.recipients.write())
        
        b.write(Int(self.no_activity_days))
        
        return b.getvalue()
