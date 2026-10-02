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


class InputMediaWebPage(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputMedia`.

    Details:
        - Layer: ``228``
        - ID: ``C21B8849``

    Parameters:
        url (``str``):
            N/A

        force_large_media (``bool``, *optional*):
            N/A

        force_small_media (``bool``, *optional*):
            N/A

        optional (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["url", "force_large_media", "force_small_media", "optional"]

    ID = 0xc21b8849
    QUALNAME = "types.InputMediaWebPage"

    def __init__(self, *, url: str, force_large_media: Optional[bool] = None, force_small_media: Optional[bool] = None, optional: Optional[bool] = None) -> None:
        self.url = url  # string
        self.force_large_media = force_large_media  # flags.0?true
        self.force_small_media = force_small_media  # flags.1?true
        self.optional = optional  # flags.2?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMediaWebPage":
        
        flags = Int.read(b)
        
        force_large_media = True if flags & (1 << 0) else False
        force_small_media = True if flags & (1 << 1) else False
        optional = True if flags & (1 << 2) else False
        url = String.read(b)
        
        return InputMediaWebPage(url=url, force_large_media=force_large_media, force_small_media=force_small_media, optional=optional)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.force_large_media else 0
        flags |= (1 << 1) if self.force_small_media else 0
        flags |= (1 << 2) if self.optional else 0
        b.write(Int(flags))
        
        b.write(String(self.url))
        
        return b.getvalue()
