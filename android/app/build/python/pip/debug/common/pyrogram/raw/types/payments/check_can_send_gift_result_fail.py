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


class CheckCanSendGiftResultFail(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.CheckCanSendGiftResult`.

    Details:
        - Layer: ``228``
        - ID: ``D5E58274``

    Parameters:
        reason (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.CheckCanSendGift
    """

    __slots__: List[str] = ["reason"]

    ID = 0xd5e58274
    QUALNAME = "types.payments.CheckCanSendGiftResultFail"

    def __init__(self, *, reason: "raw.base.TextWithEntities") -> None:
        self.reason = reason  # TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckCanSendGiftResultFail":
        # No flags
        
        reason = TLObject.read(b)
        
        return CheckCanSendGiftResultFail(reason=reason)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.reason.write())
        
        return b.getvalue()
