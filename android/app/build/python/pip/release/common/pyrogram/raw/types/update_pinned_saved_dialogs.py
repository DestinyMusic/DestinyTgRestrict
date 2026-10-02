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


class UpdatePinnedSavedDialogs(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``686C85A6``

    Parameters:
        order (List of :obj:`DialogPeer <pyrogram.raw.base.DialogPeer>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["order"]

    ID = 0x686c85a6
    QUALNAME = "types.UpdatePinnedSavedDialogs"

    def __init__(self, *, order: Optional[List["raw.base.DialogPeer"]] = None) -> None:
        self.order = order  # flags.0?Vector<DialogPeer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdatePinnedSavedDialogs":
        
        flags = Int.read(b)
        
        order = TLObject.read(b) if flags & (1 << 0) else []
        
        return UpdatePinnedSavedDialogs(order=order)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.order else 0
        b.write(Int(flags))
        
        if self.order:
            b.write(Vector(self.order))
        
        return b.getvalue()
