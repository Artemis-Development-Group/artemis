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
from r2.lib.db.operators import lower
from r2.lib.utils import tup


class LemmyPerson(Thing):
    """Lemmy Person model - represents a user account (equivalent to Lemmy's person.rs)"""
    _thing_type = "lemmy_person"
    _data_int_props = Thing._data_int_props + ('post_count', 'comment_count', 
                                                'post_score', 'comment_score')
    _essentials = ('name', 'instance_id')
    
    @classmethod
    def _new(cls, name, instance_id, display_name=None, avatar=None, 
             bio=None, local=True, public_key="", private_key=None,
             banner=None, inbox_url="", matrix_user_id=None, bot_account=False,
             ap_id="", published_at=None, updated_at=None, deleted=False,
             last_refreshed_at=None):
        thing = cls(name=name, instance_id=instance_id,
                   display_name=display_name, avatar=avatar, bio=bio,
                   local=local, public_key=public_key, private_key=private_key,
                   banner=banner, inbox_url=inbox_url, 
                   matrix_user_id=matrix_user_id, bot_account=bot_account,
                   ap_id=ap_id, published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, deleted=deleted,
                   last_refreshed_at=last_refreshed_at or datetime.utcnow(),
                   post_count=0, comment_count=0, post_score=0, comment_score=0)
        thing._commit()
        return thing


class LemmyPersonActions(Thing):
    """Lemmy Person Actions - tracks user actions on persons (follow, block, etc.)"""
    _thing_type = "lemmy_person_actions"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id', 'target_person_id')
    
    @classmethod
    def _new(cls, person_id, target_person_id, followed_at=None, 
             blocked_at=None, received_ban_at=None, ban_expires_at=None):
        thing = cls(person_id=person_id, target_person_id=target_person_id,
                   followed_at=followed_at, blocked_at=blocked_at,
                   received_ban_at=received_ban_at, ban_expires_at=ban_expires_at)
        thing._commit()
        return thing


class LemmyLocalUser(Thing):
    """Lemmy Local User - additional settings for local users (equivalent to Lemmy's local_user.rs)"""
    _thing_type = "lemmy_local_user"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('person_id',)
    
    @classmethod
    def _new(cls, person_id, email=None, password_encrypted="", 
             published_at=None, updated_at=None, show_nsfw=False,
             theme="", default_sort_type=0, default_listing_type=0,
             interface_language="en", show_avatars=True, send_notifications_to_email=True,
             preferred_username=None, bio=None, matrix_user_id=None,
             show_bot_accounts=True, show_read_posts=True, show_new_post_notifs=True,
             email_verified=False, accepted_application=False, totp_2fa_enabled=False):
        thing = cls(person_id=person_id, email=email, 
                   password_encrypted=password_encrypted,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, show_nsfw=show_nsfw,
                   theme=theme, default_sort_type=default_sort_type,
                   default_listing_type=default_listing_type,
                   interface_language=interface_language,
                   show_avatars=show_avatars,
                   send_notifications_to_email=send_notifications_to_email,
                   preferred_username=preferred_username, bio=bio,
                   matrix_user_id=matrix_user_id,
                   show_bot_accounts=show_bot_accounts,
                   show_read_posts=show_read_posts,
                   show_new_post_notifs=show_new_post_notifs,
                   email_verified=email_verified,
                   accepted_application=accepted_application,
                   totp_2fa_enabled=totp_2fa_enabled)
        thing._commit()
        return thing
