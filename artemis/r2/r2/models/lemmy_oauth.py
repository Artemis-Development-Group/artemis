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


class LemmyOAuthProvider(Thing):
    """Lemmy OAuth Provider - OAuth providers configuration"""
    _thing_type = "lemmy_oauth_provider"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('local_site_id', 'display_name', 'issuer', 'client_id', 'client_secret')
    
    @classmethod
    def _new(cls, local_site_id, display_name, issuer, client_id, client_secret,
             published_at=None, updated_at=None, enabled=True,
             authorize_url=None, token_url=None, userinfo_url=None,
             tls_verify=True, scopes=None):
        thing = cls(local_site_id=local_site_id, display_name=display_name,
                   issuer=issuer, client_id=client_id, client_secret=client_secret,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, enabled=enabled,
                   authorize_url=authorize_url, token_url=token_url,
                   userinfo_url=userinfo_url, tls_verify=tls_verify,
                   scopes=scopes)
        thing._commit()
        return thing


class LemmyOAuthAccount(Thing):
    """Lemmy OAuth Account - user accounts linked to OAuth providers"""
    _thing_type = "lemmy_oauth_account"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('local_user_id', 'oauth_provider_id', 'provider_user_id')
    
    @classmethod
    def _new(cls, local_user_id, oauth_provider_id, provider_user_id,
             published_at=None, updated_at=None, published=True):
        thing = cls(local_user_id=local_user_id, oauth_provider_id=oauth_provider_id,
                   provider_user_id=provider_user_id,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, published=published)
        thing._commit()
        return thing
