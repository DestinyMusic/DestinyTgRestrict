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


class JoinGroupCall(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``8FB53057``

    Parameters:
        call (:obj:`InputGroupCall <pyrogram.raw.base.InputGroupCall>`):
            N/A

        join_as (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        params (:obj:`DataJSON <pyrogram.raw.base.DataJSON>`):
            N/A

        muted (``bool``, *optional*):
            N/A

        video_stopped (``bool``, *optional*):
            N/A

        invite_hash (``str``, *optional*):
            N/A

        public_key (``int`` ``256-bit``, *optional*):
            N/A

        block (``bytes``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["call", "join_as", "params", "muted", "video_stopped", "invite_hash", "public_key", "block"]

    ID = 0x8fb53057
    QUALNAME = "functions.phone.JoinGroupCall"

    def __init__(self, *, call: "raw.base.InputGroupCall", join_as: "raw.base.InputPeer", params: "raw.base.DataJSON", muted: Optional[bool] = None, video_stopped: Optional[bool] = None, invite_hash: Optional[str] = None, public_key: Optional[int] = None, block: Optional[bytes] = None) -> None:
        self.call = call  # InputGroupCall
        self.join_as = join_as  # InputPeer
        self.params = params  # DataJSON
        self.muted = muted  # flags.0?true
        self.video_stopped = video_stopped  # flags.2?true
        self.invite_hash = invite_hash  # flags.1?string
        self.public_key = public_key  # flags.3?int256
        self.block = block  # flags.3?bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JoinGroupCall":
        
        flags = Int.read(b)
        
        muted = True if flags & (1 << 0) else False
        video_stopped = True if flags & (1 << 2) else False
        call = TLObject.read(b)
        
        join_as = TLObject.read(b)
        
        invite_hash = String.read(b) if flags & (1 << 1) else None
        public_key = Int256.read(b) if flags & (1 << 3) else None
        block = Bytes.read(b) if flags & (1 << 3) else None
        params = TLObject.read(b)
        
        return JoinGroupCall(call=call, join_as=join_as, params=params, muted=muted, video_stopped=video_stopped, invite_hash=invite_hash, public_key=public_key, block=block)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.muted else 0
        flags |= (1 << 2) if self.video_stopped else 0
        flags |= (1 << 1) if self.invite_hash is not None else 0
        flags |= (1 << 3) if self.public_key is not None else 0
        flags |= (1 << 3) if self.block is not None else 0
        b.write(Int(flags))
        
        b.write(self.call.write())
        
        b.write(self.join_as.write())
        
        if self.invite_hash is not None:
            b.write(String(self.invite_hash))
        
        if self.public_key is not None:
            b.write(Int256(self.public_key))
        
        if self.block is not None:
            b.write(Bytes(self.block))
        
        b.write(self.params.write())
        
        return b.getvalue()
