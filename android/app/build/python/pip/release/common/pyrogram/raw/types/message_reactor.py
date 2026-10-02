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


class MessageReactor(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MessageReactor`.

    Details:
        - Layer: ``228``
        - ID: ``4BA3A95A``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        top (``bool``, *optional*):
            N/A

        my (``bool``, *optional*):
            N/A

        anonymous (``bool``, *optional*):
            N/A

        peer_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["count", "top", "my", "anonymous", "peer_id"]

    ID = 0x4ba3a95a
    QUALNAME = "types.MessageReactor"

    def __init__(self, *, count: int, top: Optional[bool] = None, my: Optional[bool] = None, anonymous: Optional[bool] = None, peer_id: "raw.base.Peer" = None) -> None:
        self.count = count  # int
        self.top = top  # flags.0?true
        self.my = my  # flags.1?true
        self.anonymous = anonymous  # flags.2?true
        self.peer_id = peer_id  # flags.3?Peer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageReactor":
        
        flags = Int.read(b)
        
        top = True if flags & (1 << 0) else False
        my = True if flags & (1 << 1) else False
        anonymous = True if flags & (1 << 2) else False
        peer_id = TLObject.read(b) if flags & (1 << 3) else None
        
        count = Int.read(b)
        
        return MessageReactor(count=count, top=top, my=my, anonymous=anonymous, peer_id=peer_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.top else 0
        flags |= (1 << 1) if self.my else 0
        flags |= (1 << 2) if self.anonymous else 0
        flags |= (1 << 3) if self.peer_id is not None else 0
        b.write(Int(flags))
        
        if self.peer_id is not None:
            b.write(self.peer_id.write())
        
        b.write(Int(self.count))
        
        return b.getvalue()
