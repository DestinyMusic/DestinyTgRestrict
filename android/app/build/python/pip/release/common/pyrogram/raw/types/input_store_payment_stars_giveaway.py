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


class InputStorePaymentStarsGiveaway(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.InputStorePaymentPurpose`.

    Details:
        - Layer: ``228``
        - ID: ``751F08FA``

    Parameters:
        stars (``int`` ``64-bit``):
            N/A

        boost_peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

        until_date (``int`` ``32-bit``):
            N/A

        currency (``str``):
            N/A

        amount (``int`` ``64-bit``):
            N/A

        users (``int`` ``32-bit``):
            N/A

        only_new_subscribers (``bool``, *optional*):
            N/A

        winners_are_visible (``bool``, *optional*):
            N/A

        additional_peers (List of :obj:`InputPeer <pyrogram.raw.base.InputPeer>`, *optional*):
            N/A

        countries_iso2 (List of ``str``, *optional*):
            N/A

        prize_description (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["stars", "boost_peer", "random_id", "until_date", "currency", "amount", "users", "only_new_subscribers", "winners_are_visible", "additional_peers", "countries_iso2", "prize_description"]

    ID = 0x751f08fa
    QUALNAME = "types.InputStorePaymentStarsGiveaway"

    def __init__(self, *, stars: int, boost_peer: "raw.base.InputPeer", random_id: int, until_date: int, currency: str, amount: int, users: int, only_new_subscribers: Optional[bool] = None, winners_are_visible: Optional[bool] = None, additional_peers: Optional[List["raw.base.InputPeer"]] = None, countries_iso2: Optional[List[str]] = None, prize_description: Optional[str] = None) -> None:
        self.stars = stars  # long
        self.boost_peer = boost_peer  # InputPeer
        self.random_id = random_id  # long
        self.until_date = until_date  # int
        self.currency = currency  # string
        self.amount = amount  # long
        self.users = users  # int
        self.only_new_subscribers = only_new_subscribers  # flags.0?true
        self.winners_are_visible = winners_are_visible  # flags.3?true
        self.additional_peers = additional_peers  # flags.1?Vector<InputPeer>
        self.countries_iso2 = countries_iso2  # flags.2?Vector<string>
        self.prize_description = prize_description  # flags.4?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputStorePaymentStarsGiveaway":
        
        flags = Int.read(b)
        
        only_new_subscribers = True if flags & (1 << 0) else False
        winners_are_visible = True if flags & (1 << 3) else False
        stars = Long.read(b)
        
        boost_peer = TLObject.read(b)
        
        additional_peers = TLObject.read(b) if flags & (1 << 1) else []
        
        countries_iso2 = TLObject.read(b, String) if flags & (1 << 2) else []
        
        prize_description = String.read(b) if flags & (1 << 4) else None
        random_id = Long.read(b)
        
        until_date = Int.read(b)
        
        currency = String.read(b)
        
        amount = Long.read(b)
        
        users = Int.read(b)
        
        return InputStorePaymentStarsGiveaway(stars=stars, boost_peer=boost_peer, random_id=random_id, until_date=until_date, currency=currency, amount=amount, users=users, only_new_subscribers=only_new_subscribers, winners_are_visible=winners_are_visible, additional_peers=additional_peers, countries_iso2=countries_iso2, prize_description=prize_description)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.only_new_subscribers else 0
        flags |= (1 << 3) if self.winners_are_visible else 0
        flags |= (1 << 1) if self.additional_peers else 0
        flags |= (1 << 2) if self.countries_iso2 else 0
        flags |= (1 << 4) if self.prize_description is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.stars))
        
        b.write(self.boost_peer.write())
        
        if self.additional_peers:
            b.write(Vector(self.additional_peers))
        
        if self.countries_iso2:
            b.write(Vector(self.countries_iso2, String))
        
        if self.prize_description is not None:
            b.write(String(self.prize_description))
        
        b.write(Long(self.random_id))
        
        b.write(Int(self.until_date))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        b.write(Int(self.users))
        
        return b.getvalue()
