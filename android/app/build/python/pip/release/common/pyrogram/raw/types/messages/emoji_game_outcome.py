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


class EmojiGameOutcome(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.messages.EmojiGameOutcome`.

    Details:
        - Layer: ``228``
        - ID: ``DA2AD647``

    Parameters:
        seed (``bytes``):
            N/A

        stake_ton_amount (``int`` ``64-bit``):
            N/A

        ton_amount (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["seed", "stake_ton_amount", "ton_amount"]

    ID = 0xda2ad647
    QUALNAME = "types.messages.EmojiGameOutcome"

    def __init__(self, *, seed: bytes, stake_ton_amount: int, ton_amount: int) -> None:
        self.seed = seed  # bytes
        self.stake_ton_amount = stake_ton_amount  # long
        self.ton_amount = ton_amount  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiGameOutcome":
        # No flags
        
        seed = Bytes.read(b)
        
        stake_ton_amount = Long.read(b)
        
        ton_amount = Long.read(b)
        
        return EmojiGameOutcome(seed=seed, stake_ton_amount=stake_ton_amount, ton_amount=ton_amount)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.seed))
        
        b.write(Long(self.stake_ton_amount))
        
        b.write(Long(self.ton_amount))
        
        return b.getvalue()
