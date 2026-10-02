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


class PeerNotifySettings(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.PeerNotifySettings`.

    Details:
        - Layer: ``228``
        - ID: ``99622C0C``

    Parameters:
        show_previews (``bool``, *optional*):
            N/A

        silent (``bool``, *optional*):
            N/A

        mute_until (``int`` ``32-bit``, *optional*):
            N/A

        ios_sound (:obj:`NotificationSound <pyrogram.raw.base.NotificationSound>`, *optional*):
            N/A

        android_sound (:obj:`NotificationSound <pyrogram.raw.base.NotificationSound>`, *optional*):
            N/A

        other_sound (:obj:`NotificationSound <pyrogram.raw.base.NotificationSound>`, *optional*):
            N/A

        stories_muted (``bool``, *optional*):
            N/A

        stories_hide_sender (``bool``, *optional*):
            N/A

        stories_ios_sound (:obj:`NotificationSound <pyrogram.raw.base.NotificationSound>`, *optional*):
            N/A

        stories_android_sound (:obj:`NotificationSound <pyrogram.raw.base.NotificationSound>`, *optional*):
            N/A

        stories_other_sound (:obj:`NotificationSound <pyrogram.raw.base.NotificationSound>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetNotifySettings
    """

    __slots__: List[str] = ["show_previews", "silent", "mute_until", "ios_sound", "android_sound", "other_sound", "stories_muted", "stories_hide_sender", "stories_ios_sound", "stories_android_sound", "stories_other_sound"]

    ID = 0x99622c0c
    QUALNAME = "types.PeerNotifySettings"

    def __init__(self, *, show_previews: Optional[bool] = None, silent: Optional[bool] = None, mute_until: Optional[int] = None, ios_sound: "raw.base.NotificationSound" = None, android_sound: "raw.base.NotificationSound" = None, other_sound: "raw.base.NotificationSound" = None, stories_muted: Optional[bool] = None, stories_hide_sender: Optional[bool] = None, stories_ios_sound: "raw.base.NotificationSound" = None, stories_android_sound: "raw.base.NotificationSound" = None, stories_other_sound: "raw.base.NotificationSound" = None) -> None:
        self.show_previews = show_previews  # flags.0?Bool
        self.silent = silent  # flags.1?Bool
        self.mute_until = mute_until  # flags.2?int
        self.ios_sound = ios_sound  # flags.3?NotificationSound
        self.android_sound = android_sound  # flags.4?NotificationSound
        self.other_sound = other_sound  # flags.5?NotificationSound
        self.stories_muted = stories_muted  # flags.6?Bool
        self.stories_hide_sender = stories_hide_sender  # flags.7?Bool
        self.stories_ios_sound = stories_ios_sound  # flags.8?NotificationSound
        self.stories_android_sound = stories_android_sound  # flags.9?NotificationSound
        self.stories_other_sound = stories_other_sound  # flags.10?NotificationSound

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerNotifySettings":
        
        flags = Int.read(b)
        
        show_previews = Bool.read(b) if flags & (1 << 0) else None
        silent = Bool.read(b) if flags & (1 << 1) else None
        mute_until = Int.read(b) if flags & (1 << 2) else None
        ios_sound = TLObject.read(b) if flags & (1 << 3) else None
        
        android_sound = TLObject.read(b) if flags & (1 << 4) else None
        
        other_sound = TLObject.read(b) if flags & (1 << 5) else None
        
        stories_muted = Bool.read(b) if flags & (1 << 6) else None
        stories_hide_sender = Bool.read(b) if flags & (1 << 7) else None
        stories_ios_sound = TLObject.read(b) if flags & (1 << 8) else None
        
        stories_android_sound = TLObject.read(b) if flags & (1 << 9) else None
        
        stories_other_sound = TLObject.read(b) if flags & (1 << 10) else None
        
        return PeerNotifySettings(show_previews=show_previews, silent=silent, mute_until=mute_until, ios_sound=ios_sound, android_sound=android_sound, other_sound=other_sound, stories_muted=stories_muted, stories_hide_sender=stories_hide_sender, stories_ios_sound=stories_ios_sound, stories_android_sound=stories_android_sound, stories_other_sound=stories_other_sound)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.show_previews is not None else 0
        flags |= (1 << 1) if self.silent is not None else 0
        flags |= (1 << 2) if self.mute_until is not None else 0
        flags |= (1 << 3) if self.ios_sound is not None else 0
        flags |= (1 << 4) if self.android_sound is not None else 0
        flags |= (1 << 5) if self.other_sound is not None else 0
        flags |= (1 << 6) if self.stories_muted is not None else 0
        flags |= (1 << 7) if self.stories_hide_sender is not None else 0
        flags |= (1 << 8) if self.stories_ios_sound is not None else 0
        flags |= (1 << 9) if self.stories_android_sound is not None else 0
        flags |= (1 << 10) if self.stories_other_sound is not None else 0
        b.write(Int(flags))
        
        if self.show_previews is not None:
            b.write(Bool(self.show_previews))
        
        if self.silent is not None:
            b.write(Bool(self.silent))
        
        if self.mute_until is not None:
            b.write(Int(self.mute_until))
        
        if self.ios_sound is not None:
            b.write(self.ios_sound.write())
        
        if self.android_sound is not None:
            b.write(self.android_sound.write())
        
        if self.other_sound is not None:
            b.write(self.other_sound.write())
        
        if self.stories_muted is not None:
            b.write(Bool(self.stories_muted))
        
        if self.stories_hide_sender is not None:
            b.write(Bool(self.stories_hide_sender))
        
        if self.stories_ios_sound is not None:
            b.write(self.stories_ios_sound.write())
        
        if self.stories_android_sound is not None:
            b.write(self.stories_android_sound.write())
        
        if self.stories_other_sound is not None:
            b.write(self.stories_other_sound.write())
        
        return b.getvalue()
