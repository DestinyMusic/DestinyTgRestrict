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


class CreateTone(TLObject["raw.base.AiComposeTone"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``4AA83913``

    Parameters:
        emoji_id (``int`` ``64-bit``):
            N/A

        title (``str``):
            N/A

        prompt (``str``):
            N/A

        display_author (``bool``, *optional*):
            N/A

    Returns:
        :obj:`AiComposeTone <pyrogram.raw.base.AiComposeTone>`
    """

    __slots__: List[str] = ["emoji_id", "title", "prompt", "display_author"]

    ID = 0x4aa83913
    QUALNAME = "functions.aicompose.CreateTone"

    def __init__(self, *, emoji_id: int, title: str, prompt: str, display_author: Optional[bool] = None) -> None:
        self.emoji_id = emoji_id  # long
        self.title = title  # string
        self.prompt = prompt  # string
        self.display_author = display_author  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CreateTone":
        
        flags = Int.read(b)
        
        display_author = True if flags & (1 << 0) else False
        emoji_id = Long.read(b)
        
        title = String.read(b)
        
        prompt = String.read(b)
        
        return CreateTone(emoji_id=emoji_id, title=title, prompt=prompt, display_author=display_author)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.display_author else 0
        b.write(Int(flags))
        
        b.write(Long(self.emoji_id))
        
        b.write(String(self.title))
        
        b.write(String(self.prompt))
        
        return b.getvalue()
