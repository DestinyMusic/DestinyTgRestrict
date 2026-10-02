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


class InputPasskeyCredentialPublicKey(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputPasskeyCredential`.

    Details:
        - Layer: ``228``
        - ID: ``3C27B78F``

    Parameters:
        id (``str``):
            N/A

        raw_id (``str``):
            N/A

        response (:obj:`InputPasskeyResponse <pyrogram.raw.base.InputPasskeyResponse>`):
            N/A

    """

    __slots__: List[str] = ["id", "raw_id", "response"]

    ID = 0x3c27b78f
    QUALNAME = "types.InputPasskeyCredentialPublicKey"

    def __init__(self, *, id: str, raw_id: str, response: "raw.base.InputPasskeyResponse") -> None:
        self.id = id  # string
        self.raw_id = raw_id  # string
        self.response = response  # InputPasskeyResponse

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPasskeyCredentialPublicKey":
        # No flags
        
        id = String.read(b)
        
        raw_id = String.read(b)
        
        response = TLObject.read(b)
        
        return InputPasskeyCredentialPublicKey(id=id, raw_id=raw_id, response=response)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(String(self.raw_id))
        
        b.write(self.response.write())
        
        return b.getvalue()
