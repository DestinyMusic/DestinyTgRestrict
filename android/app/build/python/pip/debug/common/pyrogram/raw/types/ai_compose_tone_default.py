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


class AiComposeToneDefault(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.AiComposeTone`.

    Details:
        - Layer: ``228``
        - ID: ``9BAD6414``

    Parameters:
        tone (``str``):
            N/A

        emoji_id (``int`` ``64-bit``):
            N/A

        title (``str``):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            aicompose.CreateTone
            aicompose.UpdateTone
    """

    __slots__: List[str] = ["tone", "emoji_id", "title"]

    ID = 0x9bad6414
    QUALNAME = "types.AiComposeToneDefault"

    def __init__(self, *, tone: str, emoji_id: int, title: str) -> None:
        self.tone = tone  # string
        self.emoji_id = emoji_id  # long
        self.title = title  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AiComposeToneDefault":
        # No flags
        
        tone = String.read(b)
        
        emoji_id = Long.read(b)
        
        title = String.read(b)
        
        return AiComposeToneDefault(tone=tone, emoji_id=emoji_id, title=title)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.tone))
        
        b.write(Long(self.emoji_id))
        
        b.write(String(self.title))
        
        return b.getvalue()
