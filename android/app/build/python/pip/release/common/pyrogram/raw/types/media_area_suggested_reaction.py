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


class MediaAreaSuggestedReaction(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.MediaArea`.

    Details:
        - Layer: ``228``
        - ID: ``14455871``

    Parameters:
        coordinates (:obj:`MediaAreaCoordinates <pyrogram.raw.base.MediaAreaCoordinates>`):
            N/A

        reaction (:obj:`Reaction <pyrogram.raw.base.Reaction>`):
            N/A

        dark (``bool``, *optional*):
            N/A

        flipped (``bool``, *optional*):
            N/A

    """

    __slots__: List[str] = ["coordinates", "reaction", "dark", "flipped"]

    ID = 0x14455871
    QUALNAME = "types.MediaAreaSuggestedReaction"

    def __init__(self, *, coordinates: "raw.base.MediaAreaCoordinates", reaction: "raw.base.Reaction", dark: Optional[bool] = None, flipped: Optional[bool] = None) -> None:
        self.coordinates = coordinates  # MediaAreaCoordinates
        self.reaction = reaction  # Reaction
        self.dark = dark  # flags.0?true
        self.flipped = flipped  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MediaAreaSuggestedReaction":
        
        flags = Int.read(b)
        
        dark = True if flags & (1 << 0) else False
        flipped = True if flags & (1 << 1) else False
        coordinates = TLObject.read(b)
        
        reaction = TLObject.read(b)
        
        return MediaAreaSuggestedReaction(coordinates=coordinates, reaction=reaction, dark=dark, flipped=flipped)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.dark else 0
        flags |= (1 << 1) if self.flipped else 0
        b.write(Int(flags))
        
        b.write(self.coordinates.write())
        
        b.write(self.reaction.write())
        
        return b.getvalue()
