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


class FactCheck(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.FactCheck`.

    Details:
        - Layer: ``228``
        - ID: ``B89BFCCF``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        need_check (``bool``, *optional*):
            N/A

        country (``str``, *optional*):
            N/A

        text (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetFactCheck
    """

    __slots__: List[str] = ["hash", "need_check", "country", "text"]

    ID = 0xb89bfccf
    QUALNAME = "types.FactCheck"

    def __init__(self, *, hash: int, need_check: Optional[bool] = None, country: Optional[str] = None, text: "raw.base.TextWithEntities" = None) -> None:
        self.hash = hash  # long
        self.need_check = need_check  # flags.0?true
        self.country = country  # flags.1?string
        self.text = text  # flags.1?TextWithEntities

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "FactCheck":
        
        flags = Int.read(b)
        
        need_check = True if flags & (1 << 0) else False
        country = String.read(b) if flags & (1 << 1) else None
        text = TLObject.read(b) if flags & (1 << 1) else None
        
        hash = Long.read(b)
        
        return FactCheck(hash=hash, need_check=need_check, country=country, text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.need_check else 0
        flags |= (1 << 1) if self.country is not None else 0
        flags |= (1 << 1) if self.text is not None else 0
        b.write(Int(flags))
        
        if self.country is not None:
            b.write(String(self.country))
        
        if self.text is not None:
            b.write(self.text.write())
        
        b.write(Long(self.hash))
        
        return b.getvalue()
