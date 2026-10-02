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


class InputPasskeyResponseLogin(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputPasskeyResponse`.

    Details:
        - Layer: ``228``
        - ID: ``C31FC14A``

    Parameters:
        client_data (:obj:`DataJSON <pyrogram.raw.base.DataJSON>`):
            N/A

        authenticator_data (``bytes``):
            N/A

        signature (``bytes``):
            N/A

        user_handle (``str``):
            N/A

    """

    __slots__: List[str] = ["client_data", "authenticator_data", "signature", "user_handle"]

    ID = 0xc31fc14a
    QUALNAME = "types.InputPasskeyResponseLogin"

    def __init__(self, *, client_data: "raw.base.DataJSON", authenticator_data: bytes, signature: bytes, user_handle: str) -> None:
        self.client_data = client_data  # DataJSON
        self.authenticator_data = authenticator_data  # bytes
        self.signature = signature  # bytes
        self.user_handle = user_handle  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPasskeyResponseLogin":
        # No flags
        
        client_data = TLObject.read(b)
        
        authenticator_data = Bytes.read(b)
        
        signature = Bytes.read(b)
        
        user_handle = String.read(b)
        
        return InputPasskeyResponseLogin(client_data=client_data, authenticator_data=authenticator_data, signature=signature, user_handle=user_handle)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.client_data.write())
        
        b.write(Bytes(self.authenticator_data))
        
        b.write(Bytes(self.signature))
        
        b.write(String(self.user_handle))
        
        return b.getvalue()
