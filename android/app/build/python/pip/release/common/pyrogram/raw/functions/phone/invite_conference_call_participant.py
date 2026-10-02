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


class InviteConferenceCallParticipant(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``BCF22685``

    Parameters:
        call (:obj:`InputGroupCall <pyrogram.raw.base.InputGroupCall>`):
            N/A

        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        video (``bool``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["call", "user_id", "video"]

    ID = 0xbcf22685
    QUALNAME = "functions.phone.InviteConferenceCallParticipant"

    def __init__(self, *, call: "raw.base.InputGroupCall", user_id: "raw.base.InputUser", video: Optional[bool] = None) -> None:
        self.call = call  # InputGroupCall
        self.user_id = user_id  # InputUser
        self.video = video  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InviteConferenceCallParticipant":
        
        flags = Int.read(b)
        
        video = True if flags & (1 << 0) else False
        call = TLObject.read(b)
        
        user_id = TLObject.read(b)
        
        return InviteConferenceCallParticipant(call=call, user_id=user_id, video=video)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.video else 0
        b.write(Int(flags))
        
        b.write(self.call.write())
        
        b.write(self.user_id.write())
        
        return b.getvalue()
