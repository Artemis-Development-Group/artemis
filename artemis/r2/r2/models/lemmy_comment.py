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


class LemmyComment(Thing):
    """Lemmy Comment model - represents a comment (equivalent to Lemmy's comment.rs)"""
    _thing_type = "lemmy_comment"
    _data_int_props = Thing._data_int_props + ('language_id', 'score', 'upvotes', 'downvotes',
                                                'child_count', 'report_count', 
                                                'unresolved_report_count')
    _essentials = ('creator_id', 'post_id', 'community_id', 'content', 'path')
    
    @classmethod
    def _new(cls, creator_id, post_id, community_id, content, path, removed=False,
             published_at=None, updated_at=None, deleted=False, ap_id="", local=True,
             distinguished=False, language_id=0, score=0, upvotes=0, downvotes=0,
             child_count=0, hot_rank=0.0, controversy_rank=0.0,
             report_count=0, unresolved_report_count=0, federation_pending=False,
             locked=False):
        thing = cls(creator_id=creator_id, post_id=post_id, community_id=community_id,
                   content=content, path=path, removed=removed,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted, ap_id=ap_id, local=local,
                   distinguished=distinguished, language_id=language_id,
                   score=score, upvotes=upvotes, downvotes=downvotes,
                   child_count=child_count, hot_rank=hot_rank,
                   controversy_rank=controversy_rank,
                   report_count=report_count, unresolved_report_count=unresolved_report_count,
                   federation_pending=federation_pending, locked=locked)
        thing._commit()
        return thing


class LemmyCommentActions(Thing):
    """Lemmy Comment Actions - tracks user actions on comments (like, save, etc.)"""
    _thing_type = "lemmy_comment_actions"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'comment_id')
    
    @classmethod
    def _new(cls, person_id, comment_id, liked_at=None, saved_at=None, 
             published_at=None, report_count=0, unresolved_report_count=0):
        thing = cls(person_id=person_id, comment_id=comment_id,
                   liked_at=liked_at, saved_at=saved_at,
                   published_at=published_at or datetime.utcnow(),
                   report_count=report_count, unresolved_report_count=unresolved_report_count)
        thing._commit()
        return thing
