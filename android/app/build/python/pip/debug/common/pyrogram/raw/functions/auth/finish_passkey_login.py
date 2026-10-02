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


class FinishPasskeyLogin(TLObject["raw.base.auth.Authorization"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``9857AD07``

    Parameters:
        credential (:obj:`InputPasskeyCredential <pyrogram.raw.base.InputPasskeyCredential>`):
            N/A

        from_dc_id (``int`` ``32-bit``, *optional*):
            N/A

        from_auth_key_id (``int`` ``64-bit``, *optional*):
            N/A

    Returns:
        :obj:`auth.Authorization <pyrogram.raw.base.auth.Authorization>`
    """

    __slots__: List[str] = ["credential", "from_dc_id", "from_auth_key_id"]

    ID = 0x9857ad07
    QUALNAME = "functions.auth.FinishPasskeyLogin"

    def __init__(self, *, credential: "raw.base.InputPasskeyCredential", from_dc_id: Optional[int] = None, from_auth_key_id: Optional[int] = None) -> None:
        self.credential = credential  # InputPasskeyCredential
        self.from_dc_id = from_dc_id  # flags.0?int
        self.from_auth_key_id = from_auth_key_id  # flags.0?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "FinishPasskeyLogin":
        
        flags = Int.read(b)
        
        credential = TLObject.read(b)
        
        from_dc_id = Int.read(b) if flags & (1 << 0) else None
        from_auth_key_id = Long.read(b) if flags & (1 << 0) else None
        return FinishPasskeyLogin(credential=credential, from_dc_id=from_dc_id, from_auth_key_id=from_auth_key_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.from_dc_id is not None else 0
        flags |= (1 << 0) if self.from_auth_key_id is not None else 0
        b.write(Int(flags))
        
        b.write(self.credential.write())
        
        if self.from_dc_id is not None:
            b.write(Int(self.from_dc_id))
        
        if self.from_auth_key_id is not None:
            b.write(Long(self.from_auth_key_id))
        
        return b.getvalue()
