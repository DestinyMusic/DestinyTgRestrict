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


class InputRichFilePhoto(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputRichFile`.

    Details:
        - Layer: ``228``
        - ID: ``9B00622B``

    Parameters:
        id (``str``):
            N/A

        photo (:obj:`InputPhoto <pyrogram.raw.base.InputPhoto>`):
            N/A

    """

    __slots__: List[str] = ["id", "photo"]

    ID = 0x9b00622b
    QUALNAME = "types.InputRichFilePhoto"

    def __init__(self, *, id: str, photo: "raw.base.InputPhoto") -> None:
        self.id = id  # string
        self.photo = photo  # InputPhoto

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputRichFilePhoto":
        # No flags
        
        id = String.read(b)
        
        photo = TLObject.read(b)
        
        return InputRichFilePhoto(id=id, photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(self.photo.write())
        
        return b.getvalue()
