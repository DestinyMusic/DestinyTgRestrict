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


class GetSavedReactionTags(TLObject["raw.base.messages.SavedReactionTags"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``3637E05B``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            N/A

    Returns:
        :obj:`messages.SavedReactionTags <pyrogram.raw.base.messages.SavedReactionTags>`
    """

    __slots__: List[str] = ["hash", "peer"]

    ID = 0x3637e05b
    QUALNAME = "functions.messages.GetSavedReactionTags"

    def __init__(self, *, hash: int, peer: "raw.base.InputPeer" = None) -> None:
        self.hash = hash  # long
        self.peer = peer  # flags.0?InputPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetSavedReactionTags":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b) if flags & (1 << 0) else None
        
        hash = Long.read(b)
        
        return GetSavedReactionTags(hash=hash, peer=peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.peer is not None else 0
        b.write(Int(flags))
        
        if self.peer is not None:
            b.write(self.peer.write())
        
        b.write(Long(self.hash))
        
        return b.getvalue()
