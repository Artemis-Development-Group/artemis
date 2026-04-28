# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is reddit.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is reddit Inc.
#
# All portions of the code written by reddit are Copyright (c) 2006-2015 artemis
# Inc. All Rights Reserved.
###############################################################################

from datetime import datetime
from r2.lib.db.thing import Thing, Relation


class LemmyPost(Thing):
    """Lemmy Post model - represents a post/submission (equivalent to Lemmy's post.rs)"""
    _thing_type = "lemmy_post"
    _data_int_props = Thing._data_int_props + ('comments', 'score', 'upvotes', 'downvotes',
                                                'language_id', 'report_count', 
                                                'unresolved_report_count', 'embed_video_width',
                                                'embed_video_height')
    _essentials = ('name', 'creator_id', 'community_id')
    
    @classmethod
    def _new(cls, name, creator_id, community_id, url=None, body=None, removed=False,
             locked=False, published_at=None, updated_at=None, deleted=False, nsfw=False,
             embed_title=None, embed_description=None, thumbnail_url=None, ap_id="",
             local=True, embed_video_url=None, language_id=0, featured_community=False,
             featured_local=False, url_content_type=None, alt_text=None,
             scheduled_publish_time_at=None, newest_comment_time_necro_at=None,
             newest_comment_time_at=None, score=0, upvotes=0, downvotes=0,
             hot_rank=0.0, hot_rank_active=0.0, controversy_rank=0.0, scaled_rank=0.0,
             report_count=0, unresolved_report_count=0, federation_pending=False,
             embed_video_width=None, embed_video_height=None):
        thing = cls(name=name, creator_id=creator_id, community_id=community_id,
                   url=url, body=body, removed=removed, locked=locked,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted, nsfw=nsfw,
                   embed_title=embed_title, embed_description=embed_description,
                   thumbnail_url=thumbnail_url, ap_id=ap_id, local=local,
                   embed_video_url=embed_video_url, language_id=language_id,
                   featured_community=featured_community, featured_local=featured_local,
                   url_content_type=url_content_type, alt_text=alt_text,
                   scheduled_publish_time_at=scheduled_publish_time_at,
                   newest_comment_time_necro_at=newest_comment_time_necro_at,
                   newest_comment_time_at=newest_comment_time_at,
                   comments=0, score=score, upvotes=upvotes, downvotes=downvotes,
                   hot_rank=hot_rank, hot_rank_active=hot_rank_active,
                   controversy_rank=controversy_rank, scaled_rank=scaled_rank,
                   report_count=report_count, unresolved_report_count=unresolved_report_count,
                   federation_pending=federation_pending,
                   embed_video_width=embed_video_width,
                   embed_video_height=embed_video_height)
        thing._commit()
        return thing


class LemmyPostActions(Thing):
    """Lemmy Post Actions - tracks user actions on posts (like, save, read, etc.)"""
    _thing_type = "lemmy_post_actions"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'post_id')
    
    @classmethod
    def _new(cls, person_id, post_id, liked_at=None, saved_at=None, read_at=None,
             hidden_at=None, published_at=None, report_count=0, unresolved_report_count=0):
        thing = cls(person_id=person_id, post_id=post_id,
                   liked_at=liked_at, saved_at=saved_at, read_at=read_at,
                   hidden_at=hidden_at, published_at=published_at or datetime.utcnow(),
                   report_count=report_count, unresolved_report_count=unresolved_report_count)
        thing._commit()
        return thing
