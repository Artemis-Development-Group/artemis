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


class LemmyLoginToken(Thing):
    """Lemmy Login Token - authentication tokens for users"""
    _thing_type = "lemmy_login_token"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'token')
    
    @classmethod
    def _new(cls, person_id, token, published_at=None, updated_at=None,
             ip=None, user_agent=None):
        thing = cls(person_id=person_id, token=token,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, ip=ip, user_agent=user_agent)
        thing._commit()
        return thing


class LemmyEmailVerification(Thing):
    """Lemmy Email Verification - email verification tokens"""
    _thing_type = "lemmy_email_verification"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'code')
    
    @classmethod
    def _new(cls, person_id, code, published_at=None, updated_at=None, verified_at=None):
        thing = cls(person_id=person_id, code=code,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, verified_at=verified_at)
        thing._commit()
        return thing


class LemmyPasswordResetRequest(Thing):
    """Lemmy Password Reset Request - password reset tokens"""
    _thing_type = "lemmy_password_reset_request"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('local_user_id', 'token')
    
    @classmethod
    def _new(cls, local_user_id, token, published_at=None, updated_at=None,
             reset_at=None):
        thing = cls(local_user_id=local_user_id, token=token,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, reset_at=reset_at)
        thing._commit()
        return thing


class LemmyRegistrationApplication(Thing):
    """Lemmy Registration Application - user registration applications"""
    _thing_type = "lemmy_registration_application"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('local_user_id', 'answer')
    
    @classmethod
    def _new(cls, local_user_id, answer, published_at=None, updated_at=None,
             denied_at=None, resolver_id=None):
        thing = cls(local_user_id=local_user_id, answer=answer,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, denied_at=denied_at,
                   resolver_id=resolver_id)
        thing._commit()
        return thing
