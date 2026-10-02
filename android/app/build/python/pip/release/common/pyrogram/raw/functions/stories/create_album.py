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


class CreateAlbum(TLObject["raw.base.StoryAlbum"]):
    """Telegram API function.

    Details:
        - Layer: ``228``
        - ID: ``A36396E5``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        title (``str``):
            N/A

        stories (List of ``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`StoryAlbum <pyrogram.raw.base.StoryAlbum>`
    """

    __slots__: List[str] = ["peer", "title", "stories"]

    ID = 0xa36396e5
    QUALNAME = "functions.stories.CreateAlbum"

    def __init__(self, *, peer: "raw.base.InputPeer", title: str, stories: List[int]) -> None:
        self.peer = peer  # InputPeer
        self.title = title  # string
        self.stories = stories  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CreateAlbum":
        # No flags
        
        peer = TLObject.read(b)
        
        title = String.read(b)
        
        stories = TLObject.read(b, Int)
        
        return CreateAlbum(peer=peer, title=title, stories=stories)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(String(self.title))
        
        b.write(Vector(self.stories, Int))
        
        return b.getvalue()
