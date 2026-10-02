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


class EmojiStatus(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.EmojiStatus`.

    Details:
        - Layer: ``228``
        - ID: ``E7FF068A``

    Parameters:
        document_id (``int`` ``64-bit``):
            N/A

        until (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["document_id", "until"]

    ID = 0xe7ff068a
    QUALNAME = "types.EmojiStatus"

    def __init__(self, *, document_id: int, until: Optional[int] = None) -> None:
        self.document_id = document_id  # long
        self.until = until  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiStatus":
        
        flags = Int.read(b)
        
        document_id = Long.read(b)
        
        until = Int.read(b) if flags & (1 << 0) else None
        return EmojiStatus(document_id=document_id, until=until)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.until is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.document_id))
        
        if self.until is not None:
            b.write(Int(self.until))
        
        return b.getvalue()
