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


class PasskeyRegistrationOptions(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.account.PasskeyRegistrationOptions`.

    Details:
        - Layer: ``228``
        - ID: ``E16B5CE1``

    Parameters:
        options (:obj:`DataJSON <pyrogram.raw.base.DataJSON>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.InitPasskeyRegistration
    """

    __slots__: List[str] = ["options"]

    ID = 0xe16b5ce1
    QUALNAME = "types.account.PasskeyRegistrationOptions"

    def __init__(self, *, options: "raw.base.DataJSON") -> None:
        self.options = options  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PasskeyRegistrationOptions":
        # No flags
        
        options = TLObject.read(b)
        
        return PasskeyRegistrationOptions(options=options)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.options.write())
        
        return b.getvalue()
