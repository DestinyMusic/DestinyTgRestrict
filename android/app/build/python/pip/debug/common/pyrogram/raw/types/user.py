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


class User(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.User`.

    Details:
        - Layer: ``228``
        - ID: ``B1B8CC83``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        is_self (``bool``, *optional*):
            N/A

        contact (``bool``, *optional*):
            N/A

        mutual_contact (``bool``, *optional*):
            N/A

        deleted (``bool``, *optional*):
            N/A

        bot (``bool``, *optional*):
            N/A

        bot_chat_history (``bool``, *optional*):
            N/A

        bot_nochats (``bool``, *optional*):
            N/A

        verified (``bool``, *optional*):
            N/A

        restricted (``bool``, *optional*):
            N/A

        min (``bool``, *optional*):
            N/A

        bot_inline_geo (``bool``, *optional*):
            N/A

        support (``bool``, *optional*):
            N/A

        scam (``bool``, *optional*):
            N/A

        apply_min_photo (``bool``, *optional*):
            N/A

        fake (``bool``, *optional*):
            N/A

        bot_attach_menu (``bool``, *optional*):
            N/A

        premium (``bool``, *optional*):
            N/A

        attach_menu_enabled (``bool``, *optional*):
            N/A

        bot_can_edit (``bool``, *optional*):
            N/A

        close_friend (``bool``, *optional*):
            N/A

        stories_hidden (``bool``, *optional*):
            N/A

        stories_unavailable (``bool``, *optional*):
            N/A

        contact_require_premium (``bool``, *optional*):
            N/A

        bot_business (``bool``, *optional*):
            N/A

        bot_has_main_app (``bool``, *optional*):
            N/A

        bot_forum_view (``bool``, *optional*):
            N/A

        bot_forum_can_manage_topics (``bool``, *optional*):
            N/A

        bot_can_manage_bots (``bool``, *optional*):
            N/A

        bot_guestchat (``bool``, *optional*):
            N/A

        bot_guard (``bool``, *optional*):
            N/A

        access_hash (``int`` ``64-bit``, *optional*):
            N/A

        first_name (``str``, *optional*):
            N/A

        last_name (``str``, *optional*):
            N/A

        username (``str``, *optional*):
            N/A

        phone (``str``, *optional*):
            N/A

        photo (:obj:`UserProfilePhoto <pyrogram.raw.base.UserProfilePhoto>`, *optional*):
            N/A

        status (:obj:`UserStatus <pyrogram.raw.base.UserStatus>`, *optional*):
            N/A

        bot_info_version (``int`` ``32-bit``, *optional*):
            N/A

        restriction_reason (List of :obj:`RestrictionReason <pyrogram.raw.base.RestrictionReason>`, *optional*):
            N/A

        bot_inline_placeholder (``str``, *optional*):
            N/A

        lang_code (``str``, *optional*):
            N/A

        emoji_status (:obj:`EmojiStatus <pyrogram.raw.base.EmojiStatus>`, *optional*):
            N/A

        usernames (List of :obj:`Username <pyrogram.raw.base.Username>`, *optional*):
            N/A

        stories_max_id (:obj:`RecentStory <pyrogram.raw.base.RecentStory>`, *optional*):
            N/A

        color (:obj:`PeerColor <pyrogram.raw.base.PeerColor>`, *optional*):
            N/A

        profile_color (:obj:`PeerColor <pyrogram.raw.base.PeerColor>`, *optional*):
            N/A

        bot_active_users (``int`` ``32-bit``, *optional*):
            N/A

        bot_verification_icon (``int`` ``64-bit``, *optional*):
            N/A

        send_paid_messages_stars (``int`` ``64-bit``, *optional*):
            N/A

        linked_community_id (``int`` ``64-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 9 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.UpdateProfile
            account.UpdateUsername
            account.ChangePhone
            users.GetUsers
            contacts.ImportContactToken
            messages.GetFutureChatCreatorAfterLeave
            channels.GetMessageAuthor
            bots.GetAdminedBots
            bots.CreateBot
    """

    __slots__: List[str] = ["id", "is_self", "contact", "mutual_contact", "deleted", "bot", "bot_chat_history", "bot_nochats", "verified", "restricted", "min", "bot_inline_geo", "support", "scam", "apply_min_photo", "fake", "bot_attach_menu", "premium", "attach_menu_enabled", "bot_can_edit", "close_friend", "stories_hidden", "stories_unavailable", "contact_require_premium", "bot_business", "bot_has_main_app", "bot_forum_view", "bot_forum_can_manage_topics", "bot_can_manage_bots", "bot_guestchat", "bot_guard", "access_hash", "first_name", "last_name", "username", "phone", "photo", "status", "bot_info_version", "restriction_reason", "bot_inline_placeholder", "lang_code", "emoji_status", "usernames", "stories_max_id", "color", "profile_color", "bot_active_users", "bot_verification_icon", "send_paid_messages_stars", "linked_community_id"]

    ID = 0xb1b8cc83
    QUALNAME = "types.User"

    def __init__(self, *, id: int, is_self: Optional[bool] = None, contact: Optional[bool] = None, mutual_contact: Optional[bool] = None, deleted: Optional[bool] = None, bot: Optional[bool] = None, bot_chat_history: Optional[bool] = None, bot_nochats: Optional[bool] = None, verified: Optional[bool] = None, restricted: Optional[bool] = None, min: Optional[bool] = None, bot_inline_geo: Optional[bool] = None, support: Optional[bool] = None, scam: Optional[bool] = None, apply_min_photo: Optional[bool] = None, fake: Optional[bool] = None, bot_attach_menu: Optional[bool] = None, premium: Optional[bool] = None, attach_menu_enabled: Optional[bool] = None, bot_can_edit: Optional[bool] = None, close_friend: Optional[bool] = None, stories_hidden: Optional[bool] = None, stories_unavailable: Optional[bool] = None, contact_require_premium: Optional[bool] = None, bot_business: Optional[bool] = None, bot_has_main_app: Optional[bool] = None, bot_forum_view: Optional[bool] = None, bot_forum_can_manage_topics: Optional[bool] = None, bot_can_manage_bots: Optional[bool] = None, bot_guestchat: Optional[bool] = None, bot_guard: Optional[bool] = None, access_hash: Optional[int] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, username: Optional[str] = None, phone: Optional[str] = None, photo: "raw.base.UserProfilePhoto" = None, status: "raw.base.UserStatus" = None, bot_info_version: Optional[int] = None, restriction_reason: Optional[List["raw.base.RestrictionReason"]] = None, bot_inline_placeholder: Optional[str] = None, lang_code: Optional[str] = None, emoji_status: "raw.base.EmojiStatus" = None, usernames: Optional[List["raw.base.Username"]] = None, stories_max_id: "raw.base.RecentStory" = None, color: "raw.base.PeerColor" = None, profile_color: "raw.base.PeerColor" = None, bot_active_users: Optional[int] = None, bot_verification_icon: Optional[int] = None, send_paid_messages_stars: Optional[int] = None, linked_community_id: Optional[int] = None) -> None:
        self.id = id  # long
        self.is_self = is_self  # flags.10?true
        self.contact = contact  # flags.11?true
        self.mutual_contact = mutual_contact  # flags.12?true
        self.deleted = deleted  # flags.13?true
        self.bot = bot  # flags.14?true
        self.bot_chat_history = bot_chat_history  # flags.15?true
        self.bot_nochats = bot_nochats  # flags.16?true
        self.verified = verified  # flags.17?true
        self.restricted = restricted  # flags.18?true
        self.min = min  # flags.20?true
        self.bot_inline_geo = bot_inline_geo  # flags.21?true
        self.support = support  # flags.23?true
        self.scam = scam  # flags.24?true
        self.apply_min_photo = apply_min_photo  # flags.25?true
        self.fake = fake  # flags.26?true
        self.bot_attach_menu = bot_attach_menu  # flags.27?true
        self.premium = premium  # flags.28?true
        self.attach_menu_enabled = attach_menu_enabled  # flags.29?true
        self.bot_can_edit = bot_can_edit  # flags2.1?true
        self.close_friend = close_friend  # flags2.2?true
        self.stories_hidden = stories_hidden  # flags2.3?true
        self.stories_unavailable = stories_unavailable  # flags2.4?true
        self.contact_require_premium = contact_require_premium  # flags2.10?true
        self.bot_business = bot_business  # flags2.11?true
        self.bot_has_main_app = bot_has_main_app  # flags2.13?true
        self.bot_forum_view = bot_forum_view  # flags2.16?true
        self.bot_forum_can_manage_topics = bot_forum_can_manage_topics  # flags2.17?true
        self.bot_can_manage_bots = bot_can_manage_bots  # flags2.18?true
        self.bot_guestchat = bot_guestchat  # flags2.19?true
        self.bot_guard = bot_guard  # flags2.20?true
        self.access_hash = access_hash  # flags.0?long
        self.first_name = first_name  # flags.1?string
        self.last_name = last_name  # flags.2?string
        self.username = username  # flags.3?string
        self.phone = phone  # flags.4?string
        self.photo = photo  # flags.5?UserProfilePhoto
        self.status = status  # flags.6?UserStatus
        self.bot_info_version = bot_info_version  # flags.14?int
        self.restriction_reason = restriction_reason  # flags.18?Vector<RestrictionReason>
        self.bot_inline_placeholder = bot_inline_placeholder  # flags.19?string
        self.lang_code = lang_code  # flags.22?string
        self.emoji_status = emoji_status  # flags.30?EmojiStatus
        self.usernames = usernames  # flags2.0?Vector<Username>
        self.stories_max_id = stories_max_id  # flags2.5?RecentStory
        self.color = color  # flags2.8?PeerColor
        self.profile_color = profile_color  # flags2.9?PeerColor
        self.bot_active_users = bot_active_users  # flags2.12?int
        self.bot_verification_icon = bot_verification_icon  # flags2.14?long
        self.send_paid_messages_stars = send_paid_messages_stars  # flags2.15?long
        self.linked_community_id = linked_community_id  # flags2.21?long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "User":
        
        flags = Int.read(b)
        
        is_self = True if flags & (1 << 10) else False
        contact = True if flags & (1 << 11) else False
        mutual_contact = True if flags & (1 << 12) else False
        deleted = True if flags & (1 << 13) else False
        bot = True if flags & (1 << 14) else False
        bot_chat_history = True if flags & (1 << 15) else False
        bot_nochats = True if flags & (1 << 16) else False
        verified = True if flags & (1 << 17) else False
        restricted = True if flags & (1 << 18) else False
        min = True if flags & (1 << 20) else False
        bot_inline_geo = True if flags & (1 << 21) else False
        support = True if flags & (1 << 23) else False
        scam = True if flags & (1 << 24) else False
        apply_min_photo = True if flags & (1 << 25) else False
        fake = True if flags & (1 << 26) else False
        bot_attach_menu = True if flags & (1 << 27) else False
        premium = True if flags & (1 << 28) else False
        attach_menu_enabled = True if flags & (1 << 29) else False
        flags2 = Int.read(b)
        
        bot_can_edit = True if flags2 & (1 << 1) else False
        close_friend = True if flags2 & (1 << 2) else False
        stories_hidden = True if flags2 & (1 << 3) else False
        stories_unavailable = True if flags2 & (1 << 4) else False
        contact_require_premium = True if flags2 & (1 << 10) else False
        bot_business = True if flags2 & (1 << 11) else False
        bot_has_main_app = True if flags2 & (1 << 13) else False
        bot_forum_view = True if flags2 & (1 << 16) else False
        bot_forum_can_manage_topics = True if flags2 & (1 << 17) else False
        bot_can_manage_bots = True if flags2 & (1 << 18) else False
        bot_guestchat = True if flags2 & (1 << 19) else False
        bot_guard = True if flags2 & (1 << 20) else False
        id = Long.read(b)
        
        access_hash = Long.read(b) if flags & (1 << 0) else None
        first_name = String.read(b) if flags & (1 << 1) else None
        last_name = String.read(b) if flags & (1 << 2) else None
        username = String.read(b) if flags & (1 << 3) else None
        phone = String.read(b) if flags & (1 << 4) else None
        photo = TLObject.read(b) if flags & (1 << 5) else None
        
        status = TLObject.read(b) if flags & (1 << 6) else None
        
        bot_info_version = Int.read(b) if flags & (1 << 14) else None
        restriction_reason = TLObject.read(b) if flags & (1 << 18) else []
        
        bot_inline_placeholder = String.read(b) if flags & (1 << 19) else None
        lang_code = String.read(b) if flags & (1 << 22) else None
        emoji_status = TLObject.read(b) if flags & (1 << 30) else None
        
        usernames = TLObject.read(b) if flags2 & (1 << 0) else []
        
        stories_max_id = TLObject.read(b) if flags2 & (1 << 5) else None
        
        color = TLObject.read(b) if flags2 & (1 << 8) else None
        
        profile_color = TLObject.read(b) if flags2 & (1 << 9) else None
        
        bot_active_users = Int.read(b) if flags2 & (1 << 12) else None
        bot_verification_icon = Long.read(b) if flags2 & (1 << 14) else None
        send_paid_messages_stars = Long.read(b) if flags2 & (1 << 15) else None
        linked_community_id = Long.read(b) if flags2 & (1 << 21) else None
        return User(id=id, is_self=is_self, contact=contact, mutual_contact=mutual_contact, deleted=deleted, bot=bot, bot_chat_history=bot_chat_history, bot_nochats=bot_nochats, verified=verified, restricted=restricted, min=min, bot_inline_geo=bot_inline_geo, support=support, scam=scam, apply_min_photo=apply_min_photo, fake=fake, bot_attach_menu=bot_attach_menu, premium=premium, attach_menu_enabled=attach_menu_enabled, bot_can_edit=bot_can_edit, close_friend=close_friend, stories_hidden=stories_hidden, stories_unavailable=stories_unavailable, contact_require_premium=contact_require_premium, bot_business=bot_business, bot_has_main_app=bot_has_main_app, bot_forum_view=bot_forum_view, bot_forum_can_manage_topics=bot_forum_can_manage_topics, bot_can_manage_bots=bot_can_manage_bots, bot_guestchat=bot_guestchat, bot_guard=bot_guard, access_hash=access_hash, first_name=first_name, last_name=last_name, username=username, phone=phone, photo=photo, status=status, bot_info_version=bot_info_version, restriction_reason=restriction_reason, bot_inline_placeholder=bot_inline_placeholder, lang_code=lang_code, emoji_status=emoji_status, usernames=usernames, stories_max_id=stories_max_id, color=color, profile_color=profile_color, bot_active_users=bot_active_users, bot_verification_icon=bot_verification_icon, send_paid_messages_stars=send_paid_messages_stars, linked_community_id=linked_community_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 10) if self.is_self else 0
        flags |= (1 << 11) if self.contact else 0
        flags |= (1 << 12) if self.mutual_contact else 0
        flags |= (1 << 13) if self.deleted else 0
        flags |= (1 << 14) if self.bot else 0
        flags |= (1 << 15) if self.bot_chat_history else 0
        flags |= (1 << 16) if self.bot_nochats else 0
        flags |= (1 << 17) if self.verified else 0
        flags |= (1 << 18) if self.restricted else 0
        flags |= (1 << 20) if self.min else 0
        flags |= (1 << 21) if self.bot_inline_geo else 0
        flags |= (1 << 23) if self.support else 0
        flags |= (1 << 24) if self.scam else 0
        flags |= (1 << 25) if self.apply_min_photo else 0
        flags |= (1 << 26) if self.fake else 0
        flags |= (1 << 27) if self.bot_attach_menu else 0
        flags |= (1 << 28) if self.premium else 0
        flags |= (1 << 29) if self.attach_menu_enabled else 0
        flags |= (1 << 0) if self.access_hash is not None else 0
        flags |= (1 << 1) if self.first_name is not None else 0
        flags |= (1 << 2) if self.last_name is not None else 0
        flags |= (1 << 3) if self.username is not None else 0
        flags |= (1 << 4) if self.phone is not None else 0
        flags |= (1 << 5) if self.photo is not None else 0
        flags |= (1 << 6) if self.status is not None else 0
        flags |= (1 << 14) if self.bot_info_version is not None else 0
        flags |= (1 << 18) if self.restriction_reason else 0
        flags |= (1 << 19) if self.bot_inline_placeholder is not None else 0
        flags |= (1 << 22) if self.lang_code is not None else 0
        flags |= (1 << 30) if self.emoji_status is not None else 0
        b.write(Int(flags))
        flags2 = 0
        flags2 |= (1 << 1) if self.bot_can_edit else 0
        flags2 |= (1 << 2) if self.close_friend else 0
        flags2 |= (1 << 3) if self.stories_hidden else 0
        flags2 |= (1 << 4) if self.stories_unavailable else 0
        flags2 |= (1 << 10) if self.contact_require_premium else 0
        flags2 |= (1 << 11) if self.bot_business else 0
        flags2 |= (1 << 13) if self.bot_has_main_app else 0
        flags2 |= (1 << 16) if self.bot_forum_view else 0
        flags2 |= (1 << 17) if self.bot_forum_can_manage_topics else 0
        flags2 |= (1 << 18) if self.bot_can_manage_bots else 0
        flags2 |= (1 << 19) if self.bot_guestchat else 0
        flags2 |= (1 << 20) if self.bot_guard else 0
        flags2 |= (1 << 0) if self.usernames else 0
        flags2 |= (1 << 5) if self.stories_max_id is not None else 0
        flags2 |= (1 << 8) if self.color is not None else 0
        flags2 |= (1 << 9) if self.profile_color is not None else 0
        flags2 |= (1 << 12) if self.bot_active_users is not None else 0
        flags2 |= (1 << 14) if self.bot_verification_icon is not None else 0
        flags2 |= (1 << 15) if self.send_paid_messages_stars is not None else 0
        flags2 |= (1 << 21) if self.linked_community_id is not None else 0
        b.write(Int(flags2))
        
        b.write(Long(self.id))
        
        if self.access_hash is not None:
            b.write(Long(self.access_hash))
        
        if self.first_name is not None:
            b.write(String(self.first_name))
        
        if self.last_name is not None:
            b.write(String(self.last_name))
        
        if self.username is not None:
            b.write(String(self.username))
        
        if self.phone is not None:
            b.write(String(self.phone))
        
        if self.photo is not None:
            b.write(self.photo.write())
        
        if self.status is not None:
            b.write(self.status.write())
        
        if self.bot_info_version is not None:
            b.write(Int(self.bot_info_version))
        
        if self.restriction_reason:
            b.write(Vector(self.restriction_reason))
        
        if self.bot_inline_placeholder is not None:
            b.write(String(self.bot_inline_placeholder))
        
        if self.lang_code is not None:
            b.write(String(self.lang_code))
        
        if self.emoji_status is not None:
            b.write(self.emoji_status.write())
        
        if self.usernames:
            b.write(Vector(self.usernames))
        
        if self.stories_max_id is not None:
            b.write(self.stories_max_id.write())
        
        if self.color is not None:
            b.write(self.color.write())
        
        if self.profile_color is not None:
            b.write(self.profile_color.write())
        
        if self.bot_active_users is not None:
            b.write(Int(self.bot_active_users))
        
        if self.bot_verification_icon is not None:
            b.write(Long(self.bot_verification_icon))
        
        if self.send_paid_messages_stars is not None:
            b.write(Long(self.send_paid_messages_stars))
        
        if self.linked_community_id is not None:
            b.write(Long(self.linked_community_id))
        
        return b.getvalue()
