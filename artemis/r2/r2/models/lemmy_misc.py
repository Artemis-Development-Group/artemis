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


class LemmyModLog(Thing):
    """Lemmy Mod Log - moderator action log"""
    _thing_type = "lemmy_mod_log"
    _data_int_props = Thing._data_int_props + ('modlog_type',)
    _essentials = ('mod_person_id', 'action')
    
    @classmethod
    def _new(cls, mod_person_id, action, post_id=None, comment_id=None,
             community_id=None, person_id=None, published_at=None,
             reason=None, modlog_type=0):
        thing = cls(mod_person_id=mod_person_id, action=action,
                   post_id=post_id, comment_id=comment_id,
                   community_id=community_id, person_id=person_id,
                   published_at=published_at or datetime.utcnow(),
                   reason=reason, modlog_type=modlog_type)
        thing._commit()
        return thing


class LemmySecret(Thing):
    """Lemmy Secret - stored secrets for the site"""
    _thing_type = "lemmy_secret"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('secret',)
    
    @classmethod
    def _new(cls, secret, published_at=None, updated_at=None):
        thing = cls(secret=secret,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at)
        thing._commit()
        return thing


class LemmyTagline(Thing):
    """Lemmy Tagline - site taglines displayed on the frontend"""
    _thing_type = "lemmy_tagline"
    _data_int_props = Thing._data_int_props + ('display_order',)
    _essentials = ('local_site_id', 'content')
    
    @classmethod
    def _new(cls, local_site_id, content, published_at=None, updated_at=None,
             deleted=False, local=True, ap_id="", display_order=0):
        thing = cls(local_site_id=local_site_id, content=content,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted,
                   local=local, ap_id=ap_id, display_order=display_order)
        thing._commit()
        return thing


class LemmyLocalSiteUrlBlocklist(Thing):
    """Lemmy Local Site URL Blocklist - blocked URLs for the site"""
    _thing_type = "lemmy_local_site_url_blocklist"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('local_site_id', 'url')
    
    @classmethod
    def _new(cls, local_site_id, url, published_at=None, updated_at=None):
        thing = cls(local_site_id=local_site_id, url=url,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at)
        thing._commit()
        return thing
