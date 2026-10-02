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
    BannedRightsInvalid,
    ChannelPrivate,
    ChannelTooLarge,
    ChatForwardsRestricted,
    FreshChangeAdminsForbidden,
    InviteHashExpired,
    PeerIdInvalid,
    PhoneNumberInvalid,
    PrecheckoutFailed,
    StargiftMessageInvalid,
    StargiftUsageLimited,
    StarsFormAmountMismatch,
    StickersetInvalid,
    TopicClosed,
    TopicDeleted,
    TranslationsDisabled,
    UserpicUploadRequired,
)
from .forbidden_403 import (
    AllowPaymentRequired,
    PrivacyPremiumRequired,
    UserRestricted,
)


class NotAcceptable(RPCError):
    """Not Acceptable"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = __doc__


class AicomposeErrorOccured(NotAcceptable):
    """The composeTextWithAi method encountered an error."""
    ID = "AICOMPOSE_ERROR_OCCURED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AllowPaymentRequired406(AllowPaymentRequired, NotAcceptable):
    """This peer only accepts [paid messages](https://core.telegram.org/api/paid-messages): this error is only emitted for older layers without paid messages support, so the client must be updated in order to use paid messages."""
    ID = "ALLOW_PAYMENT_REQUIRED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__

    # Unlike the `AllowPaymentRequired` it subclasses, this error carries nothing.
    VALUE_NAME = RPCError.VALUE_NAME


class ApiGiftRestrictedUpdateApp(NotAcceptable):
    """Please update your Telegram app to send this gift."""
    ID = "API_GIFT_RESTRICTED_UPDATE_APP"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthKeyDuplicated(NotAcceptable):
    """The same authorization key (session file) was used in more than one place simultaneously, the current session was invalidated by the server for security reasons! You must delete your session file and log in again with your phone number or bot token."""
    ID = "AUTH_KEY_DUPLICATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BannedRightsInvalid406(BannedRightsInvalid, NotAcceptable):
    """You provided some invalid flags in the banned rights."""
    ID = "BANNED_RIGHTS_INVALID"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class BotPrecheckoutFailed(NotAcceptable):
    """Bot precheckout is failed."""
    ID = "BOT_PRECHECKOUT_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessAddressActive(NotAcceptable):
    """The user is currently advertising a [Business Location](https://core.telegram.org/api/business#location), the location may only be changed (or removed) using [account.updateBusinessLocation »](https://core.telegram.org/method/account.updateBusinessLocation)."""
    ID = "BUSINESS_ADDRESS_ACTIVE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallProtocolCompatLayerInvalid(NotAcceptable):
    """The other side of the call does not support any of the VoIP protocols supported by the local client, as specified by the `protocol.layer` and `protocol.library_versions` fields."""
    ID = "CALL_PROTOCOL_COMPAT_LAYER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelPrivate406(ChannelPrivate, NotAcceptable):
    """The channel/supergroup is not accessible."""
    ID = "CHANNEL_PRIVATE"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class ChannelTooLarge406(ChannelTooLarge, NotAcceptable):
    """Channel is too large to be deleted. Contact support for removal."""
    ID = "CHANNEL_TOO_LARGE"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class ChatForwardsRestricted406(ChatForwardsRestricted, NotAcceptable):
    """You can't forward messages from a protected chat."""
    ID = "CHAT_FORWARDS_RESTRICTED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class EditMessageTempRestricted(NotAcceptable):
    """Message editing is temporarily forbidden for this user due to regulatory restrictions."""
    ID = "EDIT_MESSAGE_TEMP_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilerefUpgradeNeeded(NotAcceptable):
    """The [file references](https://core.telegram.org/api/file_reference) has expired and you must use a refreshed one by obtaining the original media message."""
    ID = "FILEREF_UPGRADE_NEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FreshChangeAdminsForbidden406(FreshChangeAdminsForbidden, NotAcceptable):
    """You were just elected admin, you can't add or modify other admins yet."""
    ID = "FRESH_CHANGE_ADMINS_FORBIDDEN"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class FreshChangePhoneForbidden(NotAcceptable):
    """You can't change your phone number because your session was logged-in recently, please wait at least 24 hours."""
    ID = "FRESH_CHANGE_PHONE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FreshResetAuthorisationForbidden(NotAcceptable):
    """You can't terminate other authorized sessions because the current was logged-in recently, please wait at least 24 hours."""
    ID = "FRESH_RESET_AUTHORISATION_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GiftcodeNotAllowed(NotAcceptable):
    """Giftcode not allowed."""
    ID = "GIFTCODE_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteHashExpired406(InviteHashExpired, NotAcceptable):
    """The chat the user tried to join has expired and is not valid anymore."""
    ID = "INVITE_HASH_EXPIRED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PaymentUnsupported(NotAcceptable):
    """A detailed description of the error will be received separately as described [here »](https://core.telegram.org/api/errors#406-not-acceptable)."""
    ID = "PAYMENT_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PeerIdInvalid406(PeerIdInvalid, NotAcceptable):
    """The provided peer id is invalid."""
    ID = "PEER_ID_INVALID"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PhoneNumberInvalid406(PhoneNumberInvalid, NotAcceptable):
    """The phone number is invalid."""
    ID = "PHONE_NUMBER_INVALID"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PhonePasswordFlood(NotAcceptable):
    """You have tried to log-in too many times."""
    ID = "PHONE_PASSWORD_FLOOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollCountryRestricted(NotAcceptable):
    """Users from the current user's country cannot vote in this [country-restricted poll &raquo;](https://core.telegram.org/api/poll#country-restricted-polls)."""
    ID = "POLL_COUNTRY_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollMemberRestricted(NotAcceptable):
    """Only channel subscribers can vote in this poll."""
    ID = "POLL_MEMBER_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PrecheckoutFailed406(PrecheckoutFailed, NotAcceptable):
    """Precheckout is failed."""
    ID = "PRECHECKOUT_FAILED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class PremiumCurrentlyUnavailable(NotAcceptable):
    """You cannot currently purchase a Premium subscription."""
    ID = "PREMIUM_CURRENTLY_UNAVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PreviousChatImportActiveWaitMin(NotAcceptable):
    """Import for this chat is already in progress, wait {minutes} minutes before starting a new one."""
    ID = "PREVIOUS_CHAT_IMPORT_ACTIVE_WAIT_XMIN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "minutes"
    """``str``: Name of the property that holds this error's value"""

    @property
    def minutes(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class PrivacyPremiumRequired406(PrivacyPremiumRequired, NotAcceptable):
    """You need a [Telegram Premium subscription](https://core.telegram.org/api/premium) to send a message to this user."""
    ID = "PRIVACY_PREMIUM_REQUIRED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class SendCodeUnavailable(NotAcceptable):
    """Returned when all available options for this type of number were already used (e.g. flash-call, then SMS, then this error might be returned to trigger a second resend)."""
    ID = "SEND_CODE_UNAVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftExportInProgress(NotAcceptable):
    """You can't send this gift at the moment as the withdrawal process to the blockchain has already started."""
    ID = "STARGIFT_EXPORT_IN_PROGRESS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftMessageInvalid406(StargiftMessageInvalid, NotAcceptable):
    """The provided message for this gift is invalid."""
    ID = "STARGIFT_MESSAGE_INVALID"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class StargiftUsageLimited406(StargiftUsageLimited, NotAcceptable):
    """Star gift usage limited."""
    ID = "STARGIFT_USAGE_LIMITED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class StarsFormAmountMismatch406(StarsFormAmountMismatch, NotAcceptable):
    """Stars form amount mismatch."""
    ID = "STARS_FORM_AMOUNT_MISMATCH"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class StickersetInvalid406(StickersetInvalid, NotAcceptable):
    """The provided sticker set is invalid."""
    ID = "STICKERSET_INVALID"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class StickersetOwnerAnonymous(NotAcceptable):
    """The provided sticker set can't be used as the group's sticker set because it was created by one of its anonymous admins."""
    ID = "STICKERSET_OWNER_ANONYMOUS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicClosed406(TopicClosed, NotAcceptable):
    """This topic was closed, you can't send messages to it anymore."""
    ID = "TOPIC_CLOSED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class TopicDeleted406(TopicDeleted, NotAcceptable):
    """The specified topic was deleted."""
    ID = "TOPIC_DELETED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class TranslationsDisabled406(TranslationsDisabled, NotAcceptable):
    """Translations are unavailable, a detailed and localized description for the error will be emitted via an [updateServiceNotification as specified here](https://core.telegram.org/api/errors#406-not-acceptable)."""
    ID = "TRANSLATIONS_DISABLED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UpdateAppToLogin(NotAcceptable):
    """Please update your app to login."""
    ID = "UPDATE_APP_TO_LOGIN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserpicPrivacyRequired(NotAcceptable):
    """You need to disable privacy settings for your profile picture in order to make your geolocation public."""
    ID = "USERPIC_PRIVACY_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserpicUploadRequired406(UserpicUploadRequired, NotAcceptable):
    """You must have a profile picture to publish your geolocation."""
    ID = "USERPIC_UPLOAD_REQUIRED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class UserRestricted406(UserRestricted, NotAcceptable):
    """You're limited/restricted by telegram. You can't perform this action."""
    ID = "USER_RESTRICTED"
    """``str``: RPC Error ID"""
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = "Not Acceptable"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


