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


class UpdateJoinChatWebViewDecision(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``BDAC7E70``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        query_id (``int`` ``64-bit``):
            N/A

        result (:obj:`JoinChatBotResult <pyrogram.raw.base.JoinChatBotResult>`):
            N/A

    """

    __slots__: List[str] = ["peer", "query_id", "result"]

    ID = 0xbdac7e70
    QUALNAME = "types.UpdateJoinChatWebViewDecision"

    def __init__(self, *, peer: "raw.base.Peer", query_id: int, result: "raw.base.JoinChatBotResult") -> None:
        self.peer = peer  # Peer
        self.query_id = query_id  # long
        self.result = result  # JoinChatBotResult

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateJoinChatWebViewDecision":
        # No flags
        
        peer = TLObject.read(b)
        
        query_id = Long.read(b)
        
        result = TLObject.read(b)
        
        return UpdateJoinChatWebViewDecision(peer=peer, query_id=query_id, result=result)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Long(self.query_id))
        
        b.write(self.result.write())
        
        return b.getvalue()
