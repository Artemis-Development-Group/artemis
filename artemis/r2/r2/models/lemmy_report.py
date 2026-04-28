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


class LemmyPostReport(Thing):
    """Lemmy Post Report - reports on posts"""
    _thing_type = "lemmy_post_report"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('creator_id', 'post_id', 'reason')
    
    @classmethod
    def _new(cls, creator_id, post_id, reason, published_at=None,
             resolved_at=None, resolver_id=None):
        thing = cls(creator_id=creator_id, post_id=post_id, reason=reason,
                   published_at=published_at or datetime.utcnow(),
                   resolved_at=resolved_at, resolver_id=resolver_id)
        thing._commit()
        return thing


class LemmyCommentReport(Thing):
    """Lemmy Comment Report - reports on comments"""
    _thing_type = "lemmy_comment_report"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('creator_id', 'comment_id', 'reason')
    
    @classmethod
    def _new(cls, creator_id, comment_id, reason, published_at=None,
             resolved_at=None, resolver_id=None):
        thing = cls(creator_id=creator_id, comment_id=comment_id, reason=reason,
                   published_at=published_at or datetime.utcnow(),
                   resolved_at=resolved_at, resolver_id=resolver_id)
        thing._commit()
        return thing


class LemmyCommunityReport(Thing):
    """Lemmy Community Report - reports on communities"""
    _thing_type = "lemmy_community_report"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('creator_id', 'community_id', 'reason')
    
    @classmethod
    def _new(cls, creator_id, community_id, reason, published_at=None,
             resolved_at=None, resolver_id=None):
        thing = cls(creator_id=creator_id, community_id=community_id, reason=reason,
                   published_at=published_at or datetime.utcnow(),
                   resolved_at=resolved_at, resolver_id=resolver_id)
        thing._commit()
        return thing
