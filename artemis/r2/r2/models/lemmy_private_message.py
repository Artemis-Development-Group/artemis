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


class LemmyPrivateMessage(Thing):
    """Lemmy Private Message model - represents direct messages between users"""
    _thing_type = "lemmy_private_message"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('creator_id', 'recipient_id', 'content')
    
    @classmethod
    def _new(cls, creator_id, recipient_id, content, published_at=None, 
             updated_at=None, deleted=False, read_at=None, ap_id="", local=True):
        thing = cls(creator_id=creator_id, recipient_id=recipient_id,
                   content=content,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted, read_at=read_at,
                   ap_id=ap_id, local=local)
        thing._commit()
        return thing


class LemmyPrivateMessageReport(Thing):
    """Lemmy Private Message Report - reports on private messages"""
    _thing_type = "lemmy_private_message_report"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('creator_id', 'private_message_id', 'reason')
    
    @classmethod
    def _new(cls, creator_id, private_message_id, reason, published_at=None,
             resolved_at=None, resolver_id=None):
        thing = cls(creator_id=creator_id, private_message_id=private_message_id,
                   reason=reason,
                   published_at=published_at or datetime.utcnow(),
                   resolved_at=resolved_at, resolver_id=resolver_id)
        thing._commit()
        return thing
