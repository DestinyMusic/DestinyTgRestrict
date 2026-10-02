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


class AttachMenuBot(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.AttachMenuBot`.

    Details:
        - Layer: ``228``
        - ID: ``D90D8DFE``

    Parameters:
        bot_id (``int`` ``64-bit``):
            N/A

        short_name (``str``):
            N/A

        icons (List of :obj:`AttachMenuBotIcon <pyrogram.raw.base.AttachMenuBotIcon>`):
            N/A

        inactive (``bool``, *optional*):
            N/A

        has_settings (``bool``, *optional*):
            N/A

        request_write_access (``bool``, *optional*):
            N/A

        show_in_attach_menu (``bool``, *optional*):
            N/A

        show_in_side_menu (``bool``, *optional*):
            N/A

        side_menu_disclaimer_needed (``bool``, *optional*):
            N/A

        peer_types (List of :obj:`AttachMenuPeerType <pyrogram.raw.base.AttachMenuPeerType>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["bot_id", "short_name", "icons", "inactive", "has_settings", "request_write_access", "show_in_attach_menu", "show_in_side_menu", "side_menu_disclaimer_needed", "peer_types"]

    ID = 0xd90d8dfe
    QUALNAME = "types.AttachMenuBot"

    def __init__(self, *, bot_id: int, short_name: str, icons: List["raw.base.AttachMenuBotIcon"], inactive: Optional[bool] = None, has_settings: Optional[bool] = None, request_write_access: Optional[bool] = None, show_in_attach_menu: Optional[bool] = None, show_in_side_menu: Optional[bool] = None, side_menu_disclaimer_needed: Optional[bool] = None, peer_types: Optional[List["raw.base.AttachMenuPeerType"]] = None) -> None:
        self.bot_id = bot_id  # long
        self.short_name = short_name  # string
        self.icons = icons  # Vector<AttachMenuBotIcon>
        self.inactive = inactive  # flags.0?true
        self.has_settings = has_settings  # flags.1?true
        self.request_write_access = request_write_access  # flags.2?true
        self.show_in_attach_menu = show_in_attach_menu  # flags.3?true
        self.show_in_side_menu = show_in_side_menu  # flags.4?true
        self.side_menu_disclaimer_needed = side_menu_disclaimer_needed  # flags.5?true
        self.peer_types = peer_types  # flags.3?Vector<AttachMenuPeerType>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AttachMenuBot":
        
        flags = Int.read(b)
        
        inactive = True if flags & (1 << 0) else False
        has_settings = True if flags & (1 << 1) else False
        request_write_access = True if flags & (1 << 2) else False
        show_in_attach_menu = True if flags & (1 << 3) else False
        show_in_side_menu = True if flags & (1 << 4) else False
        side_menu_disclaimer_needed = True if flags & (1 << 5) else False
        bot_id = Long.read(b)
        
        short_name = String.read(b)
        
        peer_types = TLObject.read(b) if flags & (1 << 3) else []
        
        icons = TLObject.read(b)
        
        return AttachMenuBot(bot_id=bot_id, short_name=short_name, icons=icons, inactive=inactive, has_settings=has_settings, request_write_access=request_write_access, show_in_attach_menu=show_in_attach_menu, show_in_side_menu=show_in_side_menu, side_menu_disclaimer_needed=side_menu_disclaimer_needed, peer_types=peer_types)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.inactive else 0
        flags |= (1 << 1) if self.has_settings else 0
        flags |= (1 << 2) if self.request_write_access else 0
        flags |= (1 << 3) if self.show_in_attach_menu else 0
        flags |= (1 << 4) if self.show_in_side_menu else 0
        flags |= (1 << 5) if self.side_menu_disclaimer_needed else 0
        flags |= (1 << 3) if self.peer_types else 0
        b.write(Int(flags))
        
        b.write(Long(self.bot_id))
        
        b.write(String(self.short_name))
        
        if self.peer_types:
            b.write(Vector(self.peer_types))
        
        b.write(Vector(self.icons))
        
        return b.getvalue()
