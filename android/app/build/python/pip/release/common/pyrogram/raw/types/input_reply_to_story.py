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


class InputReplyToStory(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputReplyTo`.

    Details:
        - Layer: ``228``
        - ID: ``5881323A``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        story_id (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["peer", "story_id"]

    ID = 0x5881323a
    QUALNAME = "types.InputReplyToStory"

    def __init__(self, *, peer: "raw.base.InputPeer", story_id: int) -> None:
        self.peer = peer  # InputPeer
        self.story_id = story_id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputReplyToStory":
        # No flags
        
        peer = TLObject.read(b)
        
        story_id = Int.read(b)
        
        return InputReplyToStory(peer=peer, story_id=story_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.story_id))
        
        return b.getvalue()
