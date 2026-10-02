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
from .see_other_303 import (
    FileMigrate,
)


class BadRequest(RPCError):
    """Bad Request"""
    CODE = 400
    """``int``: RPC Error Code"""
    NAME = __doc__


class AboutTooLong(BadRequest):
    """The provided about/bio text is too long."""
    ID = "ABOUT_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AccessTokenExpired(BadRequest):
    """The bot token has expired."""
    ID = "ACCESS_TOKEN_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AccessTokenInvalid(BadRequest):
    """The bot access token is invalid."""
    ID = "ACCESS_TOKEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AddressInvalid(BadRequest):
    """The specified geopoint address is invalid."""
    ID = "ADDRESS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AdminsTooMuch(BadRequest):
    """The chat has too many administrators."""
    ID = "ADMINS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AdminIdInvalid(BadRequest):
    """The specified admin ID is invalid."""
    ID = "ADMIN_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AdminRankEmojiNotAllowed(BadRequest):
    """Emoji are not allowed in custom administrator titles."""
    ID = "ADMIN_RANK_EMOJI_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AdminRankInvalid(BadRequest):
    """The custom administrator title is invalid or too long."""
    ID = "ADMIN_RANK_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AdminRightsEmpty(BadRequest):
    """The chatAdminRights constructor passed in keyboardButtonRequestPeer.peer_type.user_admin_rights has no rights set (i.e. flags is 0)."""
    ID = "ADMIN_RIGHTS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AdExpired(BadRequest):
    """The ad has expired (too old or not found)."""
    ID = "AD_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AicomposeFloodPremium(BadRequest):
    """You've reached the daily limit of AI text transformations, upgrade to [Telegram Premium](https://core.telegram.org/api/premium) to get **50x** times more AI text transformations per day!"""
    ID = "AICOMPOSE_FLOOD_PREMIUM"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AicomposeToneInvalid(BadRequest):
    """The specified tone is invalid."""
    ID = "AICOMPOSE_TONE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AicomposeToneTitleInvalid(BadRequest):
    """The specified tone title is invalid."""
    ID = "AICOMPOSE_TONE_TITLE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AiComposeTaskMissing(BadRequest):
    """The text composition style is missing."""
    ID = "AI_COMPOSE_TASK_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AlbumPhotosTooMany(BadRequest):
    """Too many photos were included in the album."""
    ID = "ALBUM_PHOTOS_TOO_MANY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AnonymousOpenInvalid(BadRequest):
    """allow_adding_options is not supported for anonymous polls and quizzes."""
    ID = "ANONYMOUS_OPEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AnswerMediaTypeInvalid(BadRequest):
    """The option media type at index {index} is invalid."""
    ID = "ANSWER_X_MEDIA_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "index"
    """``str``: Name of the property that holds this error's value"""

    @property
    def index(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class ApiIdInvalid(BadRequest):
    """The api_id/api_hash combination is invalid."""
    ID = "API_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ApiIdPublishedFlood(BadRequest):
    """You are using an API key that is limited on the server side because it was published somewhere."""
    ID = "API_ID_PUBLISHED_FLOOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ArticleTitleEmpty(BadRequest):
    """The title of the article is empty."""
    ID = "ARTICLE_TITLE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AttachMediaEmpty(BadRequest):
    """The attached media is empty."""
    ID = "ATTACH_MEDIA_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AttachMediaTypeInvalid(BadRequest):
    """The attached_media is invalid."""
    ID = "ATTACH_MEDIA_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AudioContentUrlEmpty(BadRequest):
    """The remote URL specified in the content field is empty."""
    ID = "AUDIO_CONTENT_URL_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AudioTitleEmpty(BadRequest):
    """The title attribute of the audio is empty."""
    ID = "AUDIO_TITLE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthBytesInvalid(BadRequest):
    """The provided authorization bytes are invalid."""
    ID = "AUTH_BYTES_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthTokenAlreadyAccepted(BadRequest):
    """The specified auth token was already used."""
    ID = "AUTH_TOKEN_ALREADY_ACCEPTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthTokenException(BadRequest):
    """An error occurred while importing the auth token."""
    ID = "AUTH_TOKEN_EXCEPTION"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthTokenExpired(BadRequest):
    """The provided authorization token has expired and the updated QR-code must be re-scanned."""
    ID = "AUTH_TOKEN_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthTokenInvalid(BadRequest):
    """An invalid authorization token was provided."""
    ID = "AUTH_TOKEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthTokenInvalid2(BadRequest):
    """An invalid authorization token was provided."""
    ID = "AUTH_TOKEN_INVALID2"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthTokenInvalidx(BadRequest):
    """The specified auth token is invalid."""
    ID = "AUTH_TOKEN_INVALIDX"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AutoarchiveNotAvailable(BadRequest):
    """This feature is not yet enabled for your account due to it not receiving too many private messages from strangers."""
    ID = "AUTOARCHIVE_NOT_AVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BalanceTooLow(BadRequest):
    """The transaction cannot be completed because the current [Telegram Stars balance](https://core.telegram.org/api/stars) is too low."""
    ID = "BALANCE_TOO_LOW"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BankCardNumberInvalid(BadRequest):
    """The specified credit card number is invalid."""
    ID = "BANK_CARD_NUMBER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BannedRightsInvalid(BadRequest):
    """You provided a set of restrictions that is invalid."""
    ID = "BANNED_RIGHTS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BasePortLocInvalid(BadRequest):
    """The base port location is invalid."""
    ID = "BASE_PORT_LOC_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BirthdayAlready(BadRequest):
    """This user has already entered a birthday."""
    ID = "BIRTHDAY_ALREADY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BirthdayInvalid(BadRequest):
    """An invalid age was specified, must be between 0 and 150 years."""
    ID = "BIRTHDAY_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BoostsEmpty(BadRequest):
    """No boost slots were specified."""
    ID = "BOOSTS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BoostsRequired(BadRequest):
    """The specified channel must first be [boosted by its users](https://core.telegram.org/api/boost) in order to perform this action."""
    ID = "BOOSTS_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BoostNotModified(BadRequest):
    """You're already [boosting](https://core.telegram.org/api/boost) the specified channel."""
    ID = "BOOST_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BoostPeerInvalid(BadRequest):
    """The specified `boost_peer` is invalid."""
    ID = "BOOST_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotsTooMuch(BadRequest):
    """There are too many bots in this chat/channel."""
    ID = "BOTS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotAlreadyDisabled(BadRequest):
    """The connected business bot was already disabled for the specified peer."""
    ID = "BOT_ALREADY_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotAppBotInvalid(BadRequest):
    """The bot_id passed in the inputBotAppShortName constructor is invalid."""
    ID = "BOT_APP_BOT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotAppInvalid(BadRequest):
    """The specified bot app is invalid."""
    ID = "BOT_APP_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotAppShortnameInvalid(BadRequest):
    """The specified bot app short name is invalid."""
    ID = "BOT_APP_SHORTNAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotBusinessMissing(BadRequest):
    """The specified bot is not a business bot (the [user](https://core.telegram.org/constructor/user).`bot_business` flag is not set)."""
    ID = "BOT_BUSINESS_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotChannelsNa(BadRequest):
    """Bots can't edit admin privileges."""
    ID = "BOT_CHANNELS_NA"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotCommandDescriptionInvalid(BadRequest):
    """The specified command description was empty, too long or had invalid characters."""
    ID = "BOT_COMMAND_DESCRIPTION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotCommandInvalid(BadRequest):
    """The specified command is invalid."""
    ID = "BOT_COMMAND_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotCreateLimitExceeded(BadRequest):
    """The current user already owns the maximum allowed number of owned bots, as specified by [`bots_create_limit_default` &raquo;](https://core.telegram.org/api/config#bots-create-limit-default) and [`bots_create_limit_premium` &raquo;](https://core.telegram.org/api/config#bots-create-limit-premium); if the current user doesn't have Telegram Premium, upgrading to Premium will allow them to create more bots."""
    ID = "BOT_CREATE_LIMIT_EXCEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotDomainInvalid(BadRequest):
    """The domain used for the auth button does not match the one configured in @BotFather."""
    ID = "BOT_DOMAIN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotFallbackUnsupported(BadRequest):
    """The fallback flag can't be set for bots."""
    ID = "BOT_FALLBACK_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotGamesDisabled(BadRequest):
    """Bot games cannot be used in this type of chat."""
    ID = "BOT_GAMES_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotGroupsBlocked(BadRequest):
    """This bot can't be added to groups."""
    ID = "BOT_GROUPS_BLOCKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotIdInvalid(BadRequest):
    """The specified bot ID is invalid."""
    ID = "BOT_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotInlineDisabled(BadRequest):
    """The inline feature of this bot is disabled."""
    ID = "BOT_INLINE_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotInvalid(BadRequest):
    """This is not a valid bot."""
    ID = "BOT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotInvoiceInvalid(BadRequest):
    """The specified invoice is invalid."""
    ID = "BOT_INVOICE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotMethodInvalid(BadRequest):
    """The specified method cannot be used by bots."""
    ID = "BOT_METHOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotMissing(BadRequest):
    """This method can only be run by a bot."""
    ID = "BOT_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotNotConnectedYet(BadRequest):
    """No [business bot](https://core.telegram.org/api/business#connected-bots) is connected to the currently logged in user."""
    ID = "BOT_NOT_CONNECTED_YET"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotOnesideNotAvail(BadRequest):
    """Bots can't pin messages in private chats just for themselves."""
    ID = "BOT_ONESIDE_NOT_AVAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotPaymentsDisabled(BadRequest):
    """Please enable bot payments in botfather before calling this method."""
    ID = "BOT_PAYMENTS_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotPollsDisabled(BadRequest):
    """Sending polls by bots has been disabled."""
    ID = "BOT_POLLS_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotResponseTimeout(BadRequest):
    """The bot did not answer to the callback query in time."""
    ID = "BOT_RESPONSE_TIMEOUT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotScoreNotModified(BadRequest):
    """The bot score wasn't modified."""
    ID = "BOT_SCORE_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BotWebviewDisabled(BadRequest):
    """A webview cannot be opened in the specified conditions: emitted for example if `from_bot_menu` or `url` are set and `peer` is not the chat with the bot."""
    ID = "BOT_WEBVIEW_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BroadcastCallsDisabled(BadRequest):
    """Broadcast calls disabled."""
    ID = "BROADCAST_CALLS_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BroadcastIdInvalid(BadRequest):
    """The channel is invalid."""
    ID = "BROADCAST_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BroadcastPublicVotersForbidden(BadRequest):
    """Polls with public voters cannot be sent in channels."""
    ID = "BROADCAST_PUBLIC_VOTERS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BroadcastRequired(BadRequest):
    """This method can only be used with a channel."""
    ID = "BROADCAST_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessBotMissing(BadRequest):
    """The business bot is missing."""
    ID = "BUSINESS_BOT_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessConnectionInvalid(BadRequest):
    """The business connection is invalid."""
    ID = "BUSINESS_CONNECTION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessConnectionNotAllowed(BadRequest):
    """This business connection is not allowed."""
    ID = "BUSINESS_CONNECTION_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessPeerInvalid(BadRequest):
    """Messages can't be set to the specified peer through the current [business connection](https://core.telegram.org/api/business#connected-bots)."""
    ID = "BUSINESS_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessPeerUsageMissing(BadRequest):
    """You cannot send a message to a user through a [business connection](https://core.telegram.org/api/business#connected-bots) if the user hasn't recently contacted us."""
    ID = "BUSINESS_PEER_USAGE_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessRecipientsEmpty(BadRequest):
    """You didn't set any flag in inputBusinessBotRecipients, thus the bot cannot work with *any* peer."""
    ID = "BUSINESS_RECIPIENTS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessRecipientsInvalid(BadRequest):
    """The specified inputBusinessBotRecipients is invalid."""
    ID = "BUSINESS_RECIPIENTS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessWorkHoursEmpty(BadRequest):
    """No work hours were specified."""
    ID = "BUSINESS_WORK_HOURS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class BusinessWorkHoursPeriodInvalid(BadRequest):
    """The specified work hours are invalid, see [here »](https://core.telegram.org/api/business#opening-hours) for the exact requirements."""
    ID = "BUSINESS_WORK_HOURS_PERIOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonCopyTextInvalid(BadRequest):
    """The specified [keyboardButtonCopy](https://core.telegram.org/constructor/keyboardButtonCopy).`copy_text` is invalid."""
    ID = "BUTTON_COPY_TEXT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonDataInvalid(BadRequest):
    """The button callback data is invalid or too large."""
    ID = "BUTTON_DATA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonIdInvalid(BadRequest):
    """The specified button_id is invalid."""
    ID = "BUTTON_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonInvalid(BadRequest):
    """The specified button is invalid."""
    ID = "BUTTON_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonPosInvalid(BadRequest):
    """The position of one of the keyboard buttons is invalid (i.e. a Game or Pay button not in the first position, and so on...)."""
    ID = "BUTTON_POS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonTextInvalid(BadRequest):
    """The specified button text is invalid."""
    ID = "BUTTON_TEXT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonTypeInvalid(BadRequest):
    """The type of one of the buttons you provided is invalid."""
    ID = "BUTTON_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonUrlInvalid(BadRequest):
    """The button url is invalid."""
    ID = "BUTTON_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonUserInvalid(BadRequest):
    """The user_id passed to inputKeyboardButtonUserProfile is invalid!."""
    ID = "BUTTON_USER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ButtonUserPrivacyRestricted(BadRequest):
    """The privacy setting of the user specified in a [inputKeyboardButtonUserProfile](https://core.telegram.org/constructor/inputKeyboardButtonUserProfile) button do not allow creating such a button."""
    ID = "BUTTON_USER_PRIVACY_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallAlreadyAccepted(BadRequest):
    """The call was already accepted."""
    ID = "CALL_ALREADY_ACCEPTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallAlreadyDeclined(BadRequest):
    """The call was already declined."""
    ID = "CALL_ALREADY_DECLINED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallNotActive(BadRequest):
    """The specified call is not active."""
    ID = "CALL_NOT_ACTIVE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallOccupyFailed(BadRequest):
    """The call failed because the user is already making another call."""
    ID = "CALL_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallPeerInvalid(BadRequest):
    """The provided call peer object is invalid."""
    ID = "CALL_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallProtocolFlagsInvalid(BadRequest):
    """Call protocol flags invalid."""
    ID = "CALL_PROTOCOL_FLAGS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallProtocolLayerInvalid(BadRequest):
    """The specified protocol layer version range is invalid."""
    ID = "CALL_PROTOCOL_LAYER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CdnMethodInvalid(BadRequest):
    """You can't call this method in a CDN DC."""
    ID = "CDN_METHOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelsAdminLocatedTooMuch(BadRequest):
    """The user has reached the limit of public geogroups."""
    ID = "CHANNELS_ADMIN_LOCATED_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelsAdminPublicTooMuch(BadRequest):
    """You're administrator of too many public channels."""
    ID = "CHANNELS_ADMIN_PUBLIC_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelsTooMuch(BadRequest):
    """You have joined too many channels/supergroups."""
    ID = "CHANNELS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelAddInvalid(BadRequest):
    """Internal error."""
    ID = "CHANNEL_ADD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelBanned(BadRequest):
    """The channel is banned."""
    ID = "CHANNEL_BANNED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelForumMissing(BadRequest):
    """This supergroup is not a forum."""
    ID = "CHANNEL_FORUM_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelIdInvalid(BadRequest):
    """The specified supergroup ID is invalid."""
    ID = "CHANNEL_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelInvalid(BadRequest):
    """The provided channel is invalid."""
    ID = "CHANNEL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelMonoforumUnsupported(BadRequest):
    """You cannot use this method in direct chats."""
    ID = "CHANNEL_MONOFORUM_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelParicipantMissing(BadRequest):
    """The current user is not in the channel."""
    ID = "CHANNEL_PARICIPANT_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelPrivate(BadRequest):
    """You haven't joined this channel/supergroup."""
    ID = "CHANNEL_PRIVATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelTooBig(BadRequest):
    """This channel is too big."""
    ID = "CHANNEL_TOO_BIG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChannelTooLarge(BadRequest):
    """This channel is too large."""
    ID = "CHANNEL_TOO_LARGE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChargeAlreadyRefunded(BadRequest):
    """This transaction was already refunded."""
    ID = "CHARGE_ALREADY_REFUNDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChargeIdEmpty(BadRequest):
    """The specified charge_id is empty."""
    ID = "CHARGE_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChargeIdInvalid(BadRequest):
    """The specified charge_id is invalid."""
    ID = "CHARGE_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChargeNotFound(BadRequest):
    """The charge id was not found."""
    ID = "CHARGE_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatlinksTooMuch(BadRequest):
    """Too many [business chat links](https://core.telegram.org/api/business#business-chat-links) were created, please delete some older links."""
    ID = "CHATLINKS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatlinkSlugEmpty(BadRequest):
    """The specified slug is empty."""
    ID = "CHATLINK_SLUG_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatlinkSlugExpired(BadRequest):
    """The specified [business chat link](https://core.telegram.org/api/business#business-chat-links) has expired."""
    ID = "CHATLINK_SLUG_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatlistsTooMuch(BadRequest):
    """You have created too many folder links, hitting the `chatlist_invites_limit_default`/`chatlist_invites_limit_premium` [limits »](https://core.telegram.org/api/config#chatlist-invites-limit-default)."""
    ID = "CHATLISTS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatlistExcludeInvalid(BadRequest):
    """The specified `exclude_peers` are invalid."""
    ID = "CHATLIST_EXCLUDE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatAboutNotModified(BadRequest):
    """The chat about text was not modified because you tried to edit it using the same content."""
    ID = "CHAT_ABOUT_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatAboutTooLong(BadRequest):
    """The chat about text is too long."""
    ID = "CHAT_ABOUT_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatAdminRequired(BadRequest):
    """You must be an admin in this chat to do this."""
    ID = "CHAT_ADMIN_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatDiscussionUnallowed(BadRequest):
    """You can't enable forum topics in a discussion group linked to a channel."""
    ID = "CHAT_DISCUSSION_UNALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatForwardsRestricted(BadRequest):
    """You can't forward messages from a protected chat."""
    ID = "CHAT_FORWARDS_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatIdEmpty(BadRequest):
    """The provided chat id is empty."""
    ID = "CHAT_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatIdInvalid(BadRequest):
    """The chat id being used is invalid or not known yet. Make sure you see the chat before interacting with it."""
    ID = "CHAT_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatInvalid(BadRequest):
    """The chat is invalid."""
    ID = "CHAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatInvitePermanent(BadRequest):
    """You can't set an expiration date on permanent invite links."""
    ID = "CHAT_INVITE_PERMANENT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatLinkExists(BadRequest):
    """The action failed because the supergroup is linked to a channel."""
    ID = "CHAT_LINK_EXISTS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatMemberAddFailed(BadRequest):
    """Could not add participants."""
    ID = "CHAT_MEMBER_ADD_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatNotModified(BadRequest):
    """The chat settings (title, permissions, photo, etc..) were not modified because you tried to edit them using the same content."""
    ID = "CHAT_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatPublicRequired(BadRequest):
    """You can only enable join requests in public groups."""
    ID = "CHAT_PUBLIC_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatRestricted(BadRequest):
    """You can't send messages in this chat, you were restricted."""
    ID = "CHAT_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatRevokeDateUnsupported(BadRequest):
    """`min_date` and `max_date` are not available for using with non-user peers."""
    ID = "CHAT_REVOKE_DATE_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatSendInlineForbidden(BadRequest):
    """You cannot use inline bots to send messages in this chat."""
    ID = "CHAT_SEND_INLINE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatTitleEmpty(BadRequest):
    """The chat title is empty."""
    ID = "CHAT_TITLE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatTooBig(BadRequest):
    """This method is not available for groups with more than `chat_read_mark_size_threshold` members, [see client configuration »](https://core.telegram.org/api/config#client-configuration)."""
    ID = "CHAT_TOO_BIG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatWriteForbidden(BadRequest):
    """You can't write in this chat."""
    ID = "CHAT_WRITE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CodeEmpty(BadRequest):
    """The provided code is empty."""
    ID = "CODE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CodeHashInvalid(BadRequest):
    """The provided code hash invalid."""
    ID = "CODE_HASH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CodeInvalid(BadRequest):
    """The provided code is invalid (i.e. from email)."""
    ID = "CODE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CollectibleInvalid(BadRequest):
    """The specified collectible is invalid."""
    ID = "COLLECTIBLE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CollectibleNotFound(BadRequest):
    """The specified collectible could not be found."""
    ID = "COLLECTIBLE_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CollectionIdInvalid(BadRequest):
    """The specified collection ID is invalid."""
    ID = "COLLECTION_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ColorInvalid(BadRequest):
    """The specified color id is invalid."""
    ID = "COLOR_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionApiIdInvalid(BadRequest):
    """The provided API id is invalid."""
    ID = "CONNECTION_API_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionAppVersionEmpty(BadRequest):
    """App version is empty."""
    ID = "CONNECTION_APP_VERSION_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionDeviceModelEmpty(BadRequest):
    """The specified device model is empty."""
    ID = "CONNECTION_DEVICE_MODEL_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionIdInvalid(BadRequest):
    """The specified connection ID is invalid."""
    ID = "CONNECTION_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionLangPackInvalid(BadRequest):
    """The specified language pack is invalid."""
    ID = "CONNECTION_LANG_PACK_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionLayerInvalid(BadRequest):
    """The connection layer is invalid. Missing InvokeWithLayer-InitConnection call."""
    ID = "CONNECTION_LAYER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionNotInited(BadRequest):
    """Please initialize the connection using initConnection before making queries."""
    ID = "CONNECTION_NOT_INITED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionSystemEmpty(BadRequest):
    """The specified system version is empty."""
    ID = "CONNECTION_SYSTEM_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ConnectionSystemLangCodeEmpty(BadRequest):
    """The specified system language code is empty."""
    ID = "CONNECTION_SYSTEM_LANG_CODE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ContactAddMissing(BadRequest):
    """Contact to add is missing."""
    ID = "CONTACT_ADD_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ContactIdInvalid(BadRequest):
    """The provided contact ID is invalid."""
    ID = "CONTACT_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ContactMissing(BadRequest):
    """The specified user is not a contact."""
    ID = "CONTACT_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ContactNameEmpty(BadRequest):
    """The provided contact name is empty."""
    ID = "CONTACT_NAME_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ContactReqMissing(BadRequest):
    """Missing contact request."""
    ID = "CONTACT_REQ_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CreateCallFailed(BadRequest):
    """An error occurred while creating the call."""
    ID = "CREATE_CALL_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CredentialInvalid(BadRequest):
    """The credential is invalid."""
    ID = "CREDENTIAL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CurrencyTotalAmountInvalid(BadRequest):
    """The total amount of all prices is invalid."""
    ID = "CURRENCY_TOTAL_AMOUNT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CustomReactionsTooMany(BadRequest):
    """Too many custom reactions were specified."""
    ID = "CUSTOM_REACTIONS_TOO_MANY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DataHashSizeInvalid(BadRequest):
    """The size of the specified secureValueErrorData.data_hash is invalid."""
    ID = "DATA_HASH_SIZE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DataInvalid(BadRequest):
    """The encrypted data is invalid."""
    ID = "DATA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DataJsonInvalid(BadRequest):
    """The provided JSON data is invalid."""
    ID = "DATA_JSON_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DataTooLong(BadRequest):
    """The data is too long."""
    ID = "DATA_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DateEmpty(BadRequest):
    """The date argument is empty."""
    ID = "DATE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DcIdInvalid(BadRequest):
    """The provided dc_id is invalid."""
    ID = "DC_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DeleteAnswerForbidden(BadRequest):
    """You cannot delete the specified option in this poll."""
    ID = "DELETE_ANSWER_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DhGAInvalid(BadRequest):
    """The g_a parameter is invalid."""
    ID = "DH_G_A_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class DocumentInvalid(BadRequest):
    """The specified document is invalid."""
    ID = "DOCUMENT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EffectChatInvalid(BadRequest):
    """Message [effects](https://core.telegram.org/api/effects) can only be used in private 1-on-1 chats, but the caller tried to send a message with an effect to a group or channel."""
    ID = "EFFECT_CHAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EffectIdInvalid(BadRequest):
    """The specified effect id is invalid."""
    ID = "EFFECT_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailCodeEmpty(BadRequest):
    """The email code is empty."""
    ID = "EMAIL_CODE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailHashExpired(BadRequest):
    """The email hash expired and cannot be used to verify it."""
    ID = "EMAIL_HASH_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailInstallMissing(BadRequest):
    """Attempting to send a code to the recovery email, but no email is configured."""
    ID = "EMAIL_INSTALL_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailInvalid(BadRequest):
    """The specified email is invalid."""
    ID = "EMAIL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailNotAllowed(BadRequest):
    """The specified email cannot be used to complete the operation."""
    ID = "EMAIL_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailNotSetup(BadRequest):
    """In order to change the login email with emailVerifyPurposeLoginChange, an existing login email must already be set using emailVerifyPurposeLoginSetup."""
    ID = "EMAIL_NOT_SETUP"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailUnconfirmed(BadRequest):
    """Email unconfirmed."""
    ID = "EMAIL_UNCONFIRMED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmailUnconfirmedX(EmailUnconfirmed):
    """The provided email isn't confirmed, {code_length} is the length of the verification code that was just sent to the email: use [account.verifyEmail](https://core.telegram.org/method/account.verifyEmail) to enter the received verification code and enable the recovery email."""
    ID = "EMAIL_UNCONFIRMED_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "code_length"
    """``str``: Name of the property that holds this error's value"""

    @property
    def code_length(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class EmailVerifyExpired(BadRequest):
    """The verification email has expired."""
    ID = "EMAIL_VERIFY_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmojiInvalid(BadRequest):
    """The specified theme emoji is valid."""
    ID = "EMOJI_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmojiMarkupInvalid(BadRequest):
    """The specified `video_emoji_markup` was invalid."""
    ID = "EMOJI_MARKUP_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmojiNotModified(BadRequest):
    """The theme wasn't changed."""
    ID = "EMOJI_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmoticonEmpty(BadRequest):
    """The provided emoji parameter is empty."""
    ID = "EMOTICON_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmoticonInvalid(BadRequest):
    """The specified emoji is invalid."""
    ID = "EMOTICON_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EmoticonStickerpackMissing(BadRequest):
    """The emoticon sticker pack you are trying to obtain is missing."""
    ID = "EMOTICON_STICKERPACK_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptedMessageInvalid(BadRequest):
    """The special binding message (bind_auth_key_inner) contains invalid data."""
    ID = "ENCRYPTED_MESSAGE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionAlreadyAccepted(BadRequest):
    """The secret chat was already accepted."""
    ID = "ENCRYPTION_ALREADY_ACCEPTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionAlreadyDeclined(BadRequest):
    """The secret chat was already declined."""
    ID = "ENCRYPTION_ALREADY_DECLINED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionDeclined(BadRequest):
    """The secret chat was declined."""
    ID = "ENCRYPTION_DECLINED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionIdInvalid(BadRequest):
    """The provided secret chat id is invalid."""
    ID = "ENCRYPTION_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EntitiesTooLong(BadRequest):
    """The entity provided contains data that is too long, or you passed too many entities to this message."""
    ID = "ENTITIES_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EntityBoundsInvalid(BadRequest):
    """A specified [entity offset or length](https://core.telegram.org/api/entities#entity-length) is invalid, see [here »](https://core.telegram.org/api/entities#entity-length) for info on how to properly compute the entity offset/length."""
    ID = "ENTITY_BOUNDS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EntityDateFormatInvalid(BadRequest):
    """One of the passed messageEntityFormattedDate objects has an invalid format (i.e. an invalid combination of the format flags)."""
    ID = "ENTITY_DATE_FORMAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EntityDateInvalid(BadRequest):
    """A specified date/time entity is invalid."""
    ID = "ENTITY_DATE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EntityDateTooLong(BadRequest):
    """The maximum text span that can be covered by a date entity is 31 UTF-16 code units if any of the date formatting flags is set, or 127 UTF-16 code units without.  ."""
    ID = "ENTITY_DATE_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EntityMentionUserInvalid(BadRequest):
    """The mentioned entity is not an user."""
    ID = "ENTITY_MENTION_USER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ErrorTextEmpty(BadRequest):
    """The provided error message is empty."""
    ID = "ERROR_TEXT_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExpiresAtInvalid(BadRequest):
    """The specified `expires_at` timestamp is invalid."""
    ID = "EXPIRES_AT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExpireDateInvalid(BadRequest):
    """The specified expiration date is invalid."""
    ID = "EXPIRE_DATE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExpireForbidden(BadRequest):
    """Expire forbidden."""
    ID = "EXPIRE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExportCardInvalid(BadRequest):
    """The provided card is invalid."""
    ID = "EXPORT_CARD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExtendedMediaAmountInvalid(BadRequest):
    """The specified `stars_amount` of the passed [inputMediaPaidMedia](https://core.telegram.org/constructor/inputMediaPaidMedia) is invalid."""
    ID = "EXTENDED_MEDIA_AMOUNT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExtendedMediaEmpty(BadRequest):
    """The specified extended media is empty."""
    ID = "EXTENDED_MEDIA_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExtendedMediaInvalid(BadRequest):
    """The specified paid media is invalid."""
    ID = "EXTENDED_MEDIA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExtendedMediaPeerInvalid(BadRequest):
    """The specified chat type is invalid."""
    ID = "EXTENDED_MEDIA_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExtendedMediaTypeInvalid(BadRequest):
    """The specified extended media type is unsupported."""
    ID = "EXTENDED_MEDIA_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ExternalUrlInvalid(BadRequest):
    """The external media URL is invalid."""
    ID = "EXTERNAL_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FeatureDisabled(BadRequest):
    """This feature is disabled."""
    ID = "FEATURE_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FieldNameEmpty(BadRequest):
    """The field with the name FIELD_NAME is missing."""
    ID = "FIELD_NAME_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FieldNameInvalid(BadRequest):
    """The field with the name FIELD_NAME is invalid."""
    ID = "FIELD_NAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileContentTypeInvalid(BadRequest):
    """File content-type is invalid."""
    ID = "FILE_CONTENT_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileEmtpy(BadRequest):
    """An empty file was provided."""
    ID = "FILE_EMTPY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileIdInvalid(BadRequest):
    """The provided file id is invalid."""
    ID = "FILE_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileMigrate400(FileMigrate, BadRequest):
    """The file currently being accessed is stored in DC{dc_id}, please re-send the query to that DC."""
    ID = "FILE_MIGRATE_X"
    """``str``: RPC Error ID"""
    CODE = 400
    """``int``: RPC Error Code"""
    NAME = "Bad Request"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__

    VALUE_NAME = "dc_id"
    """``str``: Name of the property that holds this error's value"""

    @property
    def dc_id(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FilePartsInvalid(BadRequest):
    """The number of file parts is invalid."""
    ID = "FILE_PARTS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePart0Missing(BadRequest):
    """File part 0 missing."""
    ID = "FILE_PART_0_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartEmpty(BadRequest):
    """The provided file part is empty."""
    ID = "FILE_PART_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartInvalid(BadRequest):
    """The file part number is invalid."""
    ID = "FILE_PART_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartLengthInvalid(BadRequest):
    """The length of a file part is invalid."""
    ID = "FILE_PART_LENGTH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartSizeChanged(BadRequest):
    """The part size is different from the size of one of the previous parts in the same file."""
    ID = "FILE_PART_SIZE_CHANGED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartSizeInvalid(BadRequest):
    """The provided file part size is invalid."""
    ID = "FILE_PART_SIZE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartTooBig(BadRequest):
    """The uploaded file part is too big."""
    ID = "FILE_PART_TOO_BIG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartTooSmall(BadRequest):
    """The size limit for the content of the file part has been exceeded."""
    ID = "FILE_PART_TOO_SMALL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilePartMissing(BadRequest):
    """Part {file_part} of the file is missing from storage. Try repeating the method call to resave the part."""
    ID = "FILE_PART_X_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "file_part"
    """``str``: Name of the property that holds this error's value"""

    @property
    def file_part(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FileReferenceEmpty(BadRequest):
    """The file id contains an empty [file reference](https://core.telegram.org/api/file_reference), you must obtain a valid one by fetching the message from the origin context."""
    ID = "FILE_REFERENCE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileReferenceExpired(BadRequest):
    """The file id contains an expired [file reference](https://core.telegram.org/api/file_reference), you must obtain a valid one by fetching the message from the origin context."""
    ID = "FILE_REFERENCE_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileReferenceInvalid(BadRequest):
    """The file id contains an invalid [file reference](https://core.telegram.org/api/file_reference), you must obtain a valid one by fetching the message from the origin context."""
    ID = "FILE_REFERENCE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileReferenceEmptyX(FileReferenceEmpty):
    """The file reference of the media file at offset {index} in the multi_media array is invalid."""
    ID = "FILE_REFERENCE_X_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "index"
    """``str``: Name of the property that holds this error's value"""

    @property
    def index(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FileReferenceExpiredX(FileReferenceExpired):
    """The [file reference](https://core.telegram.org/api/file_reference) of the media file at index {index} in the passed media array expired, it must be refreshed."""
    ID = "FILE_REFERENCE_X_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "index"
    """``str``: Name of the property that holds this error's value"""

    @property
    def index(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FileReferenceInvalidX(FileReferenceInvalid):
    """The [file reference](https://core.telegram.org/api/file_reference) of the media file at index {index} in the passed media array is invalid."""
    ID = "FILE_REFERENCE_X_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "index"
    """``str``: Name of the property that holds this error's value"""

    @property
    def index(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FileTitleEmpty(BadRequest):
    """An empty file title was specified."""
    ID = "FILE_TITLE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileTokenInvalid(BadRequest):
    """The master DC did not accept the `file_token` (e.g., the token has expired). Continue downloading the file from the master DC using upload.getFile."""
    ID = "FILE_TOKEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilterIdInvalid(BadRequest):
    """The specified filter ID is invalid."""
    ID = "FILTER_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilterIncludeEmpty(BadRequest):
    """The list of include_peers of the folder is empty."""
    ID = "FILTER_INCLUDE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilterIncludeTooMuch(BadRequest):
    """You can't add more chats to this folder."""
    ID = "FILTER_INCLUDE_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilterNotSupported(BadRequest):
    """The specified filter cannot be used in this context."""
    ID = "FILTER_NOT_SUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FilterTitleEmpty(BadRequest):
    """The title field of the filter is empty."""
    ID = "FILTER_TITLE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FirstnameInvalid(BadRequest):
    """The first name is invalid."""
    ID = "FIRSTNAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FloodskipNotAllowed(BadRequest):
    """You can't execute the specified action because in order to enable this feature [the following conditions](https://core.telegram.org/bots/faq#how-can-i-message-all-of-my-bot-39s-subscribers-at-once) must be satisfied."""
    ID = "FLOODSKIP_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FolderIdEmpty(BadRequest):
    """An empty folder ID was specified."""
    ID = "FOLDER_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FolderIdInvalid(BadRequest):
    """The specified folder id is invalid."""
    ID = "FOLDER_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FormExpired(BadRequest):
    """The form was generated more than 10 minutes ago and has expired, please re-generate it using [payments.getPaymentForm](https://core.telegram.org/method/payments.getPaymentForm) and pass the new `form_id`."""
    ID = "FORM_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FormIdEmpty(BadRequest):
    """The specified form id is empty."""
    ID = "FORM_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FormIdExpired(BadRequest):
    """The specified form id has expired."""
    ID = "FORM_ID_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FormSubmitDuplicate(BadRequest):
    """The specified form is duplicated."""
    ID = "FORM_SUBMIT_DUPLICATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FormUnsupported(BadRequest):
    """The specified form is unsupported. Please update your client."""
    ID = "FORM_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ForumEnabled(BadRequest):
    """You can't execute the specified action because the group is a [forum](https://core.telegram.org/api/forum), disable forum functionality to continue."""
    ID = "FORUM_ENABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FreshChangeAdminsForbidden(BadRequest):
    """You can't change administrator settings in this chat because your session was logged-in recently."""
    ID = "FRESH_CHANGE_ADMINS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FromMessageBotDisabled(BadRequest):
    """Bots can't use fromMessage min constructors."""
    ID = "FROM_MESSAGE_BOT_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FromPeerInvalid(BadRequest):
    """The specified from_id is invalid."""
    ID = "FROM_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FrozenParticipantMissing(BadRequest):
    """The account is frozen and cannot access the chat participant."""
    ID = "FROZEN_PARTICIPANT_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FutureCreatorNone(BadRequest):
    """The future creator after leave is only applicable to supergroups."""
    ID = "FUTURE_CREATOR_NONE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GameBotInvalid(BadRequest):
    """You cannot send that game with the current bot."""
    ID = "GAME_BOT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GeneralModifyIconForbidden(BadRequest):
    """You can't modify the icon of the "General" topic."""
    ID = "GENERAL_MODIFY_ICON_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GeoPointInvalid(BadRequest):
    """Invalid geo point provided."""
    ID = "GEO_POINT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GiftMonthsInvalid(BadRequest):
    """The value passed in invoice.inputInvoicePremiumGiftStars.months is invalid."""
    ID = "GIFT_MONTHS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GiftSlugExpired(BadRequest):
    """The specified gift slug has expired."""
    ID = "GIFT_SLUG_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GiftSlugInvalid(BadRequest):
    """The specified slug is invalid."""
    ID = "GIFT_SLUG_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GiftStarsInvalid(BadRequest):
    """The specified amount of stars is invalid."""
    ID = "GIFT_STARS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GifContentTypeInvalid(BadRequest):
    """GIF content-type invalid."""
    ID = "GIF_CONTENT_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GifIdInvalid(BadRequest):
    """The provided animation id is invalid."""
    ID = "GIF_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GraphExpiredReload(BadRequest):
    """This graph has expired, please obtain a new graph token."""
    ID = "GRAPH_EXPIRED_RELOAD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GraphInvalidReload(BadRequest):
    """Invalid graph token provided, please reload the stats and provide the updated token."""
    ID = "GRAPH_INVALID_RELOAD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GraphOutdatedReload(BadRequest):
    """The graph is outdated, please get a new async token using stats.getBroadcastStats."""
    ID = "GRAPH_OUTDATED_RELOAD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallAlreadyDiscarded(BadRequest):
    """The group call was already discarded."""
    ID = "GROUPCALL_ALREADY_DISCARDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallForbidden(BadRequest):
    """The group call has already ended."""
    ID = "GROUPCALL_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallInvalid(BadRequest):
    """The specified group call is invalid."""
    ID = "GROUPCALL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallJoinMissing(BadRequest):
    """You haven't joined this group call."""
    ID = "GROUPCALL_JOIN_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallNotModified(BadRequest):
    """Group call settings weren't modified."""
    ID = "GROUPCALL_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallSsrcDuplicateMuch(BadRequest):
    """The app needs to retry joining the group call with a new SSRC value."""
    ID = "GROUPCALL_SSRC_DUPLICATE_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupedMediaInvalid(BadRequest):
    """The album contains invalid media."""
    ID = "GROUPED_MEDIA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupCallInvalid(BadRequest):
    """The group call is invalid."""
    ID = "GROUP_CALL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class HashtagInvalid(BadRequest):
    """The specified hashtag is invalid."""
    ID = "HASHTAG_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class HashInvalid(BadRequest):
    """The provided hash is invalid."""
    ID = "HASH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class HashSizeInvalid(BadRequest):
    """The size of the specified secureValueError.hash is invalid."""
    ID = "HASH_SIZE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class HideRequesterMissing(BadRequest):
    """The join request was missing or was already handled."""
    ID = "HIDE_REQUESTER_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class IdExpired(BadRequest):
    """The passed prepared inline message ID has expired."""
    ID = "ID_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class IdInvalid(BadRequest):
    """The passed ID is invalid."""
    ID = "ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImageProcessFailed(BadRequest):
    """The server failed to process your image."""
    ID = "IMAGE_PROCESS_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImportFileInvalid(BadRequest):
    """The specified chat export file is invalid."""
    ID = "IMPORT_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImportFormatDateInvalid(BadRequest):
    """The date specified in the import file is invalid."""
    ID = "IMPORT_FORMAT_DATE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImportFormatUnrecognized(BadRequest):
    """The specified chat export file was exported from an unsupported chat app."""
    ID = "IMPORT_FORMAT_UNRECOGNIZED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImportHistoryLogEmpty(BadRequest):
    """The specified chat export file is empty or has an invalid indentation."""
    ID = "IMPORT_HISTORY_LOG_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImportIdInvalid(BadRequest):
    """The specified import id is invalid."""
    ID = "IMPORT_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImportTokenInvalid(BadRequest):
    """The specified token is invalid."""
    ID = "IMPORT_TOKEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InlineResultExpired(BadRequest):
    """The inline bot query expired."""
    ID = "INLINE_RESULT_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputChatlistInvalid(BadRequest):
    """The specified folder is invalid."""
    ID = "INPUT_CHATLIST_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputConstructorInvalid(BadRequest):
    """The specified TL constructor is invalid."""
    ID = "INPUT_CONSTRUCTOR_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputFetchError(BadRequest):
    """An error occurred while deserializing the provided TL constructor."""
    ID = "INPUT_FETCH_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputFetchErrorX(InputFetchError):
    """An error occurred while parsing the provided TL {value} constructor."""
    ID = "INPUT_FETCH_ERROR_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputFetchFail(BadRequest):
    """Failed deserializing TL payload."""
    ID = "INPUT_FETCH_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputFileInvalid(BadRequest):
    """The specified [InputFile](https://core.telegram.org/type/InputFile) is invalid."""
    ID = "INPUT_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputFilterInvalid(BadRequest):
    """The specified filter is invalid."""
    ID = "INPUT_FILTER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputLayerInvalid(BadRequest):
    """The specified layer is invalid."""
    ID = "INPUT_LAYER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputMethodInvalid(BadRequest):
    """The method invoked is invalid in the current schema."""
    ID = "INPUT_METHOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputPeersEmpty(BadRequest):
    """The specified peer array is empty."""
    ID = "INPUT_PEERS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputPurposeInvalid(BadRequest):
    """The specified payment purpose is invalid."""
    ID = "INPUT_PURPOSE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputRequestTooLong(BadRequest):
    """The request payload is too long."""
    ID = "INPUT_REQUEST_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputStarsAmountInvalid(BadRequest):
    """The specified offer amount in stars is invalid, see [here &raquo;](https://core.telegram.org/api/gifts#collectible-gift-purchase-offers) for the allowed range."""
    ID = "INPUT_STARS_AMOUNT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputStarsNanosInvalid(BadRequest):
    """The specified stars nano amount is invalid."""
    ID = "INPUT_STARS_NANOS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputTextEmpty(BadRequest):
    """The specified text is empty."""
    ID = "INPUT_TEXT_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputTextTooLong(BadRequest):
    """The specified text is too long."""
    ID = "INPUT_TEXT_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InputUserDeactivated(BadRequest):
    """The target user has been deleted/deactivated."""
    ID = "INPUT_USER_DEACTIVATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InvitesTooMuch(BadRequest):
    """The maximum number of per-folder invites specified by the `chatlist_invites_limit_default`/`chatlist_invites_limit_premium` [client configuration parameters »](https://core.telegram.org/api/config#chatlist-invites-limit-default) was reached."""
    ID = "INVITES_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteForbiddenWithJoinas(BadRequest):
    """If the user has anonymously joined a group call as a channel, they can't invite other users to the group call because that would cause deanonymization, because the invite would be sent using the original user ID, not the anonymized channel ID."""
    ID = "INVITE_FORBIDDEN_WITH_JOINAS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteHashEmpty(BadRequest):
    """The invite hash is empty."""
    ID = "INVITE_HASH_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteHashExpired(BadRequest):
    """The invite link is no longer valid."""
    ID = "INVITE_HASH_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteHashInvalid(BadRequest):
    """The invite hash is invalid."""
    ID = "INVITE_HASH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteRequestSent(BadRequest):
    """You have successfully requested to join this chat or channel."""
    ID = "INVITE_REQUEST_SENT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteRevokedMissing(BadRequest):
    """The action required a chat invite link to be revoked first."""
    ID = "INVITE_REVOKED_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteSlugEmpty(BadRequest):
    """The specified invite slug is empty."""
    ID = "INVITE_SLUG_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteSlugExpired(BadRequest):
    """The specified invite slug has expired."""
    ID = "INVITE_SLUG_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InviteSlugInvalid(BadRequest):
    """The specified invite slug is invalid."""
    ID = "INVITE_SLUG_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InvoiceInvalid(BadRequest):
    """The specified invoice is invalid."""
    ID = "INVOICE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InvoicePayloadInvalid(BadRequest):
    """The specified invoice payload is invalid."""
    ID = "INVOICE_PAYLOAD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class JoinAsPeerInvalid(BadRequest):
    """The specified peer cannot be used to join a group call."""
    ID = "JOIN_AS_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LanguageInvalid(BadRequest):
    """The specified lang_code is invalid."""
    ID = "LANGUAGE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LangCodeInvalid(BadRequest):
    """The specified language code is invalid."""
    ID = "LANG_CODE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LangCodeNotSupported(BadRequest):
    """The specified language code is not supported."""
    ID = "LANG_CODE_NOT_SUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LangPackInvalid(BadRequest):
    """The provided language pack is invalid."""
    ID = "LANG_PACK_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LastnameInvalid(BadRequest):
    """The last name is invalid."""
    ID = "LASTNAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LimitInvalid(BadRequest):
    """The provided limit is invalid."""
    ID = "LIMIT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LimitPerPostInvalid(BadRequest):
    """The specified reactions_limit value is invalid."""
    ID = "LIMIT_PER_POST_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LinkNotModified(BadRequest):
    """The chat link was not modified because you tried to link to the same target."""
    ID = "LINK_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class LocationInvalid(BadRequest):
    """The provided location is invalid."""
    ID = "LOCATION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ManagerInvalid(BadRequest):
    """The provided bot manager is invalid. Bot Management Mode should be enabled for the bot in the @BotFather Mini App."""
    ID = "MANAGER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ManagerPermissionMissing(BadRequest):
    """The bot manager permission is missing. Bot Management Mode should be enabled for the bot in the @BotFather Mini App."""
    ID = "MANAGER_PERMISSION_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MaxDateInvalid(BadRequest):
    """The specified maximum date is invalid."""
    ID = "MAX_DATE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MaxIdInvalid(BadRequest):
    """The provided max_id is invalid."""
    ID = "MAX_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MaxQtsInvalid(BadRequest):
    """The specified qts is invalid."""
    ID = "MAX_QTS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class Md5ChecksumInvalid(BadRequest):
    """The file's checksum did not match the md5_checksum parameter."""
    ID = "MD5_CHECKSUM_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaAlreadyPaid(BadRequest):
    """The specified paid media is already paid."""
    ID = "MEDIA_ALREADY_PAID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaCaptionTooLong(BadRequest):
    """The media caption is too long."""
    ID = "MEDIA_CAPTION_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaEmpty(BadRequest):
    """The provided media you tried to send is invalid."""
    ID = "MEDIA_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaFileInvalid(BadRequest):
    """The specified media file is invalid."""
    ID = "MEDIA_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaGroupedInvalid(BadRequest):
    """You tried to send media of different types in an album."""
    ID = "MEDIA_GROUPED_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaInvalid(BadRequest):
    """Media invalid."""
    ID = "MEDIA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaNewInvalid(BadRequest):
    """The new media to edit the message with is invalid."""
    ID = "MEDIA_NEW_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaPrevInvalid(BadRequest):
    """The previous media cannot be edited with anything else."""
    ID = "MEDIA_PREV_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaTtlInvalid(BadRequest):
    """The specified media TTL is invalid."""
    ID = "MEDIA_TTL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaTypeInvalid(BadRequest):
    """The specified media type cannot be used in stories."""
    ID = "MEDIA_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MediaVideoStoryMissing(BadRequest):
    """A non-story video cannot be repubblished as a story (emitted when trying to resend a non-story video as a story using inputDocument)."""
    ID = "MEDIA_VIDEO_STORY_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MegagroupGeoRequired(BadRequest):
    """This method can only be invoked on a geogroup."""
    ID = "MEGAGROUP_GEO_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MegagroupIdInvalid(BadRequest):
    """The supergroup is invalid."""
    ID = "MEGAGROUP_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MegagroupPrehistoryHidden(BadRequest):
    """The action failed because the supergroup has the pre-history hidden."""
    ID = "MEGAGROUP_PREHISTORY_HIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MegagroupRequired(BadRequest):
    """The request can only be used with a supergroup."""
    ID = "MEGAGROUP_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageEditTimeExpired(BadRequest):
    """You can't edit this message anymore, too much time has passed since its creation."""
    ID = "MESSAGE_EDIT_TIME_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageEmpty(BadRequest):
    """The message sent is empty or contains invalid characters."""
    ID = "MESSAGE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageIdsEmpty(BadRequest):
    """The requested message doesn't exist or you provided no message id."""
    ID = "MESSAGE_IDS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageIdInvalid(BadRequest):
    """The provided message id is invalid."""
    ID = "MESSAGE_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageNotModified(BadRequest):
    """The message was not modified because you tried to edit it using the same content."""
    ID = "MESSAGE_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageNotReadYet(BadRequest):
    """The specified message wasn't read yet."""
    ID = "MESSAGE_NOT_READ_YET"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessagePollClosed(BadRequest):
    """You can't interact with a closed poll."""
    ID = "MESSAGE_POLL_CLOSED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageRequired(BadRequest):
    """A non-empty list of IDs must be passed to `id`."""
    ID = "MESSAGE_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageTooLong(BadRequest):
    """The provided message text is too long."""
    ID = "MESSAGE_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MessageTooOld(BadRequest):
    """The message is too old, the requested information is not available."""
    ID = "MESSAGE_TOO_OLD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MethodInvalid(BadRequest):
    """The specified API method is invalid and cannot be used."""
    ID = "METHOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MinDateInvalid(BadRequest):
    """The specified minimum date is invalid."""
    ID = "MIN_DATE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MonoforumFilterInvalid(BadRequest):
    """The specified filter is invalid."""
    ID = "MONOFORUM_FILTER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MonthInvalid(BadRequest):
    """The number of months specified in inputInvoicePremiumGiftStars.months is invalid."""
    ID = "MONTH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgIdInvalid(BadRequest):
    """The message ID used in the peer was invalid."""
    ID = "MSG_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgTooOld(BadRequest):
    """chat_read_mark_expire_period have passed since the message was sent, read receipts were deleted."""
    ID = "MSG_TOO_OLD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgVoiceMissing(BadRequest):
    """The message does not contain a voice message."""
    ID = "MSG_VOICE_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgVoiceTooLong(BadRequest):
    """The specified voice message is too long to be transcribed."""
    ID = "MSG_VOICE_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgWaitFailed(BadRequest):
    """A waiting call returned an error."""
    ID = "MSG_WAIT_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MtprotoClusterInvalid(BadRequest):
    """The MTProto cluster is invalid."""
    ID = "MTPROTO_CLUSTER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MultiMediaTooLong(BadRequest):
    """The album contains too many items."""
    ID = "MULTI_MEDIA_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NameInvalid(BadRequest):
    """The specified bot name is invalid."""
    ID = "NAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NeedActionMissing(BadRequest):
    """The caller didn't specify a valid action (either save or suggest) for the contact profile photo upload."""
    ID = "NEED_ACTION_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NewSaltInvalid(BadRequest):
    """The new salt is invalid."""
    ID = "NEW_SALT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NewSettingsEmpty(BadRequest):
    """No password is set on the current account, and no new password was specified in `new_settings`."""
    ID = "NEW_SETTINGS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NewSettingsInvalid(BadRequest):
    """The new settings are invalid."""
    ID = "NEW_SETTINGS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NextOffsetInvalid(BadRequest):
    """The next offset value is invalid."""
    ID = "NEXT_OFFSET_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NogeneralHideForbidden(BadRequest):
    """The hidden parameter is only valid for the General topic message_thread_id=1."""
    ID = "NOGENERAL_HIDE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NotEligible(BadRequest):
    """The current user is not eligible to join the Peer-to-Peer Login Program."""
    ID = "NOT_ELIGIBLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NotJoined(BadRequest):
    """The current user hasn't joined the Peer-to-Peer Login Program."""
    ID = "NOT_JOINED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NoPaymentNeeded(BadRequest):
    """The upgrade/transfer of the specified gift was already paid for or is free."""
    ID = "NO_PAYMENT_NEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OffsetInvalid(BadRequest):
    """The provided offset parameter is invalid."""
    ID = "OFFSET_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OffsetPeerIdInvalid(BadRequest):
    """The provided offset peer is invalid."""
    ID = "OFFSET_PEER_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OptionsTooMuch(BadRequest):
    """Too many poll options provided."""
    ID = "OPTIONS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OptionInvalid(BadRequest):
    """The option specified is invalid and does not exist in the target poll."""
    ID = "OPTION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class OrderInvalid(BadRequest):
    """The specified username order is invalid."""
    ID = "ORDER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PackShortNameInvalid(BadRequest):
    """Invalid sticker pack name. It must begin with a letter, can't contain consecutive underscores and must end in '_by_<bot username>'."""
    ID = "PACK_SHORT_NAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PackShortNameOccupied(BadRequest):
    """A sticker pack with this name already exists."""
    ID = "PACK_SHORT_NAME_OCCUPIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PackTitleInvalid(BadRequest):
    """The sticker pack title is invalid."""
    ID = "PACK_TITLE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PackTypeInvalid(BadRequest):
    """The masks and emojis flags are mutually exclusive."""
    ID = "PACK_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ParentPeerInvalid(BadRequest):
    """The specified `parent_peer` is invalid."""
    ID = "PARENT_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ParticipantsTooFew(BadRequest):
    """The chat doesn't have enough participants."""
    ID = "PARTICIPANTS_TOO_FEW"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ParticipantIdInvalid(BadRequest):
    """The specified participant ID is invalid."""
    ID = "PARTICIPANT_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ParticipantJoinMissing(BadRequest):
    """Trying to enable a presentation, when the user hasn't joined the Video Chat with [phone.joinGroupCall](https://core.telegram.org/method/phone.joinGroupCall)."""
    ID = "PARTICIPANT_JOIN_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ParticipantVersionOutdated(BadRequest):
    """The other participant is using an outdated Telegram app version."""
    ID = "PARTICIPANT_VERSION_OUTDATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasskeyCredentialNotFound(BadRequest):
    """The passkey credential not found."""
    ID = "PASSKEY_CREDENTIAL_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasskeyOriginMismatch(BadRequest):
    """Third-party clients currently don't support passkeys even when changing the origin."""
    ID = "PASSKEY_ORIGIN_MISMATCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasswordEmpty(BadRequest):
    """The provided password is empty."""
    ID = "PASSWORD_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasswordHashInvalid(BadRequest):
    """The two-step verification password is invalid."""
    ID = "PASSWORD_HASH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasswordMissing(BadRequest):
    """You must [enable 2FA](https://core.telegram.org/api/srp) before executing this operation."""
    ID = "PASSWORD_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasswordRecoveryExpired(BadRequest):
    """The recovery code has expired."""
    ID = "PASSWORD_RECOVERY_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasswordRecoveryNa(BadRequest):
    """No email was set, can't recover password via email."""
    ID = "PASSWORD_RECOVERY_NA"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasswordRequired(BadRequest):
    """The two-step verification password is required for this method."""
    ID = "PASSWORD_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PasswordTooFresh(BadRequest):
    """The two-step verification password was modified less than 24 hours ago, try again in {seconds} seconds."""
    ID = "PASSWORD_TOO_FRESH_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class PaymentCredentialsInvalid(BadRequest):
    """The specified payment credentials are invalid."""
    ID = "PAYMENT_CREDENTIALS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PaymentProviderInvalid(BadRequest):
    """The payment provider was not recognised or its token was invalid."""
    ID = "PAYMENT_PROVIDER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PaymentRequired(BadRequest):
    """The payment is required."""
    ID = "PAYMENT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PeersListEmpty(BadRequest):
    """The specified list of peers is empty."""
    ID = "PEERS_LIST_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PeerFlood(BadRequest):
    """The current account is limited, you cannot execute this action, check @spambot for more info."""
    ID = "PEER_FLOOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PeerHistoryEmpty(BadRequest):
    """You can't pin an empty chat with a user."""
    ID = "PEER_HISTORY_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PeerIdInvalid(BadRequest):
    """The peer id being used is invalid or not known yet. Make sure you meet the peer before interacting with it."""
    ID = "PEER_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PeerIdNotSupported(BadRequest):
    """The provided peer id is not supported."""
    ID = "PEER_ID_NOT_SUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PeerTypesInvalid(BadRequest):
    """The passed [keyboardButtonSwitchInline](https://core.telegram.org/constructor/keyboardButtonSwitchInline).`peer_types` field is invalid."""
    ID = "PEER_TYPES_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PersistentTimestampEmpty(BadRequest):
    """The pts argument is empty."""
    ID = "PERSISTENT_TIMESTAMP_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PersistentTimestampInvalid(BadRequest):
    """The persistent timestamp is invalid."""
    ID = "PERSISTENT_TIMESTAMP_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneCodeEmpty(BadRequest):
    """The phone code is missing."""
    ID = "PHONE_CODE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneCodeExpired(BadRequest):
    """The provided confirmation code has expired. Make sure you haven't sent it to anyone else and use the code on the same connection."""
    ID = "PHONE_CODE_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneCodeHashEmpty(BadRequest):
    """The phone code hash is missing."""
    ID = "PHONE_CODE_HASH_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneCodeInvalid(BadRequest):
    """The provided confirmation code is invalid."""
    ID = "PHONE_CODE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneHashExpired(BadRequest):
    """An invalid or expired phone code hash was provided."""
    ID = "PHONE_HASH_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNotOccupied(BadRequest):
    """No user is associated to the specified phone number."""
    ID = "PHONE_NOT_OCCUPIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNumberAppSignupForbidden(BadRequest):
    """You can't sign up using this app."""
    ID = "PHONE_NUMBER_APP_SIGNUP_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNumberBanned(BadRequest):
    """The specified phone number is banned from Telegram and cannot be used."""
    ID = "PHONE_NUMBER_BANNED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNumberFlood(BadRequest):
    """This number has tried to login too many times."""
    ID = "PHONE_NUMBER_FLOOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNumberInvalid(BadRequest):
    """The phone number is invalid."""
    ID = "PHONE_NUMBER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNumberOccupied(BadRequest):
    """The phone number is already in use."""
    ID = "PHONE_NUMBER_OCCUPIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhoneNumberUnoccupied(BadRequest):
    """The phone number is not yet being used."""
    ID = "PHONE_NUMBER_UNOCCUPIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhonePasswordProtected(BadRequest):
    """This phone is password protected."""
    ID = "PHONE_PASSWORD_PROTECTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoContentTypeInvalid(BadRequest):
    """The photo content type is invalid."""
    ID = "PHOTO_CONTENT_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoContentUrlEmpty(BadRequest):
    """The photo content URL is empty."""
    ID = "PHOTO_CONTENT_URL_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoCropFileMissing(BadRequest):
    """Photo crop file missing."""
    ID = "PHOTO_CROP_FILE_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoCropSizeSmall(BadRequest):
    """Photo is too small."""
    ID = "PHOTO_CROP_SIZE_SMALL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoExtInvalid(BadRequest):
    """The extension of the photo is invalid."""
    ID = "PHOTO_EXT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoFileMissing(BadRequest):
    """Profile photo file missing."""
    ID = "PHOTO_FILE_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoIdInvalid(BadRequest):
    """Photo ID invalid."""
    ID = "PHOTO_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoInvalid(BadRequest):
    """Photo invalid."""
    ID = "PHOTO_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoInvalidDimensions(BadRequest):
    """The photo dimensions are invalid."""
    ID = "PHOTO_INVALID_DIMENSIONS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoSaveFileInvalid(BadRequest):
    """The photo you tried to send cannot be saved by Telegram."""
    ID = "PHOTO_SAVE_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoThumbUrlEmpty(BadRequest):
    """The photo thumbnail URL is empty."""
    ID = "PHOTO_THUMB_URL_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoThumbUrlInvalid(BadRequest):
    """The photo thumb URL is invalid."""
    ID = "PHOTO_THUMB_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PinnedDialogsTooMuch(BadRequest):
    """Too many pinned dialogs."""
    ID = "PINNED_DIALOGS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PinnedTooMuch(BadRequest):
    """There are too many pinned topics, unpin some first."""
    ID = "PINNED_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PinnedTopicNotModified(BadRequest):
    """The pinned topic was not modified."""
    ID = "PINNED_TOPIC_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PinRestricted(BadRequest):
    """You can't pin messages in private chats with other people."""
    ID = "PIN_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PlatformInvalid(BadRequest):
    """The provided platform is invalid. Allowed values are "android", "ios", "wp", "bb", "desktop", "web", "ubp", "other"."""
    ID = "PLATFORM_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollAnswersInvalid(BadRequest):
    """Invalid poll answers were provided."""
    ID = "POLL_ANSWERS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollAnswerInvalid(BadRequest):
    """One of the poll answers is not acceptable."""
    ID = "POLL_ANSWER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollOptionDuplicate(BadRequest):
    """A duplicate option was sent in the same poll."""
    ID = "POLL_OPTION_DUPLICATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollOptionInvalid(BadRequest):
    """IA poll option used invalid data (the data may be too long)."""
    ID = "POLL_OPTION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollQuestionInvalid(BadRequest):
    """The poll question is invalid."""
    ID = "POLL_QUESTION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollUnsupported(BadRequest):
    """This layer does not support polls in the invoked method."""
    ID = "POLL_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PollVoteRequired(BadRequest):
    """Cast a vote in the poll before calling this method."""
    ID = "POLL_VOTE_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PrecheckoutFailed(BadRequest):
    """Precheckout failed. Probably you don't have enough funds to complete the purchase."""
    ID = "PRECHECKOUT_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PremiumAccountRequired(BadRequest):
    """A premium account is required to execute this action."""
    ID = "PREMIUM_ACCOUNT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PremiumGiftcodeWasRefunded(BadRequest):
    """This gift code can't be redeemed because the giveaway organizer requested a refund."""
    ID = "PREMIUM_GIFTCODE_WAS_REFUNDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PremiumPurposeInvalid(BadRequest):
    """The specified InputStorePaymentPurpose is invalid."""
    ID = "PREMIUM_PURPOSE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PricingChatInvalid(BadRequest):
    """The pricing for the [subscription](https://core.telegram.org/api/subscriptions) is invalid, the maximum price is specified in the [`stars_subscription_amount_max` config key »](https://core.telegram.org/api/config#stars-subscription-amount-max)."""
    ID = "PRICING_CHAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PrivacyKeyInvalid(BadRequest):
    """The privacy key is invalid."""
    ID = "PRIVACY_KEY_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PrivacyTooLong(BadRequest):
    """Your privacy exception list has exceeded the maximum capacity."""
    ID = "PRIVACY_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PrivacyValueInvalid(BadRequest):
    """The specified privacy rule combination is invalid."""
    ID = "PRIVACY_VALUE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PublicBroadcastExpected(BadRequest):
    """A public channel was expected, but something else was provided."""
    ID = "PUBLIC_BROADCAST_EXPECTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PublicKeyInvalid(BadRequest):
    """The specified e2e public key is invalid."""
    ID = "PUBLIC_KEY_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PublicKeyRequired(BadRequest):
    """A public key is required."""
    ID = "PUBLIC_KEY_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PurposeInvalid(BadRequest):
    """The specified payment purpose is invalid."""
    ID = "PURPOSE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QueryIdEmpty(BadRequest):
    """The query ID is empty."""
    ID = "QUERY_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QueryIdInvalid(BadRequest):
    """The query ID is invalid."""
    ID = "QUERY_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QueryTooShort(BadRequest):
    """The query string is too short."""
    ID = "QUERY_TOO_SHORT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuickRepliesBotNotAllowed(BadRequest):
    """[Quick replies](https://core.telegram.org/api/business#quick-reply-shortcuts) cannot be used by bots."""
    ID = "QUICK_REPLIES_BOT_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuickRepliesTooMuch(BadRequest):
    """A maximum of [appConfig.`quick_replies_limit`](https://core.telegram.org/api/config#quick-replies-limit) shortcuts may be created, the limit was reached."""
    ID = "QUICK_REPLIES_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuizAnswerMissing(BadRequest):
    """You can forward a quiz while hiding the original author only after choosing an option in the quiz."""
    ID = "QUIZ_ANSWER_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuizCorrectAnswersEmpty(BadRequest):
    """No correct quiz answer was specified."""
    ID = "QUIZ_CORRECT_ANSWERS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuizCorrectAnswersTooMuch(BadRequest):
    """You specified too many correct answers in a quiz, quizzes can only have one right answer!."""
    ID = "QUIZ_CORRECT_ANSWERS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuizCorrectAnswerInvalid(BadRequest):
    """An invalid value was provided to the correct_answers field."""
    ID = "QUIZ_CORRECT_ANSWER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuizMultipleInvalid(BadRequest):
    """A quiz can't have multiple answers."""
    ID = "QUIZ_MULTIPLE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class QuoteTextInvalid(BadRequest):
    """The specified quote text is invalid."""
    ID = "QUOTE_TEXT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RaiseHandForbidden(BadRequest):
    """You cannot raise your hand."""
    ID = "RAISE_HAND_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RandomIdDuplicate(BadRequest):
    """You provided a random ID that was already used."""
    ID = "RANDOM_ID_DUPLICATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RandomIdEmpty(BadRequest):
    """The random ID is empty."""
    ID = "RANDOM_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RandomIdExpired(BadRequest):
    """The specified `random_id` was expired (most likely it didn't follow the required `uint64_t random_id = (time() << 32) | ((uint64_t)random_uint32_t())` format, or the specified time is too far in the past)."""
    ID = "RANDOM_ID_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RandomIdInvalid(BadRequest):
    """The provided random ID is invalid."""
    ID = "RANDOM_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RandomLengthInvalid(BadRequest):
    """The random length is invalid."""
    ID = "RANDOM_LENGTH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RangesInvalid(BadRequest):
    """Invalid range provided."""
    ID = "RANGES_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RankInvalid(BadRequest):
    """The specified member tag is invalid."""
    ID = "RANK_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReactionsCountInvalid(BadRequest):
    """The count of the reactions should be less than `stars_paid_reaction_amount_max` stars, you can't react with more number of stars, see [the docs for more info](https://core.telegram.org/api/config#client-configuration)."""
    ID = "REACTIONS_COUNT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReactionsTooMany(BadRequest):
    """Non-premium users, can set up only one reaction per message."""
    ID = "REACTIONS_TOO_MANY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReactionEmpty(BadRequest):
    """The specified reaction is empty."""
    ID = "REACTION_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReactionInvalid(BadRequest):
    """The specified reaction is invalid (only valid emoji are allowed)."""
    ID = "REACTION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReceiptEmpty(BadRequest):
    """The specified receipt is empty."""
    ID = "RECEIPT_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReflectorNotAvailable(BadRequest):
    """The call reflector is not available."""
    ID = "REFLECTOR_NOT_AVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyMarkupBuyEmpty(BadRequest):
    """Reply markup for buy button empty."""
    ID = "REPLY_MARKUP_BUY_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyMarkupGameEmpty(BadRequest):
    """A game message is being edited, but the newly provided keyboard doesn't have a keyboardButtonGame button."""
    ID = "REPLY_MARKUP_GAME_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyMarkupInvalid(BadRequest):
    """The provided reply markup is invalid."""
    ID = "REPLY_MARKUP_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyMarkupTooLong(BadRequest):
    """The specified reply markup is too long."""
    ID = "REPLY_MARKUP_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyMessagesTooMuch(BadRequest):
    """Each shortcut can contain a maximum of [appConfig.`quick_reply_messages_limit`](https://core.telegram.org/api/config#quick-reply-messages-limit) messages, the limit was reached."""
    ID = "REPLY_MESSAGES_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyMessageIdInvalid(BadRequest):
    """The specified reply message id is invalid."""
    ID = "REPLY_MESSAGE_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyToInvalid(BadRequest):
    """The specified `reply_to` field is invalid."""
    ID = "REPLY_TO_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyToMonoforumPeerInvalid(BadRequest):
    """The specified `reply_to` field is invalid."""
    ID = "REPLY_TO_MONOFORUM_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ReplyToUserInvalid(BadRequest):
    """The replied-to user is invalid."""
    ID = "REPLY_TO_USER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RequestMsgExpired(BadRequest):
    """The request specified in request_msg_id has already expired."""
    ID = "REQUEST_MSG_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RequestTokenInvalid(BadRequest):
    """The master DC did not accept the `request_token` from the CDN DC. Continue downloading the file from the master DC using upload.getFile."""
    ID = "REQUEST_TOKEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResellStarsTooFew(BadRequest):
    """The offered price is too low."""
    ID = "RESELL_STARS_TOO_FEW"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResellStarsTooMuch(BadRequest):
    """The offered price is too high."""
    ID = "RESELL_STARS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResetRequestMissing(BadRequest):
    """No password reset is in progress."""
    ID = "RESET_REQUEST_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResultsTooMuch(BadRequest):
    """The result contains too many items."""
    ID = "RESULTS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResultIdDuplicate(BadRequest):
    """The result contains items with duplicated identifiers."""
    ID = "RESULT_ID_DUPLICATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResultIdEmpty(BadRequest):
    """Result ID empty."""
    ID = "RESULT_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResultIdInvalid(BadRequest):
    """The given result cannot be used to send the selection to the bot."""
    ID = "RESULT_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ResultTypeInvalid(BadRequest):
    """The result type is invalid."""
    ID = "RESULT_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RevoteNotAllowed(BadRequest):
    """You cannot change your vote."""
    ID = "REVOTE_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RichMessageUnsupported(BadRequest):
    """The rich message is not supported."""
    ID = "RICH_MESSAGE_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RightsNotModified(BadRequest):
    """The new admin rights are equal to the old rights, no change was made."""
    ID = "RIGHTS_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RingtoneInvalid(BadRequest):
    """The specified ringtone is invalid."""
    ID = "RINGTONE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RingtoneMimeInvalid(BadRequest):
    """The MIME type for the ringtone is invalid."""
    ID = "RINGTONE_MIME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RsaDecryptFailed(BadRequest):
    """Internal RSA decryption failed."""
    ID = "RSA_DECRYPT_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SavedDialogsUnsupported(BadRequest):
    """You cannot use this method."""
    ID = "SAVED_DIALOGS_UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SavedIdEmpty(BadRequest):
    """The passed inputSavedStarGiftChat.saved_id is empty."""
    ID = "SAVED_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SavedPeerInvalid(BadRequest):
    """The saved peer is invalid."""
    ID = "SAVED_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ScheduleBotNotAllowed(BadRequest):
    """Bots are not allowed to schedule messages."""
    ID = "SCHEDULE_BOT_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ScheduleDateInvalid(BadRequest):
    """Invalid schedule date provided."""
    ID = "SCHEDULE_DATE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ScheduleDateTooLate(BadRequest):
    """The date you tried to schedule is too far in the future (more than one year)."""
    ID = "SCHEDULE_DATE_TOO_LATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ScheduleStatusPrivate(BadRequest):
    """You cannot schedule a message until the person comes online if their privacy does not show this information."""
    ID = "SCHEDULE_STATUS_PRIVATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ScheduleTooMuch(BadRequest):
    """You tried to schedule too many messages in this chat."""
    ID = "SCHEDULE_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ScoreInvalid(BadRequest):
    """The specified game score is invalid."""
    ID = "SCORE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SearchQueryEmpty(BadRequest):
    """The search query is empty."""
    ID = "SEARCH_QUERY_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SearchWithLinkNotSupported(BadRequest):
    """You cannot provide a search query and an invite link at the same time."""
    ID = "SEARCH_WITH_LINK_NOT_SUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SecondsInvalid(BadRequest):
    """The seconds interval is invalid."""
    ID = "SECONDS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SecureSecretRequired(BadRequest):
    """A secure secret is required."""
    ID = "SECURE_SECRET_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SelfDeleteRestricted(BadRequest):
    """Business bots can't delete messages just for the user, `revoke` **must** be set."""
    ID = "SELF_DELETE_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SendAsPeerInvalid(BadRequest):
    """You can't send messages as the specified peer."""
    ID = "SEND_AS_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SendMessageGameInvalid(BadRequest):
    """An inputBotInlineMessageGame can only be contained in an inputBotInlineResultGame, not in an inputBotInlineResult/inputBotInlineResultPhoto/etc."""
    ID = "SEND_MESSAGE_GAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SendMessageMediaInvalid(BadRequest):
    """The message media is invalid."""
    ID = "SEND_MESSAGE_MEDIA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SendMessageTypeInvalid(BadRequest):
    """The message type is invalid."""
    ID = "SEND_MESSAGE_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SessionTooFresh(BadRequest):
    """This session was created less than 24 hours ago, try again in {seconds} seconds."""
    ID = "SESSION_TOO_FRESH_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class SettingsInvalid(BadRequest):
    """Invalid settings were provided."""
    ID = "SETTINGS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class Sha256HashInvalid(BadRequest):
    """The provided SHA256 hash is invalid."""
    ID = "SHA256_HASH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ShortcutInvalid(BadRequest):
    """The specified shortcut is invalid."""
    ID = "SHORTCUT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ShortnameOccupyFailed(BadRequest):
    """An error occurred when trying to register the short-name used for the sticker pack. Try a different name."""
    ID = "SHORTNAME_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ShortNameInvalid(BadRequest):
    """The specified short name is invalid."""
    ID = "SHORT_NAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ShortNameOccupied(BadRequest):
    """The specified short name is already in use."""
    ID = "SHORT_NAME_OCCUPIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SlotsEmpty(BadRequest):
    """The specified slot list is empty."""
    ID = "SLOTS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SlowmodeMultiMsgsDisabled(BadRequest):
    """Slowmode is enabled, you cannot forward multiple messages to this group."""
    ID = "SLOWMODE_MULTI_MSGS_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SlugInvalid(BadRequest):
    """The specified invoice slug is invalid."""
    ID = "SLUG_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SmsjobIdInvalid(BadRequest):
    """The specified job ID is invalid."""
    ID = "SMSJOB_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SmsCodeCreateFailed(BadRequest):
    """An error occurred while creating the SMS code."""
    ID = "SMS_CODE_CREATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SolutionMediaEmpty(BadRequest):
    """The solution_media is empty."""
    ID = "SOLUTION_MEDIA_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SolutionMediaTypeInvalid(BadRequest):
    """The solution_media is invalid."""
    ID = "SOLUTION_MEDIA_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SrpAInvalid(BadRequest):
    """The specified inputCheckPasswordSRP.A value is invalid."""
    ID = "SRP_A_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SrpIdInvalid(BadRequest):
    """Invalid SRP ID provided."""
    ID = "SRP_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SrpPasswordChanged(BadRequest):
    """The password has changed."""
    ID = "SRP_PASSWORD_CHANGED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftAlreadyBurned(BadRequest):
    """The provided gift is already burned."""
    ID = "STARGIFT_ALREADY_BURNED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftAlreadyConverted(BadRequest):
    """The provided star gift already converted to stars."""
    ID = "STARGIFT_ALREADY_CONVERTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftAlreadyRefunded(BadRequest):
    """The specified star gift was already refunded."""
    ID = "STARGIFT_ALREADY_REFUNDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftAlreadyTransferred(BadRequest):
    """The provided star gift is already transferred."""
    ID = "STARGIFT_ALREADY_TRANSFERRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftAlreadyUpgraded(BadRequest):
    """This star gift was already upgraded before."""
    ID = "STARGIFT_ALREADY_UPGRADED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftAttributeInvalid(BadRequest):
    """The provided gift attribute is invalid."""
    ID = "STARGIFT_ATTRIBUTE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftConvertTooOld(BadRequest):
    """This gift can no longer be converted into stars."""
    ID = "STARGIFT_CONVERT_TOO_OLD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftExportUnavailable(BadRequest):
    """This gift is not available for export yet."""
    ID = "STARGIFT_EXPORT_UNAVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftInvalid(BadRequest):
    """The passed [inputInvoiceStarGift](https://core.telegram.org/constructor/inputInvoiceStarGift) is invalid."""
    ID = "STARGIFT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftMessageInvalid(BadRequest):
    """The provided message for this gift is invalid."""
    ID = "STARGIFT_MESSAGE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftNotFound(BadRequest):
    """The specified star gift was not found."""
    ID = "STARGIFT_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftNotOwner(BadRequest):
    """You can't control this gift because it doesn't belong to you."""
    ID = "STARGIFT_NOT_OWNER"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftNotUnique(BadRequest):
    """You can't transfer a non-collectible gift."""
    ID = "STARGIFT_NOT_UNIQUE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftObjectInvalid(BadRequest):
    """The specified star gift object is invalid."""
    ID = "STARGIFT_OBJECT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftOfferInvalid(BadRequest):
    """The specified offer amount is invalid."""
    ID = "STARGIFT_OFFER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftOfferNotAllowed(BadRequest):
    """You can't send a purchase offer for this gift."""
    ID = "STARGIFT_OFFER_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftOwnerInvalid(BadRequest):
    """The specified gift owner is invalid."""
    ID = "STARGIFT_OWNER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftPeerInvalid(BadRequest):
    """The specified inputSavedStarGiftChat.peer is invalid."""
    ID = "STARGIFT_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftResellCurrencyNotAllowed(BadRequest):
    """The currency provided for gift resell is not allowed."""
    ID = "STARGIFT_RESELL_CURRENCY_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftResellNotAllowed(BadRequest):
    """You can't buy this gift. Someone else may have already bought it or this gift is not for sale."""
    ID = "STARGIFT_RESELL_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftResellTooEarly(BadRequest):
    """A wait of {seconds} seconds is required to resell this gift."""
    ID = "STARGIFT_RESELL_TOO_EARLY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class StargiftSlugInvalid(BadRequest):
    """The provided star gift slug is invalid (must match the format CollectionName-123)."""
    ID = "STARGIFT_SLUG_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftTransferTooEarly(BadRequest):
    """A wait of {seconds} seconds is required to transfer this gift."""
    ID = "STARGIFT_TRANSFER_TOO_EARLY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class StargiftUpgradeUnavailable(BadRequest):
    """Gift is not available for upgrade yet."""
    ID = "STARGIFT_UPGRADE_UNAVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftUsageLimited(BadRequest):
    """The gift is sold out."""
    ID = "STARGIFT_USAGE_LIMITED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StargiftUserUsageLimited(BadRequest):
    """You've reached the starGift.limited_per_user limit, you can't buy any more gifts of this type."""
    ID = "STARGIFT_USER_USAGE_LIMITED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarrefAwaitingEnd(BadRequest):
    """The previous referral program was terminated less than 24 hours ago: further changes can be made after the date specified in userFull.starref_program.end_date."""
    ID = "STARREF_AWAITING_END"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarrefExpired(BadRequest):
    """The specified referral link is expired."""
    ID = "STARREF_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarrefHashRevoked(BadRequest):
    """The specified affiliate link was already revoked."""
    ID = "STARREF_HASH_REVOKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarrefMonthsTooLow(BadRequest):
    """The `duration_months` parameter must be between 0 and 36."""
    ID = "STARREF_MONTHS_TOO_LOW"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarrefPermilleInvalid(BadRequest):
    """The specified commission_permille is invalid: the minimum and maximum values for this parameter are contained in the [starref_min_commission_permille](https://core.telegram.org/api/config#starref-min-commission-permille) and [starref_max_commission_permille](https://core.telegram.org/api/config#starref-max-commission-permille) client configuration parameters."""
    ID = "STARREF_PERMILLE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarrefPermilleTooLow(BadRequest):
    """The specified commission_permille is too low: the minimum and maximum values for this parameter are contained in the [starref_min_commission_permille](https://core.telegram.org/api/config#starref-min-commission-permille) and [starref_max_commission_permille](https://core.telegram.org/api/config#starref-max-commission-permille) client configuration parameters."""
    ID = "STARREF_PERMILLE_TOO_LOW"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarsAmountInvalid(BadRequest):
    """The specified `paid_stars` amount is invalid."""
    ID = "STARS_AMOUNT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarsFormAmountMismatch(BadRequest):
    """The stars form amount mismatch."""
    ID = "STARS_FORM_AMOUNT_MISMATCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarsInvoiceInvalid(BadRequest):
    """The specified Telegram Star invoice is invalid."""
    ID = "STARS_INVOICE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StarsPaymentRequired(BadRequest):
    """To import this chat invite link, you must first [pay for the associated Telegram Star subscription »](https://core.telegram.org/api/subscriptions#channel-subscriptions)."""
    ID = "STARS_PAYMENT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StartParamEmpty(BadRequest):
    """The start parameter is empty."""
    ID = "START_PARAM_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StartParamInvalid(BadRequest):
    """The start parameter invalid."""
    ID = "START_PARAM_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StartParamTooLong(BadRequest):
    """The start parameter is too long."""
    ID = "START_PARAM_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerpackStickersTooMuch(BadRequest):
    """There are too many stickers in this stickerpack, you can't add any more."""
    ID = "STICKERPACK_STICKERS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickersetInvalid(BadRequest):
    """The requested sticker set is invalid."""
    ID = "STICKERSET_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickersetNotModified(BadRequest):
    """TThe sticker set is not modified."""
    ID = "STICKERSET_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickersEmpty(BadRequest):
    """No sticker provided."""
    ID = "STICKERS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickersTooMuch(BadRequest):
    """There are too many stickers in this stickerpack, you can't add any more."""
    ID = "STICKERS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerDocumentInvalid(BadRequest):
    """The specified sticker document is invalid."""
    ID = "STICKER_DOCUMENT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerEmojiInvalid(BadRequest):
    """Sticker emoji invalid."""
    ID = "STICKER_EMOJI_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerFileInvalid(BadRequest):
    """Sticker file invalid."""
    ID = "STICKER_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerGifDimensions(BadRequest):
    """The specified video sticker has invalid dimensions."""
    ID = "STICKER_GIF_DIMENSIONS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerIdInvalid(BadRequest):
    """The provided sticker ID is invalid."""
    ID = "STICKER_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerInvalid(BadRequest):
    """The provided sticker is invalid."""
    ID = "STICKER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerMimeInvalid(BadRequest):
    """The specified sticker MIME type is invalid. Make sure to pass a valid image file for the right InputFile parameter."""
    ID = "STICKER_MIME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerPngDimensions(BadRequest):
    """SThe sticker png dimensions are invalid."""
    ID = "STICKER_PNG_DIMENSIONS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerPngNopng(BadRequest):
    """Stickers must be png files but the provided image was not a png."""
    ID = "STICKER_PNG_NOPNG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerTgsNodoc(BadRequest):
    """You must send the animated sticker as a document."""
    ID = "STICKER_TGS_NODOC"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerTgsNotgs(BadRequest):
    """A tgs sticker file was expected, but something else was provided."""
    ID = "STICKER_TGS_NOTGS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerThumbPngNopng(BadRequest):
    """IA png sticker thumbnail file was expected, but something else was provided."""
    ID = "STICKER_THUMB_PNG_NOPNG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerThumbTgsNotgs(BadRequest):
    """Incorrect stickerset TGS thumb file provided."""
    ID = "STICKER_THUMB_TGS_NOTGS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerVideoBig(BadRequest):
    """The specified video sticker is too big."""
    ID = "STICKER_VIDEO_BIG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerVideoNodoc(BadRequest):
    """You must send the video sticker as a document."""
    ID = "STICKER_VIDEO_NODOC"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StickerVideoNowebm(BadRequest):
    """A webm video file was expected, but something else was provided."""
    ID = "STICKER_VIDEO_NOWEBM"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StorageKeyRequired(BadRequest):
    """A cloud storage key is required."""
    ID = "STORAGE_KEY_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoriesNeverCreated(BadRequest):
    """This peer hasn't ever posted any stories."""
    ID = "STORIES_NEVER_CREATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoriesTooMuch(BadRequest):
    """You have hit the maximum active stories limit as specified by the [`story_expiring_limit_*` client configuration parameters](https://core.telegram.org/api/config#story-expiring-limit-default): you should buy a [Premium](https://core.telegram.org/api/premium) subscription, delete an active story, or wait for the oldest story to expire."""
    ID = "STORIES_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoryIdEmpty(BadRequest):
    """You specified no story IDs."""
    ID = "STORY_ID_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoryIdInvalid(BadRequest):
    """The specified story ID is invalid."""
    ID = "STORY_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoryLiveAlready(BadRequest):
    """The user or the chat has an active live story with identifier {story_id}."""
    ID = "STORY_LIVE_ALREADY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "story_id"
    """``str``: Name of the property that holds this error's value"""

    @property
    def story_id(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class StoryNotModified(BadRequest):
    """The new story information you passed is equal to the previous story information, thus it wasn't modified."""
    ID = "STORY_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoryPeriodInvalid(BadRequest):
    """The specified story period is invalid for this account."""
    ID = "STORY_PERIOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoryPublicMissing(BadRequest):
    """The story you are trying to access or manipulate is not publicly available."""
    ID = "STORY_PUBLIC_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StorySendFloodMonthly(BadRequest):
    """You've hit the monthly story limit as specified by the [`stories_sent_monthly_limit_*` client configuration parameters](https://core.telegram.org/api/config#stories-sent-monthly-limit-default): wait {seconds} seconds before posting a new story."""
    ID = "STORY_SEND_FLOOD_MONTHLY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class StorySendFloodWeekly(BadRequest):
    """You've hit the weekly story limit as specified by the [`stories_sent_weekly_limit_*` client configuration parameters](https://core.telegram.org/api/config#stories-sent-weekly-limit-default): wait {seconds} seconds before posting a new story."""
    ID = "STORY_SEND_FLOOD_WEEKLY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class SubscriptionExportMissing(BadRequest):
    """You cannot send a [bot subscription invoice](https://core.telegram.org/api/subscriptions#bot-subscriptions) directly, you may only create invoice links using [payments.exportInvoice](https://core.telegram.org/method/payments.exportInvoice)."""
    ID = "SUBSCRIPTION_EXPORT_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SubscriptionIdInvalid(BadRequest):
    """The specified subscription_id is invalid."""
    ID = "SUBSCRIPTION_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SubscriptionPeriodInvalid(BadRequest):
    """The specified subscription_pricing.period is invalid."""
    ID = "SUBSCRIPTION_PERIOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SuggestedPostAmountInvalid(BadRequest):
    """The specified price for the suggested post is invalid."""
    ID = "SUGGESTED_POST_AMOUNT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SuggestedPostPeerInvalid(BadRequest):
    """You cannot send suggested posts to non-[monoforum](https://core.telegram.org/api/monoforum) peers."""
    ID = "SUGGESTED_POST_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SwitchPmTextEmpty(BadRequest):
    """The switch_pm.text field was empty."""
    ID = "SWITCH_PM_TEXT_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SwitchWebviewUrlInvalid(BadRequest):
    """The URL specified in switch_webview.url is invalid!."""
    ID = "SWITCH_WEBVIEW_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TakeoutInvalid(BadRequest):
    """The specified takeout ID is invalid."""
    ID = "TAKEOUT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TakeoutRequired(BadRequest):
    """The method must be invoked inside a [takeout](https://core.telegram.org/api/takeout) session."""
    ID = "TAKEOUT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TaskAlreadyExists(BadRequest):
    """An email reset was already requested."""
    ID = "TASK_ALREADY_EXISTS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TempAuthKeyAlreadyBound(BadRequest):
    """The passed temporary key is already bound to another **perm_auth_key_id**."""
    ID = "TEMP_AUTH_KEY_ALREADY_BOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TempAuthKeyEmpty(BadRequest):
    """The temporary auth key provided is empty."""
    ID = "TEMP_AUTH_KEY_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TermsUrlInvalid(BadRequest):
    """The specified [invoice](https://core.telegram.org/constructor/invoice).`terms_url` is invalid."""
    ID = "TERMS_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TextdraftPeerInvalid(BadRequest):
    """The specified peer is invalid."""
    ID = "TEXTDRAFT_PEER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ThemeFileInvalid(BadRequest):
    """Invalid theme file provided."""
    ID = "THEME_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ThemeFormatInvalid(BadRequest):
    """Invalid theme format provided."""
    ID = "THEME_FORMAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ThemeInvalid(BadRequest):
    """Invalid theme provided."""
    ID = "THEME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ThemeMimeInvalid(BadRequest):
    """You cannot create this theme because the mime-type is invalid."""
    ID = "THEME_MIME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ThemeParamsInvalid(BadRequest):
    """The specified `theme_params` field is invalid."""
    ID = "THEME_PARAMS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ThemeSlugInvalid(BadRequest):
    """The specified theme slug is invalid."""
    ID = "THEME_SLUG_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ThemeTitleInvalid(BadRequest):
    """The specified theme title is invalid."""
    ID = "THEME_TITLE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TimezoneInvalid(BadRequest):
    """The specified timezone does not exist."""
    ID = "TIMEZONE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TitleInvalid(BadRequest):
    """The specified stickerpack title is invalid."""
    ID = "TITLE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TmpPasswordDisabled(BadRequest):
    """The temporary password is disabled."""
    ID = "TMP_PASSWORD_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TmpPasswordInvalid(BadRequest):
    """The temporary password is invalid."""
    ID = "TMP_PASSWORD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TodoItemsEmpty(BadRequest):
    """A checklist was specified, but no [checklist items](https://core.telegram.org/api/todo) were passed."""
    ID = "TODO_ITEMS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TodoItemsTooMuch(BadRequest):
    """You specified too many todo list items."""
    ID = "TODO_ITEMS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TodoItemDuplicate(BadRequest):
    """The provided ToDo task already exists."""
    ID = "TODO_ITEM_DUPLICATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TodoNotModified(BadRequest):
    """No todo items were specified, so no changes were made to the todo list."""
    ID = "TODO_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TokenEmpty(BadRequest):
    """The specified token is empty."""
    ID = "TOKEN_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TokenInvalid(BadRequest):
    """The provided token is invalid."""
    ID = "TOKEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TokenSecretInvalid(BadRequest):
    """The specified token secret is invalid."""
    ID = "TOKEN_SECRET_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TokenTypeInvalid(BadRequest):
    """The specified token type is invalid."""
    ID = "TOKEN_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicsEmpty(BadRequest):
    """You specified no topic IDs."""
    ID = "TOPICS_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicClosed(BadRequest):
    """This topic was closed, you can't send messages to it anymore."""
    ID = "TOPIC_CLOSED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicCloseSeparately(BadRequest):
    """The `close` flag cannot be provided together with any of the other flags."""
    ID = "TOPIC_CLOSE_SEPARATELY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicDeleted(BadRequest):
    """The specified topic was deleted."""
    ID = "TOPIC_DELETED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicHideSeparately(BadRequest):
    """The `hide` flag cannot be provided together with any of the other flags."""
    ID = "TOPIC_HIDE_SEPARATELY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicIdInvalid(BadRequest):
    """The specified topic ID is invalid."""
    ID = "TOPIC_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicNotModified(BadRequest):
    """The updated topic info is equal to the current topic info, nothing was changed."""
    ID = "TOPIC_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TopicTitleEmpty(BadRequest):
    """The specified topic title is empty."""
    ID = "TOPIC_TITLE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ToIdInvalid(BadRequest):
    """The specified `to_id` of the passed inputInvoiceStarGiftResale or inputInvoiceStarGiftTransfer is invalid."""
    ID = "TO_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ToLangInvalid(BadRequest):
    """The specified destination language is invalid."""
    ID = "TO_LANG_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TransactionIdInvalid(BadRequest):
    """The specified transaction ID is invalid."""
    ID = "TRANSACTION_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TranscriptionFailed(BadRequest):
    """Telegram is having internal problems. Please try again later to transcribe the audio."""
    ID = "TRANSCRIPTION_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TranslateReqQuotaExceeded(BadRequest):
    """Translation is currently unavailable due to a temporary server-side lack of resources."""
    ID = "TRANSLATE_REQ_QUOTA_EXCEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TranslationsDisabled(BadRequest):
    """Translation is disabled."""
    ID = "TRANSLATIONS_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TranslationsDisabledAlt(BadRequest):
    """Translation is disabled."""
    ID = "TRANSLATIONS_DISABLED_ALT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TtlDaysInvalid(BadRequest):
    """The provided TTL days is invalid."""
    ID = "TTL_DAYS_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TtlMediaInvalid(BadRequest):
    """The media does not support self-destruction."""
    ID = "TTL_MEDIA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TtlPeriodInvalid(BadRequest):
    """The specified TTL period is invalid."""
    ID = "TTL_PERIOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TypesEmpty(BadRequest):
    """The types parameter is empty."""
    ID = "TYPES_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TypeConstructorInvalid(BadRequest):
    """The type constructor is invalid."""
    ID = "TYPE_CONSTRUCTOR_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UnknownError400(BadRequest):
    """Unknown error."""
    ID = "UNKNOWN_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class Unsupported(BadRequest):
    """This method is not supported."""
    ID = "UNSUPPORTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UntilDateInvalid(BadRequest):
    """That date parameter is invalid."""
    ID = "UNTIL_DATE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UrlExpired(BadRequest):
    """The specified OAuth request has expired."""
    ID = "URL_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UrlInvalid(BadRequest):
    """The URL provided is invalid."""
    ID = "URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsageLimitInvalid(BadRequest):
    """The specified usage limit is invalid."""
    ID = "USAGE_LIMIT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsernamesActiveTooMuch(BadRequest):
    """The maximum number of active usernames was reached."""
    ID = "USERNAMES_ACTIVE_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsernameInvalid(BadRequest):
    """The provided username is not valid."""
    ID = "USERNAME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsernameNotModified(BadRequest):
    """The username was not modified because you tried to edit it using the same one."""
    ID = "USERNAME_NOT_MODIFIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsernameNotOccupied(BadRequest):
    """The provided username is not occupied by anyone."""
    ID = "USERNAME_NOT_OCCUPIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsernameOccupied(BadRequest):
    """The provided username is already in use by someone else."""
    ID = "USERNAME_OCCUPIED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsernamePurchaseAvailable(BadRequest):
    """The specified username can be purchased on https://fragment.com."""
    ID = "USERNAME_PURCHASE_AVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsernameSuffixMissing(BadRequest):
    """Bot username must end in `bot`."""
    ID = "USERNAME_SUFFIX_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserpicUploadRequired(BadRequest):
    """You are required to upload a profile picture for this action."""
    ID = "USERPIC_UPLOAD_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsersTooFew(BadRequest):
    """Not enough users (to create a chat, for example)."""
    ID = "USERS_TOO_FEW"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UsersTooMuch(BadRequest):
    """The maximum number of users has been exceeded (to create a chat, for example)."""
    ID = "USERS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserAdminInvalid(BadRequest):
    """The action requires admin privileges. Probably you tried to edit admin privileges on someone you don't have rights to."""
    ID = "USER_ADMIN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserAlreadyInvited(BadRequest):
    """You have already invited this user."""
    ID = "USER_ALREADY_INVITED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserAlreadyParticipant(BadRequest):
    """The user is already a participant of this chat."""
    ID = "USER_ALREADY_PARTICIPANT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserBannedInChannel(BadRequest):
    """You're limited from sending messages in supergroups/channels, check @spambot for details."""
    ID = "USER_BANNED_IN_CHANNEL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserBlocked(BadRequest):
    """The user is blocked."""
    ID = "USER_BLOCKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserBot(BadRequest):
    """Bots in channels can only be administrators, not members."""
    ID = "USER_BOT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserBotInvalid(BadRequest):
    """User accounts must provide the `bot` method parameter when calling this method. If there is no such method parameter, this method can only be invoked by bot accounts."""
    ID = "USER_BOT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserBotRequired(BadRequest):
    """This method can only be called by a bot."""
    ID = "USER_BOT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserBotToBotDisabled(BadRequest):
    """Bot-to-bot messaging is disabled because one of the two bots hasn't enabled the Bot to Bot setting in @BotFather."""
    ID = "USER_BOT_TO_BOT_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserChannelsTooMuch(BadRequest):
    """One of the users you tried to add is already in too many channels/supergroups."""
    ID = "USER_CHANNELS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserCreator(BadRequest):
    """The user id being used is invalid or not known yet. Make sure you meet the user before interacting with it."""
    ID = "USER_CREATOR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserGiftUnavailable(BadRequest):
    """Gifts are not available in the current region ([stars_gifts_enabled](https://core.telegram.org/api/config#stars-gifts-enabled) is equal to false)."""
    ID = "USER_GIFT_UNAVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserHandleMismatch(BadRequest):
    """The user handle mismatch."""
    ID = "USER_HANDLE_MISMATCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserIdInvalid(BadRequest):
    """The provided user id is invalid."""
    ID = "USER_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserInvalid(BadRequest):
    """The provided user is invalid."""
    ID = "USER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserIsBlocked(BadRequest):
    """You were blocked by this user."""
    ID = "USER_IS_BLOCKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserIsBot(BadRequest):
    """A bot cannot send messages to other bots or to itself."""
    ID = "USER_IS_BOT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserKicked(BadRequest):
    """This user was kicked from this chat."""
    ID = "USER_KICKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserNotMutualContact(BadRequest):
    """The provided user is not a mutual contact."""
    ID = "USER_NOT_MUTUAL_CONTACT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserNotParticipant(BadRequest):
    """You're not a member of this chat."""
    ID = "USER_NOT_PARTICIPANT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserPublicMissing(BadRequest):
    """The accounts username is missing."""
    ID = "USER_PUBLIC_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserRightsMissing(BadRequest):
    """The user rights is missing."""
    ID = "USER_RIGHTS_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserVolumeInvalid(BadRequest):
    """The specified user volume is invalid."""
    ID = "USER_VOLUME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VenueIdInvalid(BadRequest):
    """The specified venue ID is invalid."""
    ID = "VENUE_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VideoContentTypeInvalid(BadRequest):
    """The video content type is invalid (i.e.: not streamable)."""
    ID = "VIDEO_CONTENT_TYPE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VideoDurationInvalid(BadRequest):
    """The duration of the specified video is invalid."""
    ID = "VIDEO_DURATION_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VideoFileInvalid(BadRequest):
    """The specified video file is invalid."""
    ID = "VIDEO_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VideoPauseForbidden(BadRequest):
    """You cannot pause the video stream."""
    ID = "VIDEO_PAUSE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VideoStopForbidden(BadRequest):
    """You cannot stop the video stream."""
    ID = "VIDEO_STOP_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VideoTitleEmpty(BadRequest):
    """The specified video title is empty."""
    ID = "VIDEO_TITLE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VoiceMessagesForbidden(BadRequest):
    """This user's privacy settings forbid you from sending voice messages."""
    ID = "VOICE_MESSAGES_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VolumeLocNotFound(BadRequest):
    """The volume location can't be found."""
    ID = "VOLUME_LOC_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WallpaperFileInvalid(BadRequest):
    """TThe provided file cannot be used as a wallpaper."""
    ID = "WALLPAPER_FILE_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WallpaperInvalid(BadRequest):
    """The specified wallpaper is invalid."""
    ID = "WALLPAPER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WallpaperMimeInvalid(BadRequest):
    """The specified wallpaper MIME type is invalid."""
    ID = "WALLPAPER_MIME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WallpaperNotFound(BadRequest):
    """The specified wallpaper could not be found."""
    ID = "WALLPAPER_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WcConvertUrlInvalid(BadRequest):
    """WC convert URL invalid."""
    ID = "WC_CONVERT_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebappReqIdInvalid(BadRequest):
    """The specified webapp_req_id is invalid."""
    ID = "WEBAPP_REQ_ID_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebauthTokenExpired(BadRequest):
    """The specified auth token has expired."""
    ID = "WEBAUTH_TOKEN_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebdocumentInvalid(BadRequest):
    """Invalid webdocument URL provided."""
    ID = "WEBDOCUMENT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebdocumentMimeInvalid(BadRequest):
    """Invalid webdocument mime type provided."""
    ID = "WEBDOCUMENT_MIME_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebdocumentSizeTooBig(BadRequest):
    """Webdocument is too big!."""
    ID = "WEBDOCUMENT_SIZE_TOO_BIG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebdocumentUrlEmpty(BadRequest):
    """The passed web document URL is empty."""
    ID = "WEBDOCUMENT_URL_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebdocumentUrlInvalid(BadRequest):
    """The specified webdocument URL is invalid."""
    ID = "WEBDOCUMENT_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebpageCurlFailed(BadRequest):
    """Telegram server could not fetch the provided URL."""
    ID = "WEBPAGE_CURL_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebpageMediaEmpty(BadRequest):
    """The URL doesn't contain any valid media."""
    ID = "WEBPAGE_MEDIA_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebpageNotFound(BadRequest):
    """A preview for the specified webpage `url` could not be generated."""
    ID = "WEBPAGE_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebpageUrlInvalid(BadRequest):
    """The specified webpage `url` is invalid."""
    ID = "WEBPAGE_URL_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebpushAuthInvalid(BadRequest):
    """The specified web push authentication secret is invalid."""
    ID = "WEBPUSH_AUTH_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebpushKeyInvalid(BadRequest):
    """The specified web push elliptic curve Diffie-Hellman public key is invalid."""
    ID = "WEBPUSH_KEY_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WebpushTokenInvalid(BadRequest):
    """The specified web push token is invalid."""
    ID = "WEBPUSH_TOKEN_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class YouBlockedUser(BadRequest):
    """You blocked this user."""
    ID = "YOU_BLOCKED_USER"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


