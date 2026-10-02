# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from ..rpc_error import RPCError
from .bad_request_400 import (
    ChatAdminRequired,
    ChatSendInlineForbidden,
    ChatWriteForbidden,
    GroupcallForbidden,
    NotEligible,
    ParticipantJoinMissing,
    PeerIdInvalid,
    PollVoteRequired,
    PremiumAccountRequired,
    TakeoutRequired,
    UserBannedInChannel,
    UserBotInvalid,
    UserChannelsTooMuch,
    UserInvalid,
    UserIsBlocked,
    UserNotMutualContact,
    UserNotParticipant,
    VoiceMessagesForbidden,
)


class Forbidden(RPCError):
    """Forbidden"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = __doc__


class AccessDenied(Forbidden):
    """You cannot perform this request."""
    ID = "ACCESS_DENIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AllowPaymentRequired(Forbidden):
    """The user has enabled paid messages with {star_count} stars."""
    ID = "ALLOW_PAYMENT_REQUIRED_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "star_count"
    """``str``: Name of the property that holds this error's value"""

    @property
    def star_count(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class AnonymousReactionsDisabled(Forbidden):
    """Sorry, anonymous administrators cannot leave reactions or participate in polls."""
    ID = "ANONYMOUS_REACTIONS_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ApnsVerifyCheck(Forbidden):
    """The request can't be completed unless the APNs verification {value} is performed."""
    ID = "APNS_VERIFY_CHECK_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotAccessForbidden(Forbidden):
    """You can't access this bot."""
    ID = "BOT_ACCESS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotForumCreateForbidden(Forbidden):
    """This bot prevents users from creating or deleting topics."""
    ID = "BOT_FORUM_CREATE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotGuardNotSupported(Forbidden):
    """This bot is not designated as a "join guard" bot. This method is only available to bots that mediate user joins to chats. ."""
    ID = "BOT_GUARD_NOT_SUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotOwnerRequired(Forbidden):
    """You must be the owner of the bot to perform this action."""
    ID = "BOT_OWNER_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotVerifierForbidden(Forbidden):
    """This bot cannot assign [verification icons](https://core.telegram.org/api/bots/verification)."""
    ID = "BOT_VERIFIER_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BroadcastForbidden(Forbidden):
    """This request can't be used in channels."""
    ID = "BROADCAST_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelPublicGroupNa(Forbidden):
    """The channel/supergroup is not available."""
    ID = "CHANNEL_PUBLIC_GROUP_NA"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatActionForbidden(Forbidden):
    """You cannot execute this action."""
    ID = "CHAT_ACTION_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatAdminInviteRequired(Forbidden):
    """You don't have rights to invite other users."""
    ID = "CHAT_ADMIN_INVITE_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatAdminRequired403(ChatAdminRequired, Forbidden):
    """You must be an admin in this chat to do this."""
    ID = "CHAT_ADMIN_REQUIRED"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class ChatForbidden(Forbidden):
    """This chat is not available to the current user."""
    ID = "CHAT_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatGuestSendForbidden(Forbidden):
    """You need to join the discussion group before commenting, see [here »](https://core.telegram.org/api/discussion#requiring-users-to-join-the-group) for more info."""
    ID = "CHAT_GUEST_SEND_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendAudiosForbidden(Forbidden):
    """You can't send audio messages in this chat."""
    ID = "CHAT_SEND_AUDIOS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendDocsForbidden(Forbidden):
    """You can't send documents in this chat."""
    ID = "CHAT_SEND_DOCS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendGameForbidden(Forbidden):
    """You can't send a game to this chat."""
    ID = "CHAT_SEND_GAME_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendGifsForbidden(Forbidden):
    """You can't send animations in this chat."""
    ID = "CHAT_SEND_GIFS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendInlineForbidden403(ChatSendInlineForbidden, Forbidden):
    """You cannot use inline bots to send messages in this chat."""
    ID = "CHAT_SEND_INLINE_FORBIDDEN"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class ChatSendMediaForbidden(Forbidden):
    """You can't send media messages in this chat."""
    ID = "CHAT_SEND_MEDIA_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendPhotosForbidden(Forbidden):
    """You can't send photos in this chat."""
    ID = "CHAT_SEND_PHOTOS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendPlainForbidden(Forbidden):
    """You can't send non-media (text) messages in this chat."""
    ID = "CHAT_SEND_PLAIN_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendPollForbidden(Forbidden):
    """You can't send polls in this chat."""
    ID = "CHAT_SEND_POLL_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendRoundvideosForbidden(Forbidden):
    """You can't send video notes in this chat."""
    ID = "CHAT_SEND_ROUNDVIDEOS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendStickersForbidden(Forbidden):
    """You can't send stickers in this chat."""
    ID = "CHAT_SEND_STICKERS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendVideosForbidden(Forbidden):
    """You can't send videos in this chat."""
    ID = "CHAT_SEND_VIDEOS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendVoicesForbidden(Forbidden):
    """You can't send voice recordings in this chat."""
    ID = "CHAT_SEND_VOICES_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendWebpageForbidden(Forbidden):
    """You can't send web pages in this chat."""
    ID = "CHAT_SEND_WEBPAGE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatTypeInvalid(Forbidden):
    """The specified chat type is invalid."""
    ID = "CHAT_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatWriteForbidden403(ChatWriteForbidden, Forbidden):
    """You don't have rights to send messages in this chat."""
    ID = "CHAT_WRITE_FORBIDDEN"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class EditBotInviteForbidden(Forbidden):
    """Normal users can't edit invites that were created by bots."""
    ID = "EDIT_BOT_INVITE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallAlreadyStarted(Forbidden):
    """The groupcall has already started, you can join directly using [phone.joinGroupCall](https://core.telegram.org/method/phone.joinGroupCall)."""
    ID = "GROUPCALL_ALREADY_STARTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallChangeForbidden(Forbidden):
    """You cannot change this group call setting."""
    ID = "GROUPCALL_CHANGE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallForbidden403(GroupcallForbidden, Forbidden):
    """The group call has already ended."""
    ID = "GROUPCALL_FORBIDDEN"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class InlineBotRequired(Forbidden):
    """The action must be performed through an inline bot callback."""
    ID = "INLINE_BOT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class IntegrityCheckClassic(Forbidden):
    """The request can't be completed unless the classic Play Integrity verification {value} is performed."""
    ID = "INTEGRITY_CHECK_CLASSIC_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LiveDisabled(Forbidden):
    """Story is disabled server-side."""
    ID = "LIVE_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageAuthorRequired(Forbidden):
    """You are not the author of this message."""
    ID = "MESSAGE_AUTHOR_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageDeleteForbidden(Forbidden):
    """You don't have rights to delete one of the messages you tried to delete, most likely because it is a service message or you are not the author of them."""
    ID = "MESSAGE_DELETE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NotAllowed(Forbidden):
    """Not allowed."""
    ID = "NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NotEligible403(NotEligible, Forbidden):
    """The current user is not eligible for this action."""
    ID = "NOT_ELIGIBLE"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class ParticipantJoinMissing403(ParticipantJoinMissing, Forbidden):
    """Trying to enable a presentation, when the user hasn't joined the Video Chat with [phone.joinGroupCall](https://core.telegram.org/method/phone.joinGroupCall)."""
    ID = "PARTICIPANT_JOIN_MISSING"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PeerIdInvalid403(PeerIdInvalid, Forbidden):
    """The provided peer id is invalid."""
    ID = "PEER_ID_INVALID"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PollVoteRequired403(PollVoteRequired, Forbidden):
    """Cast a vote in the poll before calling this method."""
    ID = "POLL_VOTE_REQUIRED"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PremiumAccountRequired403(PremiumAccountRequired, Forbidden):
    """A premium account is required to execute this action."""
    ID = "PREMIUM_ACCOUNT_REQUIRED"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PrivacyPremiumRequired(Forbidden):
    """The user has restricted from sending messages or this action requires a [Telegram Premium subscription](https://core.telegram.org/api/premium)."""
    ID = "PRIVACY_PREMIUM_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PublicChannelMissing(Forbidden):
    """You can only export group call invite links for public chats or channels."""
    ID = "PUBLIC_CHANNEL_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RecaptchaCheck(Forbidden):
    """The request can't be completed unless reCAPTCHA verification {value} is performed."""
    ID = "RECAPTCHA_CHECK_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RightForbidden(Forbidden):
    """You don't have enough rights for this action, or you tried to set one or more admin rights that can't be applied to this kind of chat (channel or supergroup)."""
    ID = "RIGHT_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SensitiveChangeForbidden(Forbidden):
    """You can't change your sensitive content settings at this time."""
    ID = "SENSITIVE_CHANGE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftConvertBotNotAllowed(Forbidden):
    """You can't convert this gift to stars."""
    ID = "STARGIFT_CONVERT_BOT_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TakeoutRequired403(TakeoutRequired, Forbidden):
    """The method must be invoked inside a [takeout](https://core.telegram.org/api/takeout) session."""
    ID = "TAKEOUT_REQUIRED"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserBannedInChannel403(UserBannedInChannel, Forbidden):
    """You're banned from sending messages in supergroups/channels."""
    ID = "USER_BANNED_IN_CHANNEL"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserBotInvalid403(UserBotInvalid, Forbidden):
    """User accounts must provide the `bot` method parameter when calling this method. If there is no such method parameter, this method can only be invoked by bot accounts."""
    ID = "USER_BOT_INVALID"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserChannelsTooMuch403(UserChannelsTooMuch, Forbidden):
    """One of the users you tried to add is already in too many channels/supergroups."""
    ID = "USER_CHANNELS_TOO_MUCH"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserDeleted(Forbidden):
    """You can't send this secret message because the other participant deleted their account."""
    ID = "USER_DELETED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserDisallowedStargifts(Forbidden):
    """You can't send gifts to this user due to their privacy settings."""
    ID = "USER_DISALLOWED_STARGIFTS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserInvalid403(UserInvalid, Forbidden):
    """The provided user is invalid."""
    ID = "USER_INVALID"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserIsBlocked403(UserIsBlocked, Forbidden):
    """You were blocked by this user."""
    ID = "USER_IS_BLOCKED"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserNotMutualContact403(UserNotMutualContact, Forbidden):
    """The provided user is not a mutual contact."""
    ID = "USER_NOT_MUTUAL_CONTACT"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserNotParticipant403(UserNotParticipant, Forbidden):
    """You're not a member of this supergroup/channel."""
    ID = "USER_NOT_PARTICIPANT"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserPermissionDenied(Forbidden):
    """The user hasn't granted or has revoked the bot's access to change their emoji status using [bots.toggleUserEmojiStatusPermission](https://core.telegram.org/method/bots.toggleUserEmojiStatusPermission)."""
    ID = "USER_PERMISSION_DENIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserPrivacyRestricted(Forbidden):
    """The user's privacy settings do not allow you to do this."""
    ID = "USER_PRIVACY_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserRestricted(Forbidden):
    """You're limited/restricted by telegram. You can't perform this action."""
    ID = "USER_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VoiceMessagesForbidden403(VoiceMessagesForbidden, Forbidden):
    """This user's privacy settings forbid you from sending voice messages."""
    ID = "VOICE_MESSAGES_FORBIDDEN"
    """``str``: RPC Error ID"""
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = "Forbidden"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class YourPrivacyRestricted(Forbidden):
    """You cannot fetch the read date of this message because you have disallowed other users to do so for *your* messages; to fix, allow other users to see *your* exact last online date OR purchase a [Telegram Premium](https://core.telegram.org/api/premium) subscription."""
    ID = "YOUR_PRIVACY_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


