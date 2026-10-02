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


class InputPollAnswer(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PollAnswer`.

    Details:
        - Layer: ``228``
        - ID: ``199FED96``

    Parameters:
        text (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["text", "media"]

    ID = 0x199fed96
    QUALNAME = "types.InputPollAnswer"

    def __init__(self, *, text: "raw.base.TextWithEntities", media: "raw.base.InputMedia" = None) -> None:
        self.text = text  # TextWithEntities
        self.media = media  # flags.0?InputMedia

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPollAnswer":
        
        flags = Int.read(b)
        
        text = TLObject.read(b)
        
        media = TLObject.read(b) if flags & (1 << 0) else None
        
        return InputPollAnswer(text=text, media=media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.media is not None else 0
        b.write(Int(flags))
        
        b.write(self.text.write())
        
        if self.media is not None:
            b.write(self.media.write())
        
        return b.getvalue()
