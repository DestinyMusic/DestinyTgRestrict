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


class GlobalPrivacySettings(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.GlobalPrivacySettings`.

    Details:
        - Layer: ``228``
        - ID: ``FE41B34F``

    Parameters:
        archive_and_mute_new_noncontact_peers (``bool``, *optional*):
            N/A

        keep_archived_unmuted (``bool``, *optional*):
            N/A

        keep_archived_folders (``bool``, *optional*):
            N/A

        hide_read_marks (``bool``, *optional*):
            N/A

        new_noncontact_peers_require_premium (``bool``, *optional*):
            N/A

        display_gifts_button (``bool``, *optional*):
            N/A

        noncontact_peers_paid_stars (``int`` ``64-bit``, *optional*):
            N/A

        disallowed_gifts (:obj:`DisallowedGiftsSettings <pyrogram.raw.base.DisallowedGiftsSettings>`, *optional*):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetGlobalPrivacySettings
            account.SetGlobalPrivacySettings
    """

    __slots__: List[str] = ["archive_and_mute_new_noncontact_peers", "keep_archived_unmuted", "keep_archived_folders", "hide_read_marks", "new_noncontact_peers_require_premium", "display_gifts_button", "noncontact_peers_paid_stars", "disallowed_gifts"]

    ID = 0xfe41b34f
    QUALNAME = "types.GlobalPrivacySettings"

    def __init__(self, *, archive_and_mute_new_noncontact_peers: Optional[bool] = None, keep_archived_unmuted: Optional[bool] = None, keep_archived_folders: Optional[bool] = None, hide_read_marks: Optional[bool] = None, new_noncontact_peers_require_premium: Optional[bool] = None, display_gifts_button: Optional[bool] = None, noncontact_peers_paid_stars: Optional[int] = None, disallowed_gifts: "raw.base.DisallowedGiftsSettings" = None) -> None:
        self.archive_and_mute_new_noncontact_peers = archive_and_mute_new_noncontact_peers  # flags.0?true
        self.keep_archived_unmuted = keep_archived_unmuted  # flags.1?true
        self.keep_archived_folders = keep_archived_folders  # flags.2?true
        self.hide_read_marks = hide_read_marks  # flags.3?true
        self.new_noncontact_peers_require_premium = new_noncontact_peers_require_premium  # flags.4?true
        self.display_gifts_button = display_gifts_button  # flags.7?true
        self.noncontact_peers_paid_stars = noncontact_peers_paid_stars  # flags.5?long
        self.disallowed_gifts = disallowed_gifts  # flags.6?DisallowedGiftsSettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GlobalPrivacySettings":
        
        flags = Int.read(b)
        
        archive_and_mute_new_noncontact_peers = True if flags & (1 << 0) else False
        keep_archived_unmuted = True if flags & (1 << 1) else False
        keep_archived_folders = True if flags & (1 << 2) else False
        hide_read_marks = True if flags & (1 << 3) else False
        new_noncontact_peers_require_premium = True if flags & (1 << 4) else False
        display_gifts_button = True if flags & (1 << 7) else False
        noncontact_peers_paid_stars = Long.read(b) if flags & (1 << 5) else None
        disallowed_gifts = TLObject.read(b) if flags & (1 << 6) else None
        
        return GlobalPrivacySettings(archive_and_mute_new_noncontact_peers=archive_and_mute_new_noncontact_peers, keep_archived_unmuted=keep_archived_unmuted, keep_archived_folders=keep_archived_folders, hide_read_marks=hide_read_marks, new_noncontact_peers_require_premium=new_noncontact_peers_require_premium, display_gifts_button=display_gifts_button, noncontact_peers_paid_stars=noncontact_peers_paid_stars, disallowed_gifts=disallowed_gifts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.archive_and_mute_new_noncontact_peers else 0
        flags |= (1 << 1) if self.keep_archived_unmuted else 0
        flags |= (1 << 2) if self.keep_archived_folders else 0
        flags |= (1 << 3) if self.hide_read_marks else 0
        flags |= (1 << 4) if self.new_noncontact_peers_require_premium else 0
        flags |= (1 << 7) if self.display_gifts_button else 0
        flags |= (1 << 5) if self.noncontact_peers_paid_stars is not None else 0
        flags |= (1 << 6) if self.disallowed_gifts is not None else 0
        b.write(Int(flags))
        
        if self.noncontact_peers_paid_stars is not None:
            b.write(Long(self.noncontact_peers_paid_stars))
        
        if self.disallowed_gifts is not None:
            b.write(self.disallowed_gifts.write())
        
        return b.getvalue()
