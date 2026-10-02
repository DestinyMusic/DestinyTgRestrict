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


class AvailableEffect(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.AvailableEffect`.

    Details:
        - Layer: ``228``
        - ID: ``93C3E27E``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        emoticon (``str``):
            N/A

        effect_sticker_id (``int`` ``64-bit``):
            N/A

        premium_required (``bool``, *optional*):
            N/A

        static_icon_id (``int`` ``64-bit``, *optional*):
            N/A

        effect_animation_id (``int`` ``64-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "emoticon", "effect_sticker_id", "premium_required", "static_icon_id", "effect_animation_id"]

    ID = 0x93c3e27e
    QUALNAME = "types.AvailableEffect"

    def __init__(self, *, id: int, emoticon: str, effect_sticker_id: int, premium_required: Optional[bool] = None, static_icon_id: Optional[int] = None, effect_animation_id: Optional[int] = None) -> None:
        self.id = id  # long
        self.emoticon = emoticon  # string
        self.effect_sticker_id = effect_sticker_id  # long
        self.premium_required = premium_required  # flags.2?true
        self.static_icon_id = static_icon_id  # flags.0?long
        self.effect_animation_id = effect_animation_id  # flags.1?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AvailableEffect":
        
        flags = Int.read(b)
        
        premium_required = True if flags & (1 << 2) else False
        id = Long.read(b)
        
        emoticon = String.read(b)
        
        static_icon_id = Long.read(b) if flags & (1 << 0) else None
        effect_sticker_id = Long.read(b)
        
        effect_animation_id = Long.read(b) if flags & (1 << 1) else None
        return AvailableEffect(id=id, emoticon=emoticon, effect_sticker_id=effect_sticker_id, premium_required=premium_required, static_icon_id=static_icon_id, effect_animation_id=effect_animation_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.premium_required else 0
        flags |= (1 << 0) if self.static_icon_id is not None else 0
        flags |= (1 << 1) if self.effect_animation_id is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.id))
        
        b.write(String(self.emoticon))
        
        if self.static_icon_id is not None:
            b.write(Long(self.static_icon_id))
        
        b.write(Long(self.effect_sticker_id))
        
        if self.effect_animation_id is not None:
            b.write(Long(self.effect_animation_id))
        
        return b.getvalue()
