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


class Poll(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Poll`.

    Details:
        - Layer: ``228``
        - ID: ``966E2DBF``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        question (:obj:`TextWithEntities <pyrogram.raw.base.TextWithEntities>`):
            N/A

        answers (List of :obj:`PollAnswer <pyrogram.raw.base.PollAnswer>`):
            N/A

        hash (``int`` ``64-bit``):
            N/A

        closed (``bool``, *optional*):
            N/A

        public_voters (``bool``, *optional*):
            N/A

        multiple_choice (``bool``, *optional*):
            N/A

        quiz (``bool``, *optional*):
            N/A

        open_answers (``bool``, *optional*):
            N/A

        revoting_disabled (``bool``, *optional*):
            N/A

        shuffle_answers (``bool``, *optional*):
            N/A

        hide_results_until_close (``bool``, *optional*):
            N/A

        creator (``bool``, *optional*):
            N/A

        subscribers_only (``bool``, *optional*):
            N/A

        close_period (``int`` ``32-bit``, *optional*):
            N/A

        close_date (``int`` ``32-bit``, *optional*):
            N/A

        countries_iso2 (List of ``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "question", "answers", "hash", "closed", "public_voters", "multiple_choice", "quiz", "open_answers", "revoting_disabled", "shuffle_answers", "hide_results_until_close", "creator", "subscribers_only", "close_period", "close_date", "countries_iso2"]

    ID = 0x966e2dbf
    QUALNAME = "types.Poll"

    def __init__(self, *, id: int, question: "raw.base.TextWithEntities", answers: List["raw.base.PollAnswer"], hash: int, closed: Optional[bool] = None, public_voters: Optional[bool] = None, multiple_choice: Optional[bool] = None, quiz: Optional[bool] = None, open_answers: Optional[bool] = None, revoting_disabled: Optional[bool] = None, shuffle_answers: Optional[bool] = None, hide_results_until_close: Optional[bool] = None, creator: Optional[bool] = None, subscribers_only: Optional[bool] = None, close_period: Optional[int] = None, close_date: Optional[int] = None, countries_iso2: Optional[List[str]] = None) -> None:
        self.id = id  # long
        self.question = question  # TextWithEntities
        self.answers = answers  # Vector<PollAnswer>
        self.hash = hash  # long
        self.closed = closed  # flags.0?true
        self.public_voters = public_voters  # flags.1?true
        self.multiple_choice = multiple_choice  # flags.2?true
        self.quiz = quiz  # flags.3?true
        self.open_answers = open_answers  # flags.6?true
        self.revoting_disabled = revoting_disabled  # flags.7?true
        self.shuffle_answers = shuffle_answers  # flags.8?true
        self.hide_results_until_close = hide_results_until_close  # flags.9?true
        self.creator = creator  # flags.10?true
        self.subscribers_only = subscribers_only  # flags.11?true
        self.close_period = close_period  # flags.4?int
        self.close_date = close_date  # flags.5?int
        self.countries_iso2 = countries_iso2  # flags.12?Vector<string>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Poll":
        
        id = Long.read(b)
        
        flags = Int.read(b)
        
        closed = True if flags & (1 << 0) else False
        public_voters = True if flags & (1 << 1) else False
        multiple_choice = True if flags & (1 << 2) else False
        quiz = True if flags & (1 << 3) else False
        open_answers = True if flags & (1 << 6) else False
        revoting_disabled = True if flags & (1 << 7) else False
        shuffle_answers = True if flags & (1 << 8) else False
        hide_results_until_close = True if flags & (1 << 9) else False
        creator = True if flags & (1 << 10) else False
        subscribers_only = True if flags & (1 << 11) else False
        question = TLObject.read(b)
        
        answers = TLObject.read(b)
        
        close_period = Int.read(b) if flags & (1 << 4) else None
        close_date = Int.read(b) if flags & (1 << 5) else None
        countries_iso2 = TLObject.read(b, String) if flags & (1 << 12) else []
        
        hash = Long.read(b)
        
        return Poll(id=id, question=question, answers=answers, hash=hash, closed=closed, public_voters=public_voters, multiple_choice=multiple_choice, quiz=quiz, open_answers=open_answers, revoting_disabled=revoting_disabled, shuffle_answers=shuffle_answers, hide_results_until_close=hide_results_until_close, creator=creator, subscribers_only=subscribers_only, close_period=close_period, close_date=close_date, countries_iso2=countries_iso2)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        
        b.write(Long(self.id))
        flags = 0
        flags |= (1 << 0) if self.closed else 0
        flags |= (1 << 1) if self.public_voters else 0
        flags |= (1 << 2) if self.multiple_choice else 0
        flags |= (1 << 3) if self.quiz else 0
        flags |= (1 << 6) if self.open_answers else 0
        flags |= (1 << 7) if self.revoting_disabled else 0
        flags |= (1 << 8) if self.shuffle_answers else 0
        flags |= (1 << 9) if self.hide_results_until_close else 0
        flags |= (1 << 10) if self.creator else 0
        flags |= (1 << 11) if self.subscribers_only else 0
        flags |= (1 << 4) if self.close_period is not None else 0
        flags |= (1 << 5) if self.close_date is not None else 0
        flags |= (1 << 12) if self.countries_iso2 else 0
        b.write(Int(flags))
        
        b.write(self.question.write())
        
        b.write(Vector(self.answers))
        
        if self.close_period is not None:
            b.write(Int(self.close_period))
        
        if self.close_date is not None:
            b.write(Int(self.close_date))
        
        if self.countries_iso2:
            b.write(Vector(self.countries_iso2, String))
        
        b.write(Long(self.hash))
        
        return b.getvalue()
