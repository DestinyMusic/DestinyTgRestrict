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


class ReportSponsoredMessage(TLObject["raw.base.channels.SponsoredMessageReportResult"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``12CBF0C4``

    Parameters:
        random_id (``bytes``):
            N/A

        option (``bytes``):
            N/A

    Returns:
        :obj:`channels.SponsoredMessageReportResult <pyrogram.raw.base.channels.SponsoredMessageReportResult>`
    """

    __slots__: List[str] = ["random_id", "option"]

    ID = 0x12cbf0c4
    QUALNAME = "functions.messages.ReportSponsoredMessage"

    def __init__(self, *, random_id: bytes, option: bytes) -> None:
        self.random_id = random_id  # bytes
        self.option = option  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReportSponsoredMessage":
        # No flags
        
        random_id = Bytes.read(b)
        
        option = Bytes.read(b)
        
        return ReportSponsoredMessage(random_id=random_id, option=option)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.random_id))
        
        b.write(Bytes(self.option))
        
        return b.getvalue()
