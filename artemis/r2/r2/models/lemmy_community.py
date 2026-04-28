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
from r2.lib.db.operators import lower


class LemmyCommunity(Thing):
    """Lemmy Community model - represents a community/subreddit (equivalent to Lemmy's community.rs)"""
    _thing_type = "lemmy_community"
    _data_int_props = Thing._data_int_props + ('subscribers', 'posts', 'comments',
                                                'users_active_day', 'users_active_week',
                                                'users_active_month', 'users_active_half_year',
                                                'subscribers_local', 'report_count',
                                                'unresolved_report_count', 'random_number')
    _essentials = ('name', 'instance_id')
    
    @classmethod
    def _new(cls, name, instance_id, title=None, sidebar=None, removed=False,
             published_at=None, updated_at=None, deleted=False, nsfw=False,
             ap_id="", local=True, public_key="", private_key=None,
             last_refreshed_at=None, icon=None, banner=None, inbox_url="",
             followers_url=None, posting_restricted_to_mods=False,
             visibility=0, summary=None, hot_rank=0.0,
             moderators_url=None, featured_url=None, local_removed=False,
             subscribers=0, posts=0, comments=0, subscribers_local=0,
             users_active_day=0, users_active_week=0, users_active_month=0,
             users_active_half_year=0, report_count=0, unresolved_report_count=0,
             random_number=0, interactions_month=0):
        thing = cls(name=name, instance_id=instance_id,
                   title=title or name, sidebar=sidebar, removed=removed,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted, nsfw=nsfw,
                   ap_id=ap_id, local=local, public_key=public_key,
                   private_key=private_key,
                   last_refreshed_at=last_refreshed_at or datetime.utcnow(),
                   icon=icon, banner=banner, inbox_url=inbox_url,
                   followers_url=followers_url,
                   posting_restricted_to_mods=posting_restricted_to_mods,
                   visibility=visibility, summary=summary, hot_rank=hot_rank,
                   moderators_url=moderators_url, featured_url=featured_url,
                   local_removed=local_removed, subscribers=subscribers,
                   posts=posts, comments=comments,
                   subscribers_local=subscribers_local,
                   users_active_day=users_active_day,
                   users_active_week=users_active_week,
                   users_active_month=users_active_month,
                   users_active_half_year=users_active_half_year,
                   report_count=report_count,
                   unresolved_report_count=unresolved_report_count,
                   random_number=random_number,
                   interactions_month=interactions_month)
        thing._commit()
        return thing


class LemmyCommunityActions(Thing):
    """Lemmy Community Actions - tracks user actions on communities (follow, block, moderate, etc.)"""
    _thing_type = "lemmy_community_actions"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'community_id')
    
    @classmethod
    def _new(cls, person_id, community_id, followed_at=None, blocked_at=None,
             received_ban_at=None, ban_expires_at=None, became_moderator_at=None,
             feature_local=False, feature_community=False, notification_state=0):
        thing = cls(person_id=person_id, community_id=community_id,
                   followed_at=followed_at, blocked_at=blocked_at,
                   received_ban_at=received_ban_at, ban_expires_at=ban_expires_at,
                   became_moderator_at=became_moderator_at,
                   feature_local=feature_local, feature_community=feature_community,
                   notification_state=notification_state)
        thing._commit()
        return thing


class LemmyCommunityFollow(Thing):
    """Lemmy Community Follow - tracks community follows between communities (for federation)"""
    _thing_type = "lemmy_community_follow"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('community_id', 'target_community_id')
    
    @classmethod
    def _new(cls, community_id, target_community_id):
        thing = cls(community_id=community_id, target_community_id=target_community_id)
        thing._commit()
        return thing
