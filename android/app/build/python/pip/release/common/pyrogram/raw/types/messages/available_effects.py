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


class AvailableEffects(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.messages.AvailableEffects`.

    Details:
        - Layer: ``228``
        - ID: ``BDDB616E``

    Parameters:
        hash (``int`` ``32-bit``):
            N/A

        effects (List of :obj:`AvailableEffect <pyrogram.raw.base.AvailableEffect>`):
            N/A

        documents (List of :obj:`Document <pyrogram.raw.base.Document>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetAvailableEffects
    """

    __slots__: List[str] = ["hash", "effects", "documents"]

    ID = 0xbddb616e
    QUALNAME = "types.messages.AvailableEffects"

    def __init__(self, *, hash: int, effects: List["raw.base.AvailableEffect"], documents: List["raw.base.Document"]) -> None:
        self.hash = hash  # int
        self.effects = effects  # Vector<AvailableEffect>
        self.documents = documents  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AvailableEffects":
        # No flags
        
        hash = Int.read(b)
        
        effects = TLObject.read(b)
        
        documents = TLObject.read(b)
        
        return AvailableEffects(hash=hash, effects=effects, documents=documents)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.effects))
        
        b.write(Vector(self.documents))
        
        return b.getvalue()
