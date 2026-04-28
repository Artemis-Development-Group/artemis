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


class LemmyLanguage(Thing):
    """Lemmy Language - language definitions"""
    _thing_type = "lemmy_language"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('code', 'name')
    
    @classmethod
    def _new(cls, code, name, published_at=None, updated_at=None):
        thing = cls(code=code, name=name,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at)
        thing._commit()
        return thing


class LemmyLocalUserLanguage(Thing):
    """Lemmy Local User Language - languages selected by a user"""
    _thing_type = "lemmy_local_user_language"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('local_user_id', 'language_id')
    
    @classmethod
    def _new(cls, local_user_id, language_id, published_at=None):
        thing = cls(local_user_id=local_user_id, language_id=language_id,
                   published_at=published_at or datetime.utcnow())
        thing._commit()
        return thing


class LemmyCommunityLanguage(Thing):
    """Lemmy Community Language - languages allowed in a community"""
    _thing_type = "lemmy_community_language"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('community_id', 'language_id')
    
    @classmethod
    def _new(cls, community_id, language_id, published_at=None):
        thing = cls(community_id=community_id, language_id=language_id,
                   published_at=published_at or datetime.utcnow())
        thing._commit()
        return thing


class LemmySiteLanguage(Thing):
    """Lemmy Site Language - languages allowed on the site"""
    _thing_type = "lemmy_site_language"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('site_id', 'language_id')
    
    @classmethod
    def _new(cls, site_id, language_id, published_at=None):
        thing = cls(site_id=site_id, language_id=language_id,
                   published_at=published_at or datetime.utcnow())
        thing._commit()
        return thing


class LemmyKeywordBlock(Thing):
    """Lemmy Keyword Block - keywords blocked by a user"""
    _thing_type = "lemmy_keyword_block"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('local_user_id', 'keyword')
    
    @classmethod
    def _new(cls, local_user_id, keyword, published_at=None):
        thing = cls(local_user_id=local_user_id, keyword=keyword,
                   published_at=published_at or datetime.utcnow())
        thing._commit()
        return thing
