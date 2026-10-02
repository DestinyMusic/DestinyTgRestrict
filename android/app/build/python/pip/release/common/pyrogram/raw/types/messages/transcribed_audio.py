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


class TranscribedAudio(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.messages.TranscribedAudio`.

    Details:
        - Layer: ``228``
        - ID: ``CFB9D957``

    Parameters:
        transcription_id (``int`` ``64-bit``):
            N/A

        text (``str``):
            N/A

        pending (``bool``, *optional*):
            N/A

        trial_remains_num (``int`` ``32-bit``, *optional*):
            N/A

        trial_remains_until_date (``int`` ``32-bit``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.TranscribeAudio
    """

    __slots__: List[str] = ["transcription_id", "text", "pending", "trial_remains_num", "trial_remains_until_date"]

    ID = 0xcfb9d957
    QUALNAME = "types.messages.TranscribedAudio"

    def __init__(self, *, transcription_id: int, text: str, pending: Optional[bool] = None, trial_remains_num: Optional[int] = None, trial_remains_until_date: Optional[int] = None) -> None:
        self.transcription_id = transcription_id  # long
        self.text = text  # string
        self.pending = pending  # flags.0?true
        self.trial_remains_num = trial_remains_num  # flags.1?int
        self.trial_remains_until_date = trial_remains_until_date  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TranscribedAudio":
        
        flags = Int.read(b)
        
        pending = True if flags & (1 << 0) else False
        transcription_id = Long.read(b)
        
        text = String.read(b)
        
        trial_remains_num = Int.read(b) if flags & (1 << 1) else None
        trial_remains_until_date = Int.read(b) if flags & (1 << 1) else None
        return TranscribedAudio(transcription_id=transcription_id, text=text, pending=pending, trial_remains_num=trial_remains_num, trial_remains_until_date=trial_remains_until_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.pending else 0
        flags |= (1 << 1) if self.trial_remains_num is not None else 0
        flags |= (1 << 1) if self.trial_remains_until_date is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.transcription_id))
        
        b.write(String(self.text))
        
        if self.trial_remains_num is not None:
            b.write(Int(self.trial_remains_num))
        
        if self.trial_remains_until_date is not None:
            b.write(Int(self.trial_remains_until_date))
        
        return b.getvalue()
