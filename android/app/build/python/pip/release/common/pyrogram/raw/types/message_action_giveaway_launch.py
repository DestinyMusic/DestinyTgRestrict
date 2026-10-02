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


class MessageActionGiveawayLaunch(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``A80F51E4``

    Parameters:
        stars (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["stars"]

    ID = 0xa80f51e4
    QUALNAME = "types.MessageActionGiveawayLaunch"

    def __init__(self, *, stars: Optional[int] = None) -> None:
        self.stars = stars  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionGiveawayLaunch":
        
        flags = Int.read(b)
        
        stars = Long.read(b) if flags & (1 << 0) else None
        return MessageActionGiveawayLaunch(stars=stars)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.stars is not None else 0
        b.write(Int(flags))
        
        if self.stars is not None:
            b.write(Long(self.stars))
        
        return b.getvalue()
