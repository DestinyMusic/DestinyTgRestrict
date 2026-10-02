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


class RecentStory(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.RecentStory`.

    Details:
        - Layer: ``228``
        - ID: ``711D692D``

    Parameters:
        live (``bool``, *optional*):
            N/A

        max_id (``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            stories.GetPeerMaxIDs
    """

    __slots__: List[str] = ["live", "max_id"]

    ID = 0x711d692d
    QUALNAME = "types.RecentStory"

    def __init__(self, *, live: Optional[bool] = None, max_id: Optional[int] = None) -> None:
        self.live = live  # flags.0?true
        self.max_id = max_id  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RecentStory":
        
        flags = Int.read(b)
        
        live = True if flags & (1 << 0) else False
        max_id = Int.read(b) if flags & (1 << 1) else None
        return RecentStory(live=live, max_id=max_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.live else 0
        flags |= (1 << 1) if self.max_id is not None else 0
        b.write(Int(flags))
        
        if self.max_id is not None:
            b.write(Int(self.max_id))
        
        return b.getvalue()
