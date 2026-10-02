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


class GetChannelRecommendations(TLObject["raw.base.messages.Chats"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``25A71742``

    Parameters:
        channel (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`, *optional*):
            N/A

    Returns:
        :obj:`messages.Chats <pyrogram.raw.base.messages.Chats>`
    """

    __slots__: List[str] = ["channel"]

    ID = 0x25a71742
    QUALNAME = "functions.channels.GetChannelRecommendations"

    def __init__(self, *, channel: "raw.base.InputChannel" = None) -> None:
        self.channel = channel  # flags.0?InputChannel

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetChannelRecommendations":
        
        flags = Int.read(b)
        
        channel = TLObject.read(b) if flags & (1 << 0) else None
        
        return GetChannelRecommendations(channel=channel)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.channel is not None else 0
        b.write(Int(flags))
        
        if self.channel is not None:
            b.write(self.channel.write())
        
        return b.getvalue()
