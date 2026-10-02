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


class ReactionsNotifySettings(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.ReactionsNotifySettings`.

    Details:
        - Layer: ``228``
        - ID: ``71E4EA58``

    Parameters:
        sound (:obj:`NotificationSound <pyrogram.raw.base.NotificationSound>`):
            N/A

        show_previews (``bool``):
            N/A

        messages_notify_from (:obj:`ReactionNotificationsFrom <pyrogram.raw.base.ReactionNotificationsFrom>`, *optional*):
            N/A

        stories_notify_from (:obj:`ReactionNotificationsFrom <pyrogram.raw.base.ReactionNotificationsFrom>`, *optional*):
            N/A

        poll_votes_notify_from (:obj:`ReactionNotificationsFrom <pyrogram.raw.base.ReactionNotificationsFrom>`, *optional*):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetReactionsNotifySettings
            account.SetReactionsNotifySettings
    """

    __slots__: List[str] = ["sound", "show_previews", "messages_notify_from", "stories_notify_from", "poll_votes_notify_from"]

    ID = 0x71e4ea58
    QUALNAME = "types.ReactionsNotifySettings"

    def __init__(self, *, sound: "raw.base.NotificationSound", show_previews: bool, messages_notify_from: "raw.base.ReactionNotificationsFrom" = None, stories_notify_from: "raw.base.ReactionNotificationsFrom" = None, poll_votes_notify_from: "raw.base.ReactionNotificationsFrom" = None) -> None:
        self.sound = sound  # NotificationSound
        self.show_previews = show_previews  # Bool
        self.messages_notify_from = messages_notify_from  # flags.0?ReactionNotificationsFrom
        self.stories_notify_from = stories_notify_from  # flags.1?ReactionNotificationsFrom
        self.poll_votes_notify_from = poll_votes_notify_from  # flags.2?ReactionNotificationsFrom

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReactionsNotifySettings":
        
        flags = Int.read(b)
        
        messages_notify_from = TLObject.read(b) if flags & (1 << 0) else None
        
        stories_notify_from = TLObject.read(b) if flags & (1 << 1) else None
        
        poll_votes_notify_from = TLObject.read(b) if flags & (1 << 2) else None
        
        sound = TLObject.read(b)
        
        show_previews = Bool.read(b)
        
        return ReactionsNotifySettings(sound=sound, show_previews=show_previews, messages_notify_from=messages_notify_from, stories_notify_from=stories_notify_from, poll_votes_notify_from=poll_votes_notify_from)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.messages_notify_from is not None else 0
        flags |= (1 << 1) if self.stories_notify_from is not None else 0
        flags |= (1 << 2) if self.poll_votes_notify_from is not None else 0
        b.write(Int(flags))
        
        if self.messages_notify_from is not None:
            b.write(self.messages_notify_from.write())
        
        if self.stories_notify_from is not None:
            b.write(self.stories_notify_from.write())
        
        if self.poll_votes_notify_from is not None:
            b.write(self.poll_votes_notify_from.write())
        
        b.write(self.sound.write())
        
        b.write(Bool(self.show_previews))
        
        return b.getvalue()
