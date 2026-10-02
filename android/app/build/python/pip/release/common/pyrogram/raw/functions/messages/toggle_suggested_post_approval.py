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


class ToggleSuggestedPostApproval(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``8107455C``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        reject (``bool``, *optional*):
            N/A

        schedule_date (``int`` ``32-bit``, *optional*):
            N/A

        reject_comment (``str``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "msg_id", "reject", "schedule_date", "reject_comment"]

    ID = 0x8107455c
    QUALNAME = "functions.messages.ToggleSuggestedPostApproval"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int, reject: Optional[bool] = None, schedule_date: Optional[int] = None, reject_comment: Optional[str] = None) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.reject = reject  # flags.1?true
        self.schedule_date = schedule_date  # flags.0?int
        self.reject_comment = reject_comment  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ToggleSuggestedPostApproval":
        
        flags = Int.read(b)
        
        reject = True if flags & (1 << 1) else False
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        schedule_date = Int.read(b) if flags & (1 << 0) else None
        reject_comment = String.read(b) if flags & (1 << 2) else None
        return ToggleSuggestedPostApproval(peer=peer, msg_id=msg_id, reject=reject, schedule_date=schedule_date, reject_comment=reject_comment)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.reject else 0
        flags |= (1 << 0) if self.schedule_date is not None else 0
        flags |= (1 << 2) if self.reject_comment is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        if self.schedule_date is not None:
            b.write(Int(self.schedule_date))
        
        if self.reject_comment is not None:
            b.write(String(self.reject_comment))
        
        return b.getvalue()
