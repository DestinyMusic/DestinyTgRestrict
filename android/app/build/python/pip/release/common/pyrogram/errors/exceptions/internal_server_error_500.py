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
    CallOccupyFailed,
    ChatInvalid,
    MsgWaitFailed,
    RandomIdDuplicate,
    VolumeLocNotFound,
)


class InternalServerError(RPCError):
    """Internal Server Error"""
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = __doc__


class ApiCallError(InternalServerError):
    """API call error due to Telegram having internal problems. Please try again later."""
    ID = "API_CALL_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthKeyUnsynchronized(InternalServerError):
    """Internal error, please repeat the method call."""
    ID = "AUTH_KEY_UNSYNCHRONIZED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthRestart(InternalServerError):
    """User authorization has restarted."""
    ID = "AUTH_RESTART"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthRestartX(AuthRestart):
    """Internal error (debug info {debug_info}), please repeat the method call."""
    ID = "AUTH_RESTART_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "debug_info"
    """``str``: Name of the property that holds this error's value"""

    @property
    def debug_info(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class CallOccupyFailed500(CallOccupyFailed, InternalServerError):
    """The call failed because the user is already making another call."""
    ID = "CALL_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = "Internal Server Error"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class CdnUploadTimeout(InternalServerError):
    """A server-side timeout occurred while reuploading the file to the CDN DC."""
    ID = "CDN_UPLOAD_TIMEOUT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatIdGenerateFailed(InternalServerError):
    """Failure while generating the chat ID."""
    ID = "CHAT_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatInvalid500(ChatInvalid, InternalServerError):
    """Invalid chat."""
    ID = "CHAT_INVALID"
    """``str``: RPC Error ID"""
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = "Internal Server Error"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class ChatOccupyLocFailed(InternalServerError):
    """An internal error occurred while creating the chat."""
    ID = "CHAT_OCCUPY_LOC_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatOccupyUsernameFailed(InternalServerError):
    """Failure to occupy chat username due to Telegram having internal problems. Please try again later."""
    ID = "CHAT_OCCUPY_USERNAME_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChpBadEvent(InternalServerError):
    """Bad event."""
    ID = "CHP_BAD_EVENT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChpCallFail(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "CHP_CALL_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionOccupyAdminFailed(InternalServerError):
    """Failed occupying memory for admin info due to Telegram having internal problems. Please try again later."""
    ID = "ENCRYPTION_OCCUPY_ADMIN_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionOccupyFailed(InternalServerError):
    """Internal server error while accepting secret chat."""
    ID = "ENCRYPTION_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FileWriteFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "FILE_WRITE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FolderDeacAutofixAll(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "FOLDER_DEAC_AUTOFIX_ALL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallAddParticipantsFailed(InternalServerError):
    """Failure while adding voice chat member due to Telegram having internal problems. Please try again later."""
    ID = "GROUPCALL_ADD_PARTICIPANTS_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupedIdOccupyFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "GROUPED_ID_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class HistoryGetFailed(InternalServerError):
    """The chat history couldn't be retrieved due to Telegram having internal problems. Please try again later."""
    ID = "HISTORY_GET_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImageEngineDown(InternalServerError):
    """Image engine down due to Telegram having internal problems. Please try again later."""
    ID = "IMAGE_ENGINE_DOWN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InterdcCallError(InternalServerError):
    """An error occurred while Telegram was intercommunicating with DC{dc_id}. Please try again later."""
    ID = "INTERDC_X_CALL_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "dc_id"
    """``str``: Name of the property that holds this error's value"""

    @property
    def dc_id(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class InterdcCallRichError(InternalServerError):
    """A rich error occurred while Telegram was intercommunicating with DC{dc_id}. Please try again later."""
    ID = "INTERDC_X_CALL_RICH_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "dc_id"
    """``str``: Name of the property that holds this error's value"""

    @property
    def dc_id(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class MemberFetchFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "MEMBER_FETCH_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MemberNoLocation(InternalServerError):
    """Couldn't find the member's location due to Telegram having internal problems. Please try again later."""
    ID = "MEMBER_NO_LOCATION"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MemberOccupyPrimaryLocFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "MEMBER_OCCUPY_PRIMARY_LOC_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MemberOccupyUsernameFailed(InternalServerError):
    """Failure to occupy member username due to Telegram having internal problems. Please try again later."""
    ID = "MEMBER_OCCUPY_USERNAME_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgidDecreaseRetry(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "MSGID_DECREASE_RETRY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgRangeUnsync(InternalServerError):
    """Message range unsynchronized due to Telegram having internal problems. Please try again later."""
    ID = "MSG_RANGE_UNSYNC"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgWaitFailed500(MsgWaitFailed, InternalServerError):
    """A waiting call returned an error."""
    ID = "MSG_WAIT_FAILED"
    """``str``: RPC Error ID"""
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = "Internal Server Error"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class MtSendQueueTooLong(InternalServerError):
    """The MTProto send queue has grown too much due to Telegram having internal problems. Please try again later."""
    ID = "MT_SEND_QUEUE_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NeedChatInvalid(InternalServerError):
    """The provided chat is invalid."""
    ID = "NEED_CHAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NeedMemberInvalid(InternalServerError):
    """The provided member is invalid or does not exist."""
    ID = "NEED_MEMBER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NoWorkersRunning(InternalServerError):
    """The Telegram server is restarting its workers. Try again later."""
    ID = "No workers running"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ParticipantCallFailed(InternalServerError):
    """Failure while making call due to Telegram having internal problems. Please try again later."""
    ID = "PARTICIPANT_CALL_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PersistentTimestampOutdated(InternalServerError):
    """The persistent timestamp is outdated due to Telegram having internal problems. Please try again later (treat this like an RPC_CALL_FAIL)."""
    ID = "PERSISTENT_TIMESTAMP_OUTDATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoCreateFailed(InternalServerError):
    """The creation of the photo failed due to Telegram having internal problems. Please try again later."""
    ID = "PHOTO_CREATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PostponedTimeout(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "POSTPONED_TIMEOUT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PtsChangeEmpty(InternalServerError):
    """No PTS change."""
    ID = "PTS_CHANGE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RandomIdDuplicate500(RandomIdDuplicate, InternalServerError):
    """You provided a random ID that was already used."""
    ID = "RANDOM_ID_DUPLICATE"
    """``str``: RPC Error ID"""
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = "Internal Server Error"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class RegIdGenerateFailed(InternalServerError):
    """The registration id failed to generate due to Telegram having internal problems. Please try again later."""
    ID = "REG_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RpcCallFail(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "RPC_CALL_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RpcConnectFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "RPC_CONNECT_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RpcMcgetFail(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "RPC_MCGET_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RpcSendFail(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "RPC_SEND_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SendMediaInvalid(InternalServerError):
    """The specified media is invalid."""
    ID = "SEND_MEDIA_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SignInFailed(InternalServerError):
    """Failure while signing in due to Telegram having internal problems. Please try again later."""
    ID = "SIGN_IN_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StorageCheckFailed(InternalServerError):
    """Server storage check failed due to Telegram having internal problems. Please try again later."""
    ID = "STORAGE_CHECK_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StorageChooseVolumeFailed(InternalServerError):
    """Storage choose volume failed due to Telegram having internal problems. Please try again later."""
    ID = "STORAGE_CHOOSE_VOLUME_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoreInvalidScalarType(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "STORE_INVALID_SCALAR_TYPE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class Timeout(InternalServerError):
    """A timeout occurred while fetching data from the worker."""
    ID = "TIMEOUT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class TranslateReqFailed(InternalServerError):
    """Translation failed, please try again later."""
    ID = "TRANSLATE_REQ_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UnknownMethod(InternalServerError):
    """The method you tried to call cannot be called on non-CDN DCs."""
    ID = "UNKNOWN_METHOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UploadNoVolume(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "UPLOAD_NO_VOLUME"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VolumeLocNotFound500(VolumeLocNotFound, InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "VOLUME_LOC_NOT_FOUND"
    """``str``: RPC Error ID"""
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = "Internal Server Error"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class WorkerBusyTooLongRetry(InternalServerError):
    """Server workers are too busy right now due to Telegram having internal problems. Please try again later."""
    ID = "WORKER_BUSY_TOO_LONG_RETRY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WpIdGenerateFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later."""
    ID = "WP_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


