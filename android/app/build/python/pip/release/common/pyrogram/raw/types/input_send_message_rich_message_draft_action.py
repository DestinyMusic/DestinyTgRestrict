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


class InputSendMessageRichMessageDraftAction(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.SendMessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``E2B23B51``

    Parameters:
        random_id (``int`` ``64-bit``):
            N/A

        rich_message (:obj:`InputRichMessage <pyrogram.raw.base.InputRichMessage>`):
            N/A

    """

    __slots__: List[str] = ["random_id", "rich_message"]

    ID = 0xe2b23b51
    QUALNAME = "types.InputSendMessageRichMessageDraftAction"

    def __init__(self, *, random_id: int, rich_message: "raw.base.InputRichMessage") -> None:
        self.random_id = random_id  # long
        self.rich_message = rich_message  # InputRichMessage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputSendMessageRichMessageDraftAction":
        # No flags
        
        random_id = Long.read(b)
        
        rich_message = TLObject.read(b)
        
        return InputSendMessageRichMessageDraftAction(random_id=random_id, rich_message=rich_message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.random_id))
        
        b.write(self.rich_message.write())
        
        return b.getvalue()
