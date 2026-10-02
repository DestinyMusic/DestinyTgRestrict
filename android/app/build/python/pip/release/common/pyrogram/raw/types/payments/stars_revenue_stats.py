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


class StarsRevenueStats(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.StarsRevenueStats`.

    Details:
        - Layer: ``228``
        - ID: ``6C207376``

    Parameters:
        revenue_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        status (:obj:`StarsRevenueStatus <pyrogram.raw.base.StarsRevenueStatus>`):
            N/A

        usd_rate (``float`` ``64-bit``):
            N/A

        top_hours_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetStarsRevenueStats
    """

    __slots__: List[str] = ["revenue_graph", "status", "usd_rate", "top_hours_graph"]

    ID = 0x6c207376
    QUALNAME = "types.payments.StarsRevenueStats"

    def __init__(self, *, revenue_graph: "raw.base.StatsGraph", status: "raw.base.StarsRevenueStatus", usd_rate: float, top_hours_graph: "raw.base.StatsGraph" = None) -> None:
        self.revenue_graph = revenue_graph  # StatsGraph
        self.status = status  # StarsRevenueStatus
        self.usd_rate = usd_rate  # double
        self.top_hours_graph = top_hours_graph  # flags.0?StatsGraph

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsRevenueStats":
        
        flags = Int.read(b)
        
        top_hours_graph = TLObject.read(b) if flags & (1 << 0) else None
        
        revenue_graph = TLObject.read(b)
        
        status = TLObject.read(b)
        
        usd_rate = Double.read(b)
        
        return StarsRevenueStats(revenue_graph=revenue_graph, status=status, usd_rate=usd_rate, top_hours_graph=top_hours_graph)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.top_hours_graph is not None else 0
        b.write(Int(flags))
        
        if self.top_hours_graph is not None:
            b.write(self.top_hours_graph.write())
        
        b.write(self.revenue_graph.write())
        
        b.write(self.status.write())
        
        b.write(Double(self.usd_rate))
        
        return b.getvalue()
