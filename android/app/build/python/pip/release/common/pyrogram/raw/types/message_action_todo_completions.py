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


class MessageActionTodoCompletions(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``CC7C5C89``

    Parameters:
        completed (List of ``int`` ``32-bit``):
            N/A

        incompleted (List of ``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["completed", "incompleted"]

    ID = 0xcc7c5c89
    QUALNAME = "types.MessageActionTodoCompletions"

    def __init__(self, *, completed: List[int], incompleted: List[int]) -> None:
        self.completed = completed  # Vector<int>
        self.incompleted = incompleted  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionTodoCompletions":
        # No flags
        
        completed = TLObject.read(b, Int)
        
        incompleted = TLObject.read(b, Int)
        
        return MessageActionTodoCompletions(completed=completed, incompleted=incompleted)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.completed, Int))
        
        b.write(Vector(self.incompleted, Int))
        
        return b.getvalue()
