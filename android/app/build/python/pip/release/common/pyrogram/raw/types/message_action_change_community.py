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


class MessageActionChangeCommunity(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageAction`.

    Details:
        - Layer: ``228``
        - ID: ``5D20BAE8``

    Parameters:
        community_id (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["community_id"]

    ID = 0x5d20bae8
    QUALNAME = "types.MessageActionChangeCommunity"

    def __init__(self, *, community_id: Optional[int] = None) -> None:
        self.community_id = community_id  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionChangeCommunity":
        
        flags = Int.read(b)
        
        community_id = Long.read(b) if flags & (1 << 0) else None
        return MessageActionChangeCommunity(community_id=community_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.community_id is not None else 0
        b.write(Int(flags))
        
        if self.community_id is not None:
            b.write(Long(self.community_id))
        
        return b.getvalue()
