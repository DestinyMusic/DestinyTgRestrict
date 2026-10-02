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


class ReportResultChooseOption(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.ReportResult`.

    Details:
        - Layer: ``228``
        - ID: ``F0E4E0B6``

    Parameters:
        title (``str``):
            N/A

        options (List of :obj:`MessageReportOption <pyrogram.raw.base.MessageReportOption>`):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.Report
            stories.Report
            ephemeral.ReportMessage
    """

    __slots__: List[str] = ["title", "options"]

    ID = 0xf0e4e0b6
    QUALNAME = "types.ReportResultChooseOption"

    def __init__(self, *, title: str, options: List["raw.base.MessageReportOption"]) -> None:
        self.title = title  # string
        self.options = options  # Vector<MessageReportOption>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReportResultChooseOption":
        # No flags
        
        title = String.read(b)
        
        options = TLObject.read(b)
        
        return ReportResultChooseOption(title=title, options=options)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.title))
        
        b.write(Vector(self.options))
        
        return b.getvalue()
