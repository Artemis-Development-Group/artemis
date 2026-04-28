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


class LemmyInstance(Thing):
    """Lemmy Instance model - represents a federated instance (equivalent to Lemmy's instance.rs)"""
    _thing_type = "lemmy_instance"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('domain',)
    
    @classmethod
    def _new(cls, domain, published_at=None, updated_at=None, software=None, version=None):
        thing = cls(domain=domain,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, software=software, version=version)
        thing._commit()
        return thing


class LemmyInstanceActions(Thing):
    """Lemmy Instance Actions - tracks user actions on instances (block, ban, etc.)"""
    _thing_type = "lemmy_instance_actions"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'instance_id')
    
    @classmethod
    def _new(cls, person_id, instance_id, blocked_communities_at=None, 
             blocked_persons_at=None, received_ban_at=None, ban_expires_at=None):
        thing = cls(person_id=person_id, instance_id=instance_id,
                   blocked_communities_at=blocked_communities_at,
                   blocked_persons_at=blocked_persons_at,
                   received_ban_at=received_ban_at, ban_expires_at=ban_expires_at)
        thing._commit()
        return thing
