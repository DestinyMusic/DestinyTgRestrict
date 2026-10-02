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


class ComposedRichMessageWithAI(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.messages.ComposedRichMessageWithAI`.

    Details:
        - Layer: ``228``
        - ID: ``4C4537C8``

    Parameters:
        result (:obj:`RichMessage <pyrogram.raw.base.RichMessage>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.ComposeRichMessageWithAI
    """

    __slots__: List[str] = ["result"]

    ID = 0x4c4537c8
    QUALNAME = "types.messages.ComposedRichMessageWithAI"

    def __init__(self, *, result: "raw.base.RichMessage") -> None:
        self.result = result  # RichMessage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ComposedRichMessageWithAI":
        # No flags
        
        result = TLObject.read(b)
        
        return ComposedRichMessageWithAI(result=result)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.result.write())
        
        return b.getvalue()
