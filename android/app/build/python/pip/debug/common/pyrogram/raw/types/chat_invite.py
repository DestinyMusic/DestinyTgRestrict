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


class ChatInvite(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.ChatInvite`.

    Details:
        - Layer: ``228``
        - ID: ``5C9D3702``

    Parameters:
        title (``str``):
            N/A

        photo (:obj:`Photo <pyrogram.raw.base.Photo>`):
            N/A

        participants_count (``int`` ``32-bit``):
            N/A

        color (``int`` ``32-bit``):
            N/A

        channel (``bool``, *optional*):
            N/A

        broadcast (``bool``, *optional*):
            N/A

        public (``bool``, *optional*):
            N/A

        megagroup (``bool``, *optional*):
            N/A

        request_needed (``bool``, *optional*):
            N/A

        verified (``bool``, *optional*):
            N/A

        scam (``bool``, *optional*):
            N/A

        fake (``bool``, *optional*):
            N/A

        can_refulfill_subscription (``bool``, *optional*):
            N/A

        about (``str``, *optional*):
            N/A

        participants (List of :obj:`User <pyrogram.raw.base.User>`, *optional*):
            N/A

        subscription_pricing (:obj:`StarsSubscriptionPricing <pyrogram.raw.base.StarsSubscriptionPricing>`, *optional*):
            N/A

        subscription_form_id (``int`` ``64-bit``, *optional*):
            N/A

        bot_verification (:obj:`BotVerification <pyrogram.raw.base.BotVerification>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.CheckChatInvite
    """

    __slots__: List[str] = ["title", "photo", "participants_count", "color", "channel", "broadcast", "public", "megagroup", "request_needed", "verified", "scam", "fake", "can_refulfill_subscription", "about", "participants", "subscription_pricing", "subscription_form_id", "bot_verification"]

    ID = 0x5c9d3702
    QUALNAME = "types.ChatInvite"

    def __init__(self, *, title: str, photo: "raw.base.Photo", participants_count: int, color: int, channel: Optional[bool] = None, broadcast: Optional[bool] = None, public: Optional[bool] = None, megagroup: Optional[bool] = None, request_needed: Optional[bool] = None, verified: Optional[bool] = None, scam: Optional[bool] = None, fake: Optional[bool] = None, can_refulfill_subscription: Optional[bool] = None, about: Optional[str] = None, participants: Optional[List["raw.base.User"]] = None, subscription_pricing: "raw.base.StarsSubscriptionPricing" = None, subscription_form_id: Optional[int] = None, bot_verification: "raw.base.BotVerification" = None) -> None:
        self.title = title  # string
        self.photo = photo  # Photo
        self.participants_count = participants_count  # int
        self.color = color  # int
        self.channel = channel  # flags.0?true
        self.broadcast = broadcast  # flags.1?true
        self.public = public  # flags.2?true
        self.megagroup = megagroup  # flags.3?true
        self.request_needed = request_needed  # flags.6?true
        self.verified = verified  # flags.7?true
        self.scam = scam  # flags.8?true
        self.fake = fake  # flags.9?true
        self.can_refulfill_subscription = can_refulfill_subscription  # flags.11?true
        self.about = about  # flags.5?string
        self.participants = participants  # flags.4?Vector<User>
        self.subscription_pricing = subscription_pricing  # flags.10?StarsSubscriptionPricing
        self.subscription_form_id = subscription_form_id  # flags.12?long
        self.bot_verification = bot_verification  # flags.13?BotVerification

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInvite":
        
        flags = Int.read(b)
        
        channel = True if flags & (1 << 0) else False
        broadcast = True if flags & (1 << 1) else False
        public = True if flags & (1 << 2) else False
        megagroup = True if flags & (1 << 3) else False
        request_needed = True if flags & (1 << 6) else False
        verified = True if flags & (1 << 7) else False
        scam = True if flags & (1 << 8) else False
        fake = True if flags & (1 << 9) else False
        can_refulfill_subscription = True if flags & (1 << 11) else False
        title = String.read(b)
        
        about = String.read(b) if flags & (1 << 5) else None
        photo = TLObject.read(b)
        
        participants_count = Int.read(b)
        
        participants = TLObject.read(b) if flags & (1 << 4) else []
        
        color = Int.read(b)
        
        subscription_pricing = TLObject.read(b) if flags & (1 << 10) else None
        
        subscription_form_id = Long.read(b) if flags & (1 << 12) else None
        bot_verification = TLObject.read(b) if flags & (1 << 13) else None
        
        return ChatInvite(title=title, photo=photo, participants_count=participants_count, color=color, channel=channel, broadcast=broadcast, public=public, megagroup=megagroup, request_needed=request_needed, verified=verified, scam=scam, fake=fake, can_refulfill_subscription=can_refulfill_subscription, about=about, participants=participants, subscription_pricing=subscription_pricing, subscription_form_id=subscription_form_id, bot_verification=bot_verification)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.channel else 0
        flags |= (1 << 1) if self.broadcast else 0
        flags |= (1 << 2) if self.public else 0
        flags |= (1 << 3) if self.megagroup else 0
        flags |= (1 << 6) if self.request_needed else 0
        flags |= (1 << 7) if self.verified else 0
        flags |= (1 << 8) if self.scam else 0
        flags |= (1 << 9) if self.fake else 0
        flags |= (1 << 11) if self.can_refulfill_subscription else 0
        flags |= (1 << 5) if self.about is not None else 0
        flags |= (1 << 4) if self.participants else 0
        flags |= (1 << 10) if self.subscription_pricing is not None else 0
        flags |= (1 << 12) if self.subscription_form_id is not None else 0
        flags |= (1 << 13) if self.bot_verification is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.title))
        
        if self.about is not None:
            b.write(String(self.about))
        
        b.write(self.photo.write())
        
        b.write(Int(self.participants_count))
        
        if self.participants:
            b.write(Vector(self.participants))
        
        b.write(Int(self.color))
        
        if self.subscription_pricing is not None:
            b.write(self.subscription_pricing.write())
        
        if self.subscription_form_id is not None:
            b.write(Long(self.subscription_form_id))
        
        if self.bot_verification is not None:
            b.write(self.bot_verification.write())
        
        return b.getvalue()
