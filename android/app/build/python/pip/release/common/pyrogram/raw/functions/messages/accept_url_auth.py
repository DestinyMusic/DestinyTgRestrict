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


class AcceptUrlAuth(TLObject["raw.base.UrlAuthResult"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``67A3F0DE``

    Parameters:
        write_allowed (``bool``, *optional*):
            N/A

        share_phone_number (``bool``, *optional*):
            N/A

        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            N/A

        msg_id (``int`` ``32-bit``, *optional*):
            N/A

        button_id (``int`` ``32-bit``, *optional*):
            N/A

        url (``str``, *optional*):
            N/A

        match_code (``str``, *optional*):
            N/A

    Returns:
        :obj:`UrlAuthResult <pyrogram.raw.base.UrlAuthResult>`
    """

    __slots__: List[str] = ["write_allowed", "share_phone_number", "peer", "msg_id", "button_id", "url", "match_code"]

    ID = 0x67a3f0de
    QUALNAME = "functions.messages.AcceptUrlAuth"

    def __init__(self, *, write_allowed: Optional[bool] = None, share_phone_number: Optional[bool] = None, peer: "raw.base.InputPeer" = None, msg_id: Optional[int] = None, button_id: Optional[int] = None, url: Optional[str] = None, match_code: Optional[str] = None) -> None:
        self.write_allowed = write_allowed  # flags.0?true
        self.share_phone_number = share_phone_number  # flags.3?true
        self.peer = peer  # flags.1?InputPeer
        self.msg_id = msg_id  # flags.1?int
        self.button_id = button_id  # flags.1?int
        self.url = url  # flags.2?string
        self.match_code = match_code  # flags.4?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AcceptUrlAuth":
        
        flags = Int.read(b)
        
        write_allowed = True if flags & (1 << 0) else False
        share_phone_number = True if flags & (1 << 3) else False
        peer = TLObject.read(b) if flags & (1 << 1) else None
        
        msg_id = Int.read(b) if flags & (1 << 1) else None
        button_id = Int.read(b) if flags & (1 << 1) else None
        url = String.read(b) if flags & (1 << 2) else None
        match_code = String.read(b) if flags & (1 << 4) else None
        return AcceptUrlAuth(write_allowed=write_allowed, share_phone_number=share_phone_number, peer=peer, msg_id=msg_id, button_id=button_id, url=url, match_code=match_code)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.write_allowed else 0
        flags |= (1 << 3) if self.share_phone_number else 0
        flags |= (1 << 1) if self.peer is not None else 0
        flags |= (1 << 1) if self.msg_id is not None else 0
        flags |= (1 << 1) if self.button_id is not None else 0
        flags |= (1 << 2) if self.url is not None else 0
        flags |= (1 << 4) if self.match_code is not None else 0
        b.write(Int(flags))
        
        if self.peer is not None:
            b.write(self.peer.write())
        
        if self.msg_id is not None:
            b.write(Int(self.msg_id))
        
        if self.button_id is not None:
            b.write(Int(self.button_id))
        
        if self.url is not None:
            b.write(String(self.url))
        
        if self.match_code is not None:
            b.write(String(self.match_code))
        
        return b.getvalue()
