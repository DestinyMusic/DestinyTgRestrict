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


class GetSmsJob(TLObject["raw.base.SmsJob"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``778D902F``

    Parameters:
        job_id (``str``):
            N/A

    Returns:
        :obj:`SmsJob <pyrogram.raw.base.SmsJob>`
    """

    __slots__: List[str] = ["job_id"]

    ID = 0x778d902f
    QUALNAME = "functions.smsjobs.GetSmsJob"

    def __init__(self, *, job_id: str) -> None:
        self.job_id = job_id  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetSmsJob":
        # No flags
        
        job_id = String.read(b)
        
        return GetSmsJob(job_id=job_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.job_id))
        
        return b.getvalue()
