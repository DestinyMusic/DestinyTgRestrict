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


class Community(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Chat`.

    Details:
        - Layer: ``228``
        - ID: ``65EFE954``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        title (``str``):
            N/A

        photo (:obj:`ChatPhoto <pyrogram.raw.base.ChatPhoto>`):
            N/A

        date (``int`` ``32-bit``):
            N/A

        creator (``bool``, *optional*):
            N/A

        left (``bool``, *optional*):
            N/A

        min (``bool``, *optional*):
            N/A

        collapsed_in_dialogs (``bool``, *optional*):
            N/A

        access_hash (``int`` ``64-bit``, *optional*):
            N/A

        admin_rights (:obj:`ChatAdminRights <pyrogram.raw.base.ChatAdminRights>`, *optional*):
            N/A

        default_banned_rights (:obj:`ChatBannedRights <pyrogram.raw.base.ChatBannedRights>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "title", "photo", "date", "creator", "left", "min", "collapsed_in_dialogs", "access_hash", "admin_rights", "default_banned_rights"]

    ID = 0x65efe954
    QUALNAME = "types.Community"

    def __init__(self, *, id: int, title: str, photo: "raw.base.ChatPhoto", date: int, creator: Optional[bool] = None, left: Optional[bool] = None, min: Optional[bool] = None, collapsed_in_dialogs: Optional[bool] = None, access_hash: Optional[int] = None, admin_rights: "raw.base.ChatAdminRights" = None, default_banned_rights: "raw.base.ChatBannedRights" = None) -> None:
        self.id = id  # long
        self.title = title  # string
        self.photo = photo  # ChatPhoto
        self.date = date  # int
        self.creator = creator  # flags.0?true
        self.left = left  # flags.2?true
        self.min = min  # flags.12?true
        self.collapsed_in_dialogs = collapsed_in_dialogs  # flags2.20?true
        self.access_hash = access_hash  # flags.13?long
        self.admin_rights = admin_rights  # flags.14?ChatAdminRights
        self.default_banned_rights = default_banned_rights  # flags.18?ChatBannedRights

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Community":
        
        flags = Int.read(b)
        
        creator = True if flags & (1 << 0) else False
        left = True if flags & (1 << 2) else False
        min = True if flags & (1 << 12) else False
        flags2 = Int.read(b)
        
        collapsed_in_dialogs = True if flags2 & (1 << 20) else False
        id = Long.read(b)
        
        access_hash = Long.read(b) if flags & (1 << 13) else None
        title = String.read(b)
        
        photo = TLObject.read(b)
        
        date = Int.read(b)
        
        admin_rights = TLObject.read(b) if flags & (1 << 14) else None
        
        default_banned_rights = TLObject.read(b) if flags & (1 << 18) else None
        
        return Community(id=id, title=title, photo=photo, date=date, creator=creator, left=left, min=min, collapsed_in_dialogs=collapsed_in_dialogs, access_hash=access_hash, admin_rights=admin_rights, default_banned_rights=default_banned_rights)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.creator else 0
        flags |= (1 << 2) if self.left else 0
        flags |= (1 << 12) if self.min else 0
        flags |= (1 << 13) if self.access_hash is not None else 0
        flags |= (1 << 14) if self.admin_rights is not None else 0
        flags |= (1 << 18) if self.default_banned_rights is not None else 0
        b.write(Int(flags))
        flags2 = 0
        flags2 |= (1 << 20) if self.collapsed_in_dialogs else 0
        b.write(Int(flags2))
        
        b.write(Long(self.id))
        
        if self.access_hash is not None:
            b.write(Long(self.access_hash))
        
        b.write(String(self.title))
        
        b.write(self.photo.write())
        
        b.write(Int(self.date))
        
        if self.admin_rights is not None:
            b.write(self.admin_rights.write())
        
        if self.default_banned_rights is not None:
            b.write(self.default_banned_rights.write())
        
        return b.getvalue()
