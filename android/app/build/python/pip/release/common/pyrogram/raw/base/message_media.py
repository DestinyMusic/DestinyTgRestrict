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
    MessageMedia = Union[raw.types.MessageMediaContact, raw.types.MessageMediaDice, raw.types.MessageMediaDocument, raw.types.MessageMediaEmpty, raw.types.MessageMediaGame, raw.types.MessageMediaGeo, raw.types.MessageMediaGeoLive, raw.types.MessageMediaGiveaway, raw.types.MessageMediaGiveawayResults, raw.types.MessageMediaInvoice, raw.types.MessageMediaPaidMedia, raw.types.MessageMediaPhoto, raw.types.MessageMediaPoll, raw.types.MessageMediaStory, raw.types.MessageMediaToDo, raw.types.MessageMediaUnsupported, raw.types.MessageMediaVenue, raw.types.MessageMediaVideoStream, raw.types.MessageMediaWebPage]
else:
    # noinspection PyRedeclaration
    class MessageMedia(metaclass=BaseTypeMeta):  # type: ignore
        """Telegram API base type.

    Constructors:
        This base type has 19 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            MessageMediaContact
            MessageMediaDice
            MessageMediaDocument
            MessageMediaEmpty
            MessageMediaGame
            MessageMediaGeo
            MessageMediaGeoLive
            MessageMediaGiveaway
            MessageMediaGiveawayResults
            MessageMediaInvoice
            MessageMediaPaidMedia
            MessageMediaPhoto
            MessageMediaPoll
            MessageMediaStory
            MessageMediaToDo
            MessageMediaUnsupported
            MessageMediaVenue
            MessageMediaVideoStream
            MessageMediaWebPage

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.UploadMedia
            messages.UploadImportedMedia
        """

        QUALNAME = "pyrogram.raw.base.MessageMedia"
        __union_types__ = Union[raw.types.MessageMediaContact, raw.types.MessageMediaDice, raw.types.MessageMediaDocument, raw.types.MessageMediaEmpty, raw.types.MessageMediaGame, raw.types.MessageMediaGeo, raw.types.MessageMediaGeoLive, raw.types.MessageMediaGiveaway, raw.types.MessageMediaGiveawayResults, raw.types.MessageMediaInvoice, raw.types.MessageMediaPaidMedia, raw.types.MessageMediaPhoto, raw.types.MessageMediaPoll, raw.types.MessageMediaStory, raw.types.MessageMediaToDo, raw.types.MessageMediaUnsupported, raw.types.MessageMediaVenue, raw.types.MessageMediaVideoStream, raw.types.MessageMediaWebPage]

        def __init__(self):
            raise TypeError("Base types can only be used for type checking purposes: "
                            "you tried to use a base type instance as argument, "
                            "but you need to instantiate one of its constructors instead. "
                            "More info: https://docs.kurigram.icu/telegram/base/message-media")
