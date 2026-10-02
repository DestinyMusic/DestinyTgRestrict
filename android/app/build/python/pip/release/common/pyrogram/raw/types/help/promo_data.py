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


class PromoData(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.help.PromoData`.

    Details:
        - Layer: ``228``
        - ID: ``8A4D87A``

    Parameters:
        expires (``int`` ``32-bit``):
            N/A

        pending_suggestions (List of ``str``):
            N/A

        dismissed_suggestions (List of ``str``):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

        proxy (``bool``, *optional*):
            N/A

        peer (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        psa_type (``str``, *optional*):
            N/A

        psa_message (``str``, *optional*):
            N/A

        custom_pending_suggestion (:obj:`PendingSuggestion <pyrogram.raw.base.PendingSuggestion>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetPromoData
    """

    __slots__: List[str] = ["expires", "pending_suggestions", "dismissed_suggestions", "chats", "users", "proxy", "peer", "psa_type", "psa_message", "custom_pending_suggestion"]

    ID = 0x8a4d87a
    QUALNAME = "types.help.PromoData"

    def __init__(self, *, expires: int, pending_suggestions: List[str], dismissed_suggestions: List[str], chats: List["raw.base.Chat"], users: List["raw.base.User"], proxy: Optional[bool] = None, peer: "raw.base.Peer" = None, psa_type: Optional[str] = None, psa_message: Optional[str] = None, custom_pending_suggestion: "raw.base.PendingSuggestion" = None) -> None:
        self.expires = expires  # int
        self.pending_suggestions = pending_suggestions  # Vector<string>
        self.dismissed_suggestions = dismissed_suggestions  # Vector<string>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.proxy = proxy  # flags.0?true
        self.peer = peer  # flags.3?Peer
        self.psa_type = psa_type  # flags.1?string
        self.psa_message = psa_message  # flags.2?string
        self.custom_pending_suggestion = custom_pending_suggestion  # flags.4?PendingSuggestion

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PromoData":
        
        flags = Int.read(b)
        
        proxy = True if flags & (1 << 0) else False
        expires = Int.read(b)
        
        peer = TLObject.read(b) if flags & (1 << 3) else None
        
        psa_type = String.read(b) if flags & (1 << 1) else None
        psa_message = String.read(b) if flags & (1 << 2) else None
        pending_suggestions = TLObject.read(b, String)
        
        dismissed_suggestions = TLObject.read(b, String)
        
        custom_pending_suggestion = TLObject.read(b) if flags & (1 << 4) else None
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return PromoData(expires=expires, pending_suggestions=pending_suggestions, dismissed_suggestions=dismissed_suggestions, chats=chats, users=users, proxy=proxy, peer=peer, psa_type=psa_type, psa_message=psa_message, custom_pending_suggestion=custom_pending_suggestion)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.proxy else 0
        flags |= (1 << 3) if self.peer is not None else 0
        flags |= (1 << 1) if self.psa_type is not None else 0
        flags |= (1 << 2) if self.psa_message is not None else 0
        flags |= (1 << 4) if self.custom_pending_suggestion is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.expires))
        
        if self.peer is not None:
            b.write(self.peer.write())
        
        if self.psa_type is not None:
            b.write(String(self.psa_type))
        
        if self.psa_message is not None:
            b.write(String(self.psa_message))
        
        b.write(Vector(self.pending_suggestions, String))
        
        b.write(Vector(self.dismissed_suggestions, String))
        
        if self.custom_pending_suggestion is not None:
            b.write(self.custom_pending_suggestion.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
