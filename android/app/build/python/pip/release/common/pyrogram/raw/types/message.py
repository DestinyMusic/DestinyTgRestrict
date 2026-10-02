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


class Message(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Message`.

    Details:
        - Layer: ``228``
        - ID: ``7600B9D3``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

        peer_id (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        date (``int`` ``32-bit``):
            N/A

        message (``str``):
            N/A

        out (``bool``, *optional*):
            N/A

        mentioned (``bool``, *optional*):
            N/A

        media_unread (``bool``, *optional*):
            N/A

        silent (``bool``, *optional*):
            N/A

        post (``bool``, *optional*):
            N/A

        from_scheduled (``bool``, *optional*):
            N/A

        legacy (``bool``, *optional*):
            N/A

        edit_hide (``bool``, *optional*):
            N/A

        pinned (``bool``, *optional*):
            N/A

        noforwards (``bool``, *optional*):
            N/A

        invert_media (``bool``, *optional*):
            N/A

        offline (``bool``, *optional*):
            N/A

        video_processing_pending (``bool``, *optional*):
            N/A

        paid_suggested_post_stars (``bool``, *optional*):
            N/A

        paid_suggested_post_ton (``bool``, *optional*):
            N/A

        from_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        from_boosts_applied (``int`` ``32-bit``, *optional*):
            N/A

        from_rank (``str``, *optional*):
            N/A

        saved_peer_id (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        fwd_from (:obj:`MessageFwdHeader <pyrogram.raw.base.MessageFwdHeader>`, *optional*):
            N/A

        via_bot_id (``int`` ``64-bit``, *optional*):
            N/A

        via_business_bot_id (``int`` ``64-bit``, *optional*):
            N/A

        guestchat_via_from (:obj:`Peer <pyrogram.raw.base.Peer>`, *optional*):
            N/A

        reply_to (:obj:`MessageReplyHeader <pyrogram.raw.base.MessageReplyHeader>`, *optional*):
            N/A

        media (:obj:`MessageMedia <pyrogram.raw.base.MessageMedia>`, *optional*):
            N/A

        reply_markup (:obj:`ReplyMarkup <pyrogram.raw.base.ReplyMarkup>`, *optional*):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

        views (``int`` ``32-bit``, *optional*):
            N/A

        forwards (``int`` ``32-bit``, *optional*):
            N/A

        replies (:obj:`MessageReplies <pyrogram.raw.base.MessageReplies>`, *optional*):
            N/A

        edit_date (``int`` ``32-bit``, *optional*):
            N/A

        post_author (``str``, *optional*):
            N/A

        grouped_id (``int`` ``64-bit``, *optional*):
            N/A

        reactions (:obj:`MessageReactions <pyrogram.raw.base.MessageReactions>`, *optional*):
            N/A

        restriction_reason (List of :obj:`RestrictionReason <pyrogram.raw.base.RestrictionReason>`, *optional*):
            N/A

        ttl_period (``int`` ``32-bit``, *optional*):
            N/A

        quick_reply_shortcut_id (``int`` ``32-bit``, *optional*):
            N/A

        effect (``int`` ``64-bit``, *optional*):
            N/A

        factcheck (:obj:`FactCheck <pyrogram.raw.base.FactCheck>`, *optional*):
            N/A

        report_delivery_until_date (``int`` ``32-bit``, *optional*):
            N/A

        paid_message_stars (``int`` ``64-bit``, *optional*):
            N/A

        suggested_post (:obj:`SuggestedPost <pyrogram.raw.base.SuggestedPost>`, *optional*):
            N/A

        schedule_repeat_period (``int`` ``32-bit``, *optional*):
            N/A

        summary_from_language (``str``, *optional*):
            N/A

        rich_message (:obj:`RichMessage <pyrogram.raw.base.RichMessage>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "peer_id", "date", "message", "out", "mentioned", "media_unread", "silent", "post", "from_scheduled", "legacy", "edit_hide", "pinned", "noforwards", "invert_media", "offline", "video_processing_pending", "paid_suggested_post_stars", "paid_suggested_post_ton", "from_id", "from_boosts_applied", "from_rank", "saved_peer_id", "fwd_from", "via_bot_id", "via_business_bot_id", "guestchat_via_from", "reply_to", "media", "reply_markup", "entities", "views", "forwards", "replies", "edit_date", "post_author", "grouped_id", "reactions", "restriction_reason", "ttl_period", "quick_reply_shortcut_id", "effect", "factcheck", "report_delivery_until_date", "paid_message_stars", "suggested_post", "schedule_repeat_period", "summary_from_language", "rich_message"]

    ID = 0x7600b9d3
    QUALNAME = "types.Message"

    def __init__(self, *, id: int, peer_id: "raw.base.Peer", date: int, message: str, out: Optional[bool] = None, mentioned: Optional[bool] = None, media_unread: Optional[bool] = None, silent: Optional[bool] = None, post: Optional[bool] = None, from_scheduled: Optional[bool] = None, legacy: Optional[bool] = None, edit_hide: Optional[bool] = None, pinned: Optional[bool] = None, noforwards: Optional[bool] = None, invert_media: Optional[bool] = None, offline: Optional[bool] = None, video_processing_pending: Optional[bool] = None, paid_suggested_post_stars: Optional[bool] = None, paid_suggested_post_ton: Optional[bool] = None, from_id: "raw.base.Peer" = None, from_boosts_applied: Optional[int] = None, from_rank: Optional[str] = None, saved_peer_id: "raw.base.Peer" = None, fwd_from: "raw.base.MessageFwdHeader" = None, via_bot_id: Optional[int] = None, via_business_bot_id: Optional[int] = None, guestchat_via_from: "raw.base.Peer" = None, reply_to: "raw.base.MessageReplyHeader" = None, media: "raw.base.MessageMedia" = None, reply_markup: "raw.base.ReplyMarkup" = None, entities: Optional[List["raw.base.MessageEntity"]] = None, views: Optional[int] = None, forwards: Optional[int] = None, replies: "raw.base.MessageReplies" = None, edit_date: Optional[int] = None, post_author: Optional[str] = None, grouped_id: Optional[int] = None, reactions: "raw.base.MessageReactions" = None, restriction_reason: Optional[List["raw.base.RestrictionReason"]] = None, ttl_period: Optional[int] = None, quick_reply_shortcut_id: Optional[int] = None, effect: Optional[int] = None, factcheck: "raw.base.FactCheck" = None, report_delivery_until_date: Optional[int] = None, paid_message_stars: Optional[int] = None, suggested_post: "raw.base.SuggestedPost" = None, schedule_repeat_period: Optional[int] = None, summary_from_language: Optional[str] = None, rich_message: "raw.base.RichMessage" = None) -> None:
        self.id = id  # int
        self.peer_id = peer_id  # Peer
        self.date = date  # int
        self.message = message  # string
        self.out = out  # flags.1?true
        self.mentioned = mentioned  # flags.4?true
        self.media_unread = media_unread  # flags.5?true
        self.silent = silent  # flags.13?true
        self.post = post  # flags.14?true
        self.from_scheduled = from_scheduled  # flags.18?true
        self.legacy = legacy  # flags.19?true
        self.edit_hide = edit_hide  # flags.21?true
        self.pinned = pinned  # flags.24?true
        self.noforwards = noforwards  # flags.26?true
        self.invert_media = invert_media  # flags.27?true
        self.offline = offline  # flags2.1?true
        self.video_processing_pending = video_processing_pending  # flags2.4?true
        self.paid_suggested_post_stars = paid_suggested_post_stars  # flags2.8?true
        self.paid_suggested_post_ton = paid_suggested_post_ton  # flags2.9?true
        self.from_id = from_id  # flags.8?Peer
        self.from_boosts_applied = from_boosts_applied  # flags.29?int
        self.from_rank = from_rank  # flags2.12?string
        self.saved_peer_id = saved_peer_id  # flags.28?Peer
        self.fwd_from = fwd_from  # flags.2?MessageFwdHeader
        self.via_bot_id = via_bot_id  # flags.11?long
        self.via_business_bot_id = via_business_bot_id  # flags2.0?long
        self.guestchat_via_from = guestchat_via_from  # flags2.19?Peer
        self.reply_to = reply_to  # flags.3?MessageReplyHeader
        self.media = media  # flags.9?MessageMedia
        self.reply_markup = reply_markup  # flags.6?ReplyMarkup
        self.entities = entities  # flags.7?Vector<MessageEntity>
        self.views = views  # flags.10?int
        self.forwards = forwards  # flags.10?int
        self.replies = replies  # flags.23?MessageReplies
        self.edit_date = edit_date  # flags.15?int
        self.post_author = post_author  # flags.16?string
        self.grouped_id = grouped_id  # flags.17?long
        self.reactions = reactions  # flags.20?MessageReactions
        self.restriction_reason = restriction_reason  # flags.22?Vector<RestrictionReason>
        self.ttl_period = ttl_period  # flags.25?int
        self.quick_reply_shortcut_id = quick_reply_shortcut_id  # flags.30?int
        self.effect = effect  # flags2.2?long
        self.factcheck = factcheck  # flags2.3?FactCheck
        self.report_delivery_until_date = report_delivery_until_date  # flags2.5?int
        self.paid_message_stars = paid_message_stars  # flags2.6?long
        self.suggested_post = suggested_post  # flags2.7?SuggestedPost
        self.schedule_repeat_period = schedule_repeat_period  # flags2.10?int
        self.summary_from_language = summary_from_language  # flags2.11?string
        self.rich_message = rich_message  # flags2.13?RichMessage

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Message":
        
        flags = Int.read(b)
        
        out = True if flags & (1 << 1) else False
        mentioned = True if flags & (1 << 4) else False
        media_unread = True if flags & (1 << 5) else False
        silent = True if flags & (1 << 13) else False
        post = True if flags & (1 << 14) else False
        from_scheduled = True if flags & (1 << 18) else False
        legacy = True if flags & (1 << 19) else False
        edit_hide = True if flags & (1 << 21) else False
        pinned = True if flags & (1 << 24) else False
        noforwards = True if flags & (1 << 26) else False
        invert_media = True if flags & (1 << 27) else False
        flags2 = Int.read(b)
        
        offline = True if flags2 & (1 << 1) else False
        video_processing_pending = True if flags2 & (1 << 4) else False
        paid_suggested_post_stars = True if flags2 & (1 << 8) else False
        paid_suggested_post_ton = True if flags2 & (1 << 9) else False
        id = Int.read(b)
        
        from_id = TLObject.read(b) if flags & (1 << 8) else None
        
        from_boosts_applied = Int.read(b) if flags & (1 << 29) else None
        from_rank = String.read(b) if flags2 & (1 << 12) else None
        peer_id = TLObject.read(b)
        
        saved_peer_id = TLObject.read(b) if flags & (1 << 28) else None
        
        fwd_from = TLObject.read(b) if flags & (1 << 2) else None
        
        via_bot_id = Long.read(b) if flags & (1 << 11) else None
        via_business_bot_id = Long.read(b) if flags2 & (1 << 0) else None
        guestchat_via_from = TLObject.read(b) if flags2 & (1 << 19) else None
        
        reply_to = TLObject.read(b) if flags & (1 << 3) else None
        
        date = Int.read(b)
        
        message = String.read(b)
        
        media = TLObject.read(b) if flags & (1 << 9) else None
        
        reply_markup = TLObject.read(b) if flags & (1 << 6) else None
        
        entities = TLObject.read(b) if flags & (1 << 7) else []
        
        views = Int.read(b) if flags & (1 << 10) else None
        forwards = Int.read(b) if flags & (1 << 10) else None
        replies = TLObject.read(b) if flags & (1 << 23) else None
        
        edit_date = Int.read(b) if flags & (1 << 15) else None
        post_author = String.read(b) if flags & (1 << 16) else None
        grouped_id = Long.read(b) if flags & (1 << 17) else None
        reactions = TLObject.read(b) if flags & (1 << 20) else None
        
        restriction_reason = TLObject.read(b) if flags & (1 << 22) else []
        
        ttl_period = Int.read(b) if flags & (1 << 25) else None
        quick_reply_shortcut_id = Int.read(b) if flags & (1 << 30) else None
        effect = Long.read(b) if flags2 & (1 << 2) else None
        factcheck = TLObject.read(b) if flags2 & (1 << 3) else None
        
        report_delivery_until_date = Int.read(b) if flags2 & (1 << 5) else None
        paid_message_stars = Long.read(b) if flags2 & (1 << 6) else None
        suggested_post = TLObject.read(b) if flags2 & (1 << 7) else None
        
        schedule_repeat_period = Int.read(b) if flags2 & (1 << 10) else None
        summary_from_language = String.read(b) if flags2 & (1 << 11) else None
        rich_message = TLObject.read(b) if flags2 & (1 << 13) else None
        
        return Message(id=id, peer_id=peer_id, date=date, message=message, out=out, mentioned=mentioned, media_unread=media_unread, silent=silent, post=post, from_scheduled=from_scheduled, legacy=legacy, edit_hide=edit_hide, pinned=pinned, noforwards=noforwards, invert_media=invert_media, offline=offline, video_processing_pending=video_processing_pending, paid_suggested_post_stars=paid_suggested_post_stars, paid_suggested_post_ton=paid_suggested_post_ton, from_id=from_id, from_boosts_applied=from_boosts_applied, from_rank=from_rank, saved_peer_id=saved_peer_id, fwd_from=fwd_from, via_bot_id=via_bot_id, via_business_bot_id=via_business_bot_id, guestchat_via_from=guestchat_via_from, reply_to=reply_to, media=media, reply_markup=reply_markup, entities=entities, views=views, forwards=forwards, replies=replies, edit_date=edit_date, post_author=post_author, grouped_id=grouped_id, reactions=reactions, restriction_reason=restriction_reason, ttl_period=ttl_period, quick_reply_shortcut_id=quick_reply_shortcut_id, effect=effect, factcheck=factcheck, report_delivery_until_date=report_delivery_until_date, paid_message_stars=paid_message_stars, suggested_post=suggested_post, schedule_repeat_period=schedule_repeat_period, summary_from_language=summary_from_language, rich_message=rich_message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.out else 0
        flags |= (1 << 4) if self.mentioned else 0
        flags |= (1 << 5) if self.media_unread else 0
        flags |= (1 << 13) if self.silent else 0
        flags |= (1 << 14) if self.post else 0
        flags |= (1 << 18) if self.from_scheduled else 0
        flags |= (1 << 19) if self.legacy else 0
        flags |= (1 << 21) if self.edit_hide else 0
        flags |= (1 << 24) if self.pinned else 0
        flags |= (1 << 26) if self.noforwards else 0
        flags |= (1 << 27) if self.invert_media else 0
        flags |= (1 << 8) if self.from_id is not None else 0
        flags |= (1 << 29) if self.from_boosts_applied is not None else 0
        flags |= (1 << 28) if self.saved_peer_id is not None else 0
        flags |= (1 << 2) if self.fwd_from is not None else 0
        flags |= (1 << 11) if self.via_bot_id is not None else 0
        flags |= (1 << 3) if self.reply_to is not None else 0
        flags |= (1 << 9) if self.media is not None else 0
        flags |= (1 << 6) if self.reply_markup is not None else 0
        flags |= (1 << 7) if self.entities else 0
        flags |= (1 << 10) if self.views is not None else 0
        flags |= (1 << 10) if self.forwards is not None else 0
        flags |= (1 << 23) if self.replies is not None else 0
        flags |= (1 << 15) if self.edit_date is not None else 0
        flags |= (1 << 16) if self.post_author is not None else 0
        flags |= (1 << 17) if self.grouped_id is not None else 0
        flags |= (1 << 20) if self.reactions is not None else 0
        flags |= (1 << 22) if self.restriction_reason else 0
        flags |= (1 << 25) if self.ttl_period is not None else 0
        flags |= (1 << 30) if self.quick_reply_shortcut_id is not None else 0
        b.write(Int(flags))
        flags2 = 0
        flags2 |= (1 << 1) if self.offline else 0
        flags2 |= (1 << 4) if self.video_processing_pending else 0
        flags2 |= (1 << 8) if self.paid_suggested_post_stars else 0
        flags2 |= (1 << 9) if self.paid_suggested_post_ton else 0
        flags2 |= (1 << 12) if self.from_rank is not None else 0
        flags2 |= (1 << 0) if self.via_business_bot_id is not None else 0
        flags2 |= (1 << 19) if self.guestchat_via_from is not None else 0
        flags2 |= (1 << 2) if self.effect is not None else 0
        flags2 |= (1 << 3) if self.factcheck is not None else 0
        flags2 |= (1 << 5) if self.report_delivery_until_date is not None else 0
        flags2 |= (1 << 6) if self.paid_message_stars is not None else 0
        flags2 |= (1 << 7) if self.suggested_post is not None else 0
        flags2 |= (1 << 10) if self.schedule_repeat_period is not None else 0
        flags2 |= (1 << 11) if self.summary_from_language is not None else 0
        flags2 |= (1 << 13) if self.rich_message is not None else 0
        b.write(Int(flags2))
        
        b.write(Int(self.id))
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        if self.from_boosts_applied is not None:
            b.write(Int(self.from_boosts_applied))
        
        if self.from_rank is not None:
            b.write(String(self.from_rank))
        
        b.write(self.peer_id.write())
        
        if self.saved_peer_id is not None:
            b.write(self.saved_peer_id.write())
        
        if self.fwd_from is not None:
            b.write(self.fwd_from.write())
        
        if self.via_bot_id is not None:
            b.write(Long(self.via_bot_id))
        
        if self.via_business_bot_id is not None:
            b.write(Long(self.via_business_bot_id))
        
        if self.guestchat_via_from is not None:
            b.write(self.guestchat_via_from.write())
        
        if self.reply_to is not None:
            b.write(self.reply_to.write())
        
        b.write(Int(self.date))
        
        b.write(String(self.message))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.entities:
            b.write(Vector(self.entities))
        
        if self.views is not None:
            b.write(Int(self.views))
        
        if self.forwards is not None:
            b.write(Int(self.forwards))
        
        if self.replies is not None:
            b.write(self.replies.write())
        
        if self.edit_date is not None:
            b.write(Int(self.edit_date))
        
        if self.post_author is not None:
            b.write(String(self.post_author))
        
        if self.grouped_id is not None:
            b.write(Long(self.grouped_id))
        
        if self.reactions is not None:
            b.write(self.reactions.write())
        
        if self.restriction_reason:
            b.write(Vector(self.restriction_reason))
        
        if self.ttl_period is not None:
            b.write(Int(self.ttl_period))
        
        if self.quick_reply_shortcut_id is not None:
            b.write(Int(self.quick_reply_shortcut_id))
        
        if self.effect is not None:
            b.write(Long(self.effect))
        
        if self.factcheck is not None:
            b.write(self.factcheck.write())
        
        if self.report_delivery_until_date is not None:
            b.write(Int(self.report_delivery_until_date))
        
        if self.paid_message_stars is not None:
            b.write(Long(self.paid_message_stars))
        
        if self.suggested_post is not None:
            b.write(self.suggested_post.write())
        
        if self.schedule_repeat_period is not None:
            b.write(Int(self.schedule_repeat_period))
        
        if self.summary_from_language is not None:
            b.write(String(self.summary_from_language))
        
        if self.rich_message is not None:
            b.write(self.rich_message.write())
        
        return b.getvalue()
