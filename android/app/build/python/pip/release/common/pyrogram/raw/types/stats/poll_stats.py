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


class PollStats(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.stats.PollStats`.

    Details:
        - Layer: ``228``
        - ID: ``2999BEED``

    Parameters:
        votes_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            stats.GetPollStats
    """

    __slots__: List[str] = ["votes_graph"]

    ID = 0x2999beed
    QUALNAME = "types.stats.PollStats"

    def __init__(self, *, votes_graph: "raw.base.StatsGraph") -> None:
        self.votes_graph = votes_graph  # StatsGraph

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PollStats":
        # No flags
        
        votes_graph = TLObject.read(b)
        
        return PollStats(votes_graph=votes_graph)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.votes_graph.write())
        
        return b.getvalue()
