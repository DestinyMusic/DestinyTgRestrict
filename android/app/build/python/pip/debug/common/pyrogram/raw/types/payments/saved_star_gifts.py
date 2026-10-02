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


class SavedStarGifts(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.payments.SavedStarGifts`.

    Details:
        - Layer: ``228``
        - ID: ``95F389B1``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        gifts (List of :obj:`SavedStarGift <pyrogram.raw.base.SavedStarGift>`):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        chat_notifications_enabled (``bool``, *optional*):
            N/A

        next_offset (``str``, *optional*):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetSavedStarGifts
            payments.GetSavedStarGift
            payments.GetCraftStarGifts
    """

    __slots__: List[str] = ["count", "gifts", "chats", "users", "chat_notifications_enabled", "next_offset"]

    ID = 0x95f389b1
    QUALNAME = "types.payments.SavedStarGifts"

    def __init__(self, *, count: int, gifts: List["raw.base.SavedStarGift"], chats: List["raw.base.Chat"], users: List["raw.base.User"], chat_notifications_enabled: Optional[bool] = None, next_offset: Optional[str] = None) -> None:
        self.count = count  # int
        self.gifts = gifts  # Vector<SavedStarGift>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.chat_notifications_enabled = chat_notifications_enabled  # flags.1?Bool
        self.next_offset = next_offset  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SavedStarGifts":
        
        flags = Int.read(b)
        
        count = Int.read(b)
        
        chat_notifications_enabled = Bool.read(b) if flags & (1 << 1) else None
        gifts = TLObject.read(b)
        
        next_offset = String.read(b) if flags & (1 << 0) else None
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return SavedStarGifts(count=count, gifts=gifts, chats=chats, users=users, chat_notifications_enabled=chat_notifications_enabled, next_offset=next_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.chat_notifications_enabled is not None else 0
        flags |= (1 << 0) if self.next_offset is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.count))
        
        if self.chat_notifications_enabled is not None:
            b.write(Bool(self.chat_notifications_enabled))
        
        b.write(Vector(self.gifts))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
