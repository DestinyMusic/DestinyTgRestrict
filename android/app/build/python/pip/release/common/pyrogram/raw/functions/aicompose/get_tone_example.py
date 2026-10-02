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


class GetToneExample(TLObject["raw.base.AiComposeToneExample"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``D1B4AB14``

    Parameters:
        tone (:obj:`InputAiComposeTone <pyrogram.raw.base.InputAiComposeTone>`):
            N/A

        num (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`AiComposeToneExample <pyrogram.raw.base.AiComposeToneExample>`
    """

    __slots__: List[str] = ["tone", "num"]

    ID = 0xd1b4ab14
    QUALNAME = "functions.aicompose.GetToneExample"

    def __init__(self, *, tone: "raw.base.InputAiComposeTone", num: int) -> None:
        self.tone = tone  # InputAiComposeTone
        self.num = num  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetToneExample":
        # No flags
        
        tone = TLObject.read(b)
        
        num = Int.read(b)
        
        return GetToneExample(tone=tone, num=num)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.tone.write())
        
        b.write(Int(self.num))
        
        return b.getvalue()
