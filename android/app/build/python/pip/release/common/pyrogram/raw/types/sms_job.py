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


class SmsJob(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.SmsJob`.

    Details:
        - Layer: ``228``
        - ID: ``E6A1EEB8``

    Parameters:
        job_id (``str``):
            N/A

        phone_number (``str``):
            N/A

        text (``str``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            smsjobs.GetSmsJob
    """

    __slots__: List[str] = ["job_id", "phone_number", "text"]

    ID = 0xe6a1eeb8
    QUALNAME = "types.SmsJob"

    def __init__(self, *, job_id: str, phone_number: str, text: str) -> None:
        self.job_id = job_id  # string
        self.phone_number = phone_number  # string
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SmsJob":
        # No flags
        
        job_id = String.read(b)
        
        phone_number = String.read(b)
        
        text = String.read(b)
        
        return SmsJob(job_id=job_id, phone_number=phone_number, text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.job_id))
        
        b.write(String(self.phone_number))
        
        b.write(String(self.text))
        
        return b.getvalue()
