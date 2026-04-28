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


class LemmyActivity(Thing):
    """Lemmy Activity - tracks federation activity (sent/received)"""
    _thing_type = "lemmy_activity"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('ap_id', 'data', 'local', 'activity_type')
    
    @classmethod
    def _new(cls, ap_id, data, local=True, activity_type=0, published_at=None,
             updated_at=None, received_at=None, sent_at=None,
             instance_id=None, community_id=None, person_id=None):
        thing = cls(ap_id=ap_id, data=data, local=local, activity_type=activity_type,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, received_at=received_at,
                   sent_at=sent_at, instance_id=instance_id,
                   community_id=community_id, person_id=person_id)
        thing._commit()
        return thing


class LemmySentActivity(Thing):
    """Lemmy Sent Activity - tracks outgoing federation activity"""
    _thing_type = "lemmy_sent_activity"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('ap_id', 'data')
    
    @classmethod
    def _new(cls, ap_id, data, published_at=None, updated_at=None,
             send_at=None, send_retry_count=0, instance_id=None):
        thing = cls(ap_id=ap_id, data=data,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, send_at=send_at,
                   send_retry_count=send_retry_count, instance_id=instance_id)
        thing._commit()
        return thing


class LemmyReceivedActivity(Thing):
    """Lemmy Received Activity - tracks incoming federation activity"""
    _thing_type = "lemmy_received_activity"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('ap_id', 'data')
    
    @classmethod
    def _new(cls, ap_id, data, published_at=None, updated_at=None,
             received_at=None, instance_id=None):
        thing = cls(ap_id=ap_id, data=data,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, received_at=received_at,
                   instance_id=instance_id)
        thing._commit()
        return thing


class LemmyFederationAllowList(Thing):
    """Lemmy Federation Allow List - allowed instances for federation"""
    _thing_type = "lemmy_federation_allowlist"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('instance_id',)
    
    @classmethod
    def _new(cls, instance_id):
        thing = cls(instance_id=instance_id)
        thing._commit()
        return thing


class LemmyFederationBlockList(Thing):
    """Lemmy Federation Block List - blocked instances for federation"""
    _thing_type = "lemmy_federation_blocklist"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('instance_id',)
    
    @classmethod
    def _new(cls, instance_id):
        thing = cls(instance_id=instance_id)
        thing._commit()
        return thing


class LemmyFederationQueueState(Thing):
    """Lemmy Federation Queue State - tracks federation queue state"""
    _thing_type = "lemmy_federation_queue_state"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('instance_id',)
    
    @classmethod
    def _new(cls, instance_id, last_successful_send_at=None, 
             last_attempted_send_at=None, fail_count=0):
        thing = cls(instance_id=instance_id,
                   last_successful_send_at=last_successful_send_at,
                   last_attempted_send_at=last_attempted_send_at,
                   fail_count=fail_count)
        thing._commit()
        return thing
