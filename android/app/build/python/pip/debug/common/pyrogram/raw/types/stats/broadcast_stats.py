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


class BroadcastStats(TLObject):
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.stats.BroadcastStats`.

    Details:
        - Layer: ``228``
        - ID: ``396CA5FC``

    Parameters:
        period (:obj:`StatsDateRangeDays <pyrogram.raw.base.StatsDateRangeDays>`):
            N/A

        followers (:obj:`StatsAbsValueAndPrev <pyrogram.raw.base.StatsAbsValueAndPrev>`):
            N/A

        views_per_post (:obj:`StatsAbsValueAndPrev <pyrogram.raw.base.StatsAbsValueAndPrev>`):
            N/A

        shares_per_post (:obj:`StatsAbsValueAndPrev <pyrogram.raw.base.StatsAbsValueAndPrev>`):
            N/A

        reactions_per_post (:obj:`StatsAbsValueAndPrev <pyrogram.raw.base.StatsAbsValueAndPrev>`):
            N/A

        views_per_story (:obj:`StatsAbsValueAndPrev <pyrogram.raw.base.StatsAbsValueAndPrev>`):
            N/A

        shares_per_story (:obj:`StatsAbsValueAndPrev <pyrogram.raw.base.StatsAbsValueAndPrev>`):
            N/A

        reactions_per_story (:obj:`StatsAbsValueAndPrev <pyrogram.raw.base.StatsAbsValueAndPrev>`):
            N/A

        enabled_notifications (:obj:`StatsPercentValue <pyrogram.raw.base.StatsPercentValue>`):
            N/A

        growth_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        followers_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        mute_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        top_hours_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        interactions_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        iv_interactions_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        views_by_source_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        new_followers_by_source_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        languages_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        reactions_by_emotion_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        story_interactions_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        story_reactions_by_emotion_graph (:obj:`StatsGraph <pyrogram.raw.base.StatsGraph>`):
            N/A

        recent_posts_interactions (List of :obj:`PostInteractionCounters <pyrogram.raw.base.PostInteractionCounters>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            stats.GetBroadcastStats
    """

    __slots__: List[str] = ["period", "followers", "views_per_post", "shares_per_post", "reactions_per_post", "views_per_story", "shares_per_story", "reactions_per_story", "enabled_notifications", "growth_graph", "followers_graph", "mute_graph", "top_hours_graph", "interactions_graph", "iv_interactions_graph", "views_by_source_graph", "new_followers_by_source_graph", "languages_graph", "reactions_by_emotion_graph", "story_interactions_graph", "story_reactions_by_emotion_graph", "recent_posts_interactions"]

    ID = 0x396ca5fc
    QUALNAME = "types.stats.BroadcastStats"

    def __init__(self, *, period: "raw.base.StatsDateRangeDays", followers: "raw.base.StatsAbsValueAndPrev", views_per_post: "raw.base.StatsAbsValueAndPrev", shares_per_post: "raw.base.StatsAbsValueAndPrev", reactions_per_post: "raw.base.StatsAbsValueAndPrev", views_per_story: "raw.base.StatsAbsValueAndPrev", shares_per_story: "raw.base.StatsAbsValueAndPrev", reactions_per_story: "raw.base.StatsAbsValueAndPrev", enabled_notifications: "raw.base.StatsPercentValue", growth_graph: "raw.base.StatsGraph", followers_graph: "raw.base.StatsGraph", mute_graph: "raw.base.StatsGraph", top_hours_graph: "raw.base.StatsGraph", interactions_graph: "raw.base.StatsGraph", iv_interactions_graph: "raw.base.StatsGraph", views_by_source_graph: "raw.base.StatsGraph", new_followers_by_source_graph: "raw.base.StatsGraph", languages_graph: "raw.base.StatsGraph", reactions_by_emotion_graph: "raw.base.StatsGraph", story_interactions_graph: "raw.base.StatsGraph", story_reactions_by_emotion_graph: "raw.base.StatsGraph", recent_posts_interactions: List["raw.base.PostInteractionCounters"]) -> None:
        self.period = period  # StatsDateRangeDays
        self.followers = followers  # StatsAbsValueAndPrev
        self.views_per_post = views_per_post  # StatsAbsValueAndPrev
        self.shares_per_post = shares_per_post  # StatsAbsValueAndPrev
        self.reactions_per_post = reactions_per_post  # StatsAbsValueAndPrev
        self.views_per_story = views_per_story  # StatsAbsValueAndPrev
        self.shares_per_story = shares_per_story  # StatsAbsValueAndPrev
        self.reactions_per_story = reactions_per_story  # StatsAbsValueAndPrev
        self.enabled_notifications = enabled_notifications  # StatsPercentValue
        self.growth_graph = growth_graph  # StatsGraph
        self.followers_graph = followers_graph  # StatsGraph
        self.mute_graph = mute_graph  # StatsGraph
        self.top_hours_graph = top_hours_graph  # StatsGraph
        self.interactions_graph = interactions_graph  # StatsGraph
        self.iv_interactions_graph = iv_interactions_graph  # StatsGraph
        self.views_by_source_graph = views_by_source_graph  # StatsGraph
        self.new_followers_by_source_graph = new_followers_by_source_graph  # StatsGraph
        self.languages_graph = languages_graph  # StatsGraph
        self.reactions_by_emotion_graph = reactions_by_emotion_graph  # StatsGraph
        self.story_interactions_graph = story_interactions_graph  # StatsGraph
        self.story_reactions_by_emotion_graph = story_reactions_by_emotion_graph  # StatsGraph
        self.recent_posts_interactions = recent_posts_interactions  # Vector<PostInteractionCounters>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BroadcastStats":
        # No flags
        
        period = TLObject.read(b)
        
        followers = TLObject.read(b)
        
        views_per_post = TLObject.read(b)
        
        shares_per_post = TLObject.read(b)
        
        reactions_per_post = TLObject.read(b)
        
        views_per_story = TLObject.read(b)
        
        shares_per_story = TLObject.read(b)
        
        reactions_per_story = TLObject.read(b)
        
        enabled_notifications = TLObject.read(b)
        
        growth_graph = TLObject.read(b)
        
        followers_graph = TLObject.read(b)
        
        mute_graph = TLObject.read(b)
        
        top_hours_graph = TLObject.read(b)
        
        interactions_graph = TLObject.read(b)
        
        iv_interactions_graph = TLObject.read(b)
        
        views_by_source_graph = TLObject.read(b)
        
        new_followers_by_source_graph = TLObject.read(b)
        
        languages_graph = TLObject.read(b)
        
        reactions_by_emotion_graph = TLObject.read(b)
        
        story_interactions_graph = TLObject.read(b)
        
        story_reactions_by_emotion_graph = TLObject.read(b)
        
        recent_posts_interactions = TLObject.read(b)
        
        return BroadcastStats(period=period, followers=followers, views_per_post=views_per_post, shares_per_post=shares_per_post, reactions_per_post=reactions_per_post, views_per_story=views_per_story, shares_per_story=shares_per_story, reactions_per_story=reactions_per_story, enabled_notifications=enabled_notifications, growth_graph=growth_graph, followers_graph=followers_graph, mute_graph=mute_graph, top_hours_graph=top_hours_graph, interactions_graph=interactions_graph, iv_interactions_graph=iv_interactions_graph, views_by_source_graph=views_by_source_graph, new_followers_by_source_graph=new_followers_by_source_graph, languages_graph=languages_graph, reactions_by_emotion_graph=reactions_by_emotion_graph, story_interactions_graph=story_interactions_graph, story_reactions_by_emotion_graph=story_reactions_by_emotion_graph, recent_posts_interactions=recent_posts_interactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.period.write())
        
        b.write(self.followers.write())
        
        b.write(self.views_per_post.write())
        
        b.write(self.shares_per_post.write())
        
        b.write(self.reactions_per_post.write())
        
        b.write(self.views_per_story.write())
        
        b.write(self.shares_per_story.write())
        
        b.write(self.reactions_per_story.write())
        
        b.write(self.enabled_notifications.write())
        
        b.write(self.growth_graph.write())
        
        b.write(self.followers_graph.write())
        
        b.write(self.mute_graph.write())
        
        b.write(self.top_hours_graph.write())
        
        b.write(self.interactions_graph.write())
        
        b.write(self.iv_interactions_graph.write())
        
        b.write(self.views_by_source_graph.write())
        
        b.write(self.new_followers_by_source_graph.write())
        
        b.write(self.languages_graph.write())
        
        b.write(self.reactions_by_emotion_graph.write())
        
        b.write(self.story_interactions_graph.write())
        
        b.write(self.story_reactions_by_emotion_graph.write())
        
        b.write(Vector(self.recent_posts_interactions))
        
        return b.getvalue()
