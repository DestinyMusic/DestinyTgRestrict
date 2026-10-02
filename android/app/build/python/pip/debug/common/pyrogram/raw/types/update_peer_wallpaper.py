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


class UpdatePeerWallpaper(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``228``
        - ID: ``AE3F101D``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        wallpaper_overridden (``bool``, *optional*):
            N/A

        wallpaper (:obj:`WallPaper <pyrogram.raw.base.WallPaper>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["peer", "wallpaper_overridden", "wallpaper"]

    ID = 0xae3f101d
    QUALNAME = "types.UpdatePeerWallpaper"

    def __init__(self, *, peer: "raw.base.Peer", wallpaper_overridden: Optional[bool] = None, wallpaper: "raw.base.WallPaper" = None) -> None:
        self.peer = peer  # Peer
        self.wallpaper_overridden = wallpaper_overridden  # flags.1?true
        self.wallpaper = wallpaper  # flags.0?WallPaper

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdatePeerWallpaper":
        
        flags = Int.read(b)
        
        wallpaper_overridden = True if flags & (1 << 1) else False
        peer = TLObject.read(b)
        
        wallpaper = TLObject.read(b) if flags & (1 << 0) else None
        
        return UpdatePeerWallpaper(peer=peer, wallpaper_overridden=wallpaper_overridden, wallpaper=wallpaper)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.wallpaper_overridden else 0
        flags |= (1 << 0) if self.wallpaper is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        if self.wallpaper is not None:
            b.write(self.wallpaper.write())
        
        return b.getvalue()
