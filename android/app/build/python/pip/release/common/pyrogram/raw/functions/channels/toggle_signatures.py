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


class ToggleSignatures(TLObject["raw.base.Updates"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``418D549C``

    Parameters:
        channel (:obj:`InputChannel <pyrogram.raw.base.InputChannel>`):
            N/A

        signatures_enabled (``bool``, *optional*):
            N/A

        profiles_enabled (``bool``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["channel", "signatures_enabled", "profiles_enabled"]

    ID = 0x418d549c
    QUALNAME = "functions.channels.ToggleSignatures"

    def __init__(self, *, channel: "raw.base.InputChannel", signatures_enabled: Optional[bool] = None, profiles_enabled: Optional[bool] = None) -> None:
        self.channel = channel  # InputChannel
        self.signatures_enabled = signatures_enabled  # flags.0?true
        self.profiles_enabled = profiles_enabled  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ToggleSignatures":
        
        flags = Int.read(b)
        
        signatures_enabled = True if flags & (1 << 0) else False
        profiles_enabled = True if flags & (1 << 1) else False
        channel = TLObject.read(b)
        
        return ToggleSignatures(channel=channel, signatures_enabled=signatures_enabled, profiles_enabled=profiles_enabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.signatures_enabled else 0
        flags |= (1 << 1) if self.profiles_enabled else 0
        b.write(Int(flags))
        
        b.write(self.channel.write())
        
        return b.getvalue()
