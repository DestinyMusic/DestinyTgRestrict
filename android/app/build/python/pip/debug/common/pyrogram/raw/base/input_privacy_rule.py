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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import TYPE_CHECKING, Union

from pyrogram import raw
from pyrogram.raw.core import BaseTypeMeta


if TYPE_CHECKING:
    InputPrivacyRule = Union[raw.types.InputPrivacyValueAllowAll, raw.types.InputPrivacyValueAllowBots, raw.types.InputPrivacyValueAllowChatParticipants, raw.types.InputPrivacyValueAllowCloseFriends, raw.types.InputPrivacyValueAllowContacts, raw.types.InputPrivacyValueAllowPremium, raw.types.InputPrivacyValueAllowUsers, raw.types.InputPrivacyValueDisallowAll, raw.types.InputPrivacyValueDisallowBots, raw.types.InputPrivacyValueDisallowChatParticipants, raw.types.InputPrivacyValueDisallowContacts, raw.types.InputPrivacyValueDisallowUsers]
else:
    # noinspection PyRedeclaration
    class InputPrivacyRule(metaclass=BaseTypeMeta):  # type: ignore
        """Telegram API base type.

    Constructors:
        This base type has 12 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            InputPrivacyValueAllowAll
            InputPrivacyValueAllowBots
            InputPrivacyValueAllowChatParticipants
            InputPrivacyValueAllowCloseFriends
            InputPrivacyValueAllowContacts
            InputPrivacyValueAllowPremium
            InputPrivacyValueAllowUsers
            InputPrivacyValueDisallowAll
            InputPrivacyValueDisallowBots
            InputPrivacyValueDisallowChatParticipants
            InputPrivacyValueDisallowContacts
            InputPrivacyValueDisallowUsers
        """

        QUALNAME = "pyrogram.raw.base.InputPrivacyRule"
        __union_types__ = Union[raw.types.InputPrivacyValueAllowAll, raw.types.InputPrivacyValueAllowBots, raw.types.InputPrivacyValueAllowChatParticipants, raw.types.InputPrivacyValueAllowCloseFriends, raw.types.InputPrivacyValueAllowContacts, raw.types.InputPrivacyValueAllowPremium, raw.types.InputPrivacyValueAllowUsers, raw.types.InputPrivacyValueDisallowAll, raw.types.InputPrivacyValueDisallowBots, raw.types.InputPrivacyValueDisallowChatParticipants, raw.types.InputPrivacyValueDisallowContacts, raw.types.InputPrivacyValueDisallowUsers]

        def __init__(self):
            raise TypeError("Base types can only be used for type checking purposes: "
                            "you tried to use a base type instance as argument, "
                            "but you need to instantiate one of its constructors instead. "
                            "More info: https://docs.kurigram.icu/telegram/base/input-privacy-rule")
