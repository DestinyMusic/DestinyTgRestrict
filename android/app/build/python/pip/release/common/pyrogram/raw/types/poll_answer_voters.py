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


class PollAnswerVoters(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PollAnswerVoters`.

    Details:
        - Layer: ``228``
        - ID: ``3645230A``

    Parameters:
        option (``bytes``):
            N/A

        chosen (``bool``, *optional*):
            N/A

        correct (``bool``, *optional*):
            N/A

        voters (``int`` ``32-bit``, *optional*):
            N/A

        recent_voters (List of :obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["option", "chosen", "correct", "voters", "recent_voters"]

    ID = 0x3645230a
    QUALNAME = "types.PollAnswerVoters"

    def __init__(self, *, option: bytes, chosen: Optional[bool] = None, correct: Optional[bool] = None, voters: Optional[int] = None, recent_voters: Optional[List["raw.base.Peer"]] = None) -> None:
        self.option = option  # bytes
        self.chosen = chosen  # flags.0?true
        self.correct = correct  # flags.1?true
        self.voters = voters  # flags.2?int
        self.recent_voters = recent_voters  # flags.2?Vector<Peer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PollAnswerVoters":
        
        flags = Int.read(b)
        
        chosen = True if flags & (1 << 0) else False
        correct = True if flags & (1 << 1) else False
        option = Bytes.read(b)
        
        voters = Int.read(b) if flags & (1 << 2) else None
        recent_voters = TLObject.read(b) if flags & (1 << 2) else []
        
        return PollAnswerVoters(option=option, chosen=chosen, correct=correct, voters=voters, recent_voters=recent_voters)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.chosen else 0
        flags |= (1 << 1) if self.correct else 0
        flags |= (1 << 2) if self.voters is not None else 0
        flags |= (1 << 2) if self.recent_voters else 0
        b.write(Int(flags))
        
        b.write(Bytes(self.option))
        
        if self.voters is not None:
            b.write(Int(self.voters))
        
        if self.recent_voters:
            b.write(Vector(self.recent_voters))
        
        return b.getvalue()
