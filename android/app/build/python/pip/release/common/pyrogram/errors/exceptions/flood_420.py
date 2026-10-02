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
    AddressInvalid,
)


class Flood(RPCError):
    """Flood"""
    CODE = 420
    """``int``: RPC Error Code"""
    NAME = __doc__


class TwoFaConfirmWait(Flood):
    """A wait of {seconds} seconds is required because this account is active and protected by a 2FA password."""
    ID = "2FA_CONFIRM_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class AddressInvalid420(AddressInvalid, Flood):
    """The specified geopoint address is invalid."""
    ID = "ADDRESS_INVALID"
    """``str``: RPC Error ID"""
    CODE = 420
    """``int``: RPC Error Code"""
    NAME = "Flood"
    """``str``: RPC Error Name"""
    MESSAGE = __doc__


class FloodPremiumWait(Flood):
    """Please wait {seconds} seconds before repeating the action, or purchase a [Telegram Premium subscription](https://core.telegram.org/api/premium) to remove this rate limit."""
    ID = "FLOOD_PREMIUM_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FloodTestPhoneWait(Flood):
    """A wait of {seconds} seconds is required in the test servers."""
    ID = "FLOOD_TEST_PHONE_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FloodWait(Flood):
    """Please wait {seconds} seconds before repeating the action."""
    ID = "FLOOD_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class FrozenMethodInvalid(Flood):
    """The method can't be used by frozen account. You can appeal via @SpamBot if you believe this was a mistake."""
    ID = "FROZEN_METHOD_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PremiumSubActiveUntil(Flood):
    """You already have a premium subscription active until unixtime {until_date}."""
    ID = "PREMIUM_SUB_ACTIVE_UNTIL_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "until_date"
    """``str``: Name of the property that holds this error's value"""

    @property
    def until_date(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class SlowmodeWait(Flood):
    """Slowmode is enabled in this chat: wait {seconds} seconds before sending another message to this chat."""
    ID = "SLOWMODE_WAIT_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class StorySendFlood(Flood):
    """A wait of {seconds} seconds is required to continue posting stories."""
    ID = "STORY_SEND_FLOOD_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


class TakeoutInitDelay(Flood):
    """Sorry, for security reasons, you will be able to begin downloading your data in {seconds} seconds. We have notified all your devices about the export request to make sure it's authorized and to give you time to react if it's not."""
    ID = "TAKEOUT_INIT_DELAY_X"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__

    VALUE_NAME = "seconds"
    """``str``: Name of the property that holds this error's value"""

    @property
    def seconds(self) -> Optional[int]:
        """``Optional[int]``: What Telegram sent with this error, under the name its message gives it"""
        return self.value


