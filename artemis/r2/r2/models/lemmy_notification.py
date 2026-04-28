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


class LemmyNotification(Thing):
    """Lemmy Notification model - represents user notifications"""
    _thing_type = "lemmy_notification"
    _data_int_props = Thing._data_int_props + ('notification_type',)
    _essentials = ('person_id', 'comment_id', 'post_id', 'notification_type')
    
    @classmethod
    def _new(cls, person_id, comment_id=None, post_id=None, 
             notification_type=0, published_at=None, read_at=None):
        thing = cls(person_id=person_id, comment_id=comment_id, post_id=post_id,
                   notification_type=notification_type,
                   published_at=published_at or datetime.utcnow(),
                   read_at=read_at)
        thing._commit()
        return thing


class LemmyMultiCommunity(Thing):
    """Lemmy Multi Community - like multireddits"""
    _thing_type = "lemmy_multi_community"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'name')
    
    @classmethod
    def _new(cls, person_id, name, description=None, published_at=None,
             updated_at=None, deleted=False, private=False, local=True, ap_id=""):
        thing = cls(person_id=person_id, name=name, description=description,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted,
                   private=private, local=local, ap_id=ap_id)
        thing._commit()
        return thing


class LemmyCommunityTag(Thing):
    """Lemmy Community Tag - tags for communities"""
    _thing_type = "lemmy_community_tag"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('community_id', 'tag_name')
    
    @classmethod
    def _new(cls, community_id, tag_name, published_at=None, updated_at=None,
             deleted=False, local=True, ap_id=""):
        thing = cls(community_id=community_id, tag_name=tag_name,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted,
                   local=local, ap_id=ap_id)
        thing._commit()
        return thing


class LemmyPostCommunityTag(Thing):
    """Lemmy Post Community Tag - tags applied to posts"""
    _thing_type = "lemmy_post_community_tag"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('post_id', 'community_tag_id')
    
    @classmethod
    def _new(cls, post_id, community_tag_id, published_at=None):
        thing = cls(post_id=post_id, community_tag_id=community_tag_id,
                   published_at=published_at or datetime.utcnow())
        thing._commit()
        return thing
