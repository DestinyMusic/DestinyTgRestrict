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


class MyBoost(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MyBoost`.

    Details:
        - Layer: ``228``
        - ID: ``C448415C``

    Parameters:
        slot (``int`` ``32-bit``):
            N/A

        date (``int`` ``32-bit``):
            N/A

        expires (``int`` ``32-bit``):
            N/A

        peer (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        cooldown_until_date (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["slot", "date", "expires", "peer", "cooldown_until_date"]

    ID = 0xc448415c
    QUALNAME = "types.MyBoost"

    def __init__(self, *, slot: int, date: int, expires: int, peer: "raw.base.Peer" = None, cooldown_until_date: Optional[int] = None) -> None:
        self.slot = slot  # int
        self.date = date  # int
        self.expires = expires  # int
        self.peer = peer  # flags.0?Peer
        self.cooldown_until_date = cooldown_until_date  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MyBoost":
        
        flags = Int.read(b)
        
        slot = Int.read(b)
        
        peer = TLObject.read(b) if flags & (1 << 0) else None
        
        date = Int.read(b)
        
        expires = Int.read(b)
        
        cooldown_until_date = Int.read(b) if flags & (1 << 1) else None
        return MyBoost(slot=slot, date=date, expires=expires, peer=peer, cooldown_until_date=cooldown_until_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.peer is not None else 0
        flags |= (1 << 1) if self.cooldown_until_date is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.slot))
        
        if self.peer is not None:
            b.write(self.peer.write())
        
        b.write(Int(self.date))
        
        b.write(Int(self.expires))
        
        if self.cooldown_until_date is not None:
            b.write(Int(self.cooldown_until_date))
        
        return b.getvalue()
