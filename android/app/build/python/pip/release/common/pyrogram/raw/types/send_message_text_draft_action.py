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


class SendMessageTextDraftAction(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.SendMessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``376D975C``

    Parameters:
        random_id (``int`` ``64-bit``):
            N/A

        text (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

    """

    __slots__: List[str] = ["random_id", "text"]

    ID = 0x376d975c
    QUALNAME = "types.SendMessageTextDraftAction"

    def __init__(self, *, random_id: int, text: "raw.base.TextWithEntities") -> None:
        self.random_id = random_id  # long
        self.text = text  # TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMessageTextDraftAction":
        # No flags
        
        random_id = Long.read(b)
        
        text = TLObject.read(b)
        
        return SendMessageTextDraftAction(random_id=random_id, text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.random_id))
        
        b.write(self.text.write())
        
        return b.getvalue()
