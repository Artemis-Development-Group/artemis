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


class LemmySite(Thing):
    """Lemmy Site model - represents site-wide configuration (equivalent to Lemmy's site.rs)"""
    _thing_type = "lemmy_site"
    _data_int_props = Thing._data_int_props + ()
    _essentials = ('instance_id',)
    
    @classmethod
    def _new(cls, instance_id, name=None, sidebar=None, published_at=None,
             updated_at=None, description=None, ap_id="", local=True,
             icon=None, banner=None, last_refreshed_at=None):
        thing = cls(instance_id=instance_id, name=name, sidebar=sidebar,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, description=description,
                   ap_id=ap_id, local=local, icon=icon, banner=banner,
                   last_refreshed_at=last_refreshed_at or datetime.utcnow())
        thing._commit()
        return thing


class LemmyLocalSite(Thing):
    """Lemmy Local Site - site configuration for the local instance"""
    _thing_type = "lemmy_local_site"
    _data_int_props = Thing._data_int_props + ('registration_mode', 'community_visibility',
                                                'default_post_listing_type', 'default_sort_type',
                                                'user_count', 'post_count', 'comment_count',
                                                'local_post_count', 'local_comment_count')
    _essentials = ('site_id',)
    
    @classmethod
    def _new(cls, site_id, published_at=None, updated_at=None,
             enable_downvotes=True, enable_nsfw=True, community_creation_admin_only=False,
             require_email_verification=False, require_application=False,
             application_question=None, private_instance=False,
             default_sort_type=0, default_post_listing_type=0,
             registration_mode=0, captcha_enabled=False, captcha_difficulty=None,
             enable_oauth_registration=False, require_pwa=False,
             max_account_age_minutes=0, max_mention_count=0, max_comment_size=10000,
             max_post_title_length=200, max_post_body_length=50000,
             max_post_url_length=5000, max_poll_option_length=200,
             min_comment_score_for_image_popup=-100,
             max_comment_entries_in_site_view=100,
             max_posts_per_person_per_interval=10, max_posts_per_interval=10,
             max_registrations_per_interval=10, max_password_length=60,
             max_username_length=20, min_password_length=10, min_username_length=3,
             allow_custom_emoji=True, federation_enabled=False,
             federation_debug=False, federation_worker_count=64,
             captcha_allow_bypass=False, slur_filter_regex=None,
             community_visibility=0, notification_settings=None):
        thing = cls(site_id=site_id,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at,
                   enable_downvotes=enable_downvotes, enable_nsfw=enable_nsfw,
                   community_creation_admin_only=community_creation_admin_only,
                   require_email_verification=require_email_verification,
                   require_application=require_application,
                   application_question=application_question,
                   private_instance=private_instance,
                   default_sort_type=default_sort_type,
                   default_post_listing_type=default_post_listing_type,
                   registration_mode=registration_mode,
                   captcha_enabled=captcha_enabled,
                   captcha_difficulty=captcha_difficulty,
                   enable_oauth_registration=enable_oauth_registration,
                   require_pwa=require_pwa,
                   max_account_age_minutes=max_account_age_minutes,
                   max_mention_count=max_mention_count,
                   max_comment_size=max_comment_size,
                   max_post_title_length=max_post_title_length,
                   max_post_body_length=max_post_body_length,
                   max_post_url_length=max_post_url_length,
                   max_poll_option_length=max_poll_option_length,
                   min_comment_score_for_image_popup=min_comment_score_for_image_popup,
                   max_comment_entries_in_site_view=max_comment_entries_in_site_view,
                   max_posts_per_person_per_interval=max_posts_per_person_per_interval,
                   max_posts_per_interval=max_posts_per_interval,
                   max_registrations_per_interval=max_registrations_per_interval,
                   max_password_length=max_password_length,
                   max_username_length=max_username_length,
                   min_password_length=min_password_length,
                   min_username_length=min_username_length,
                   allow_custom_emoji=allow_custom_emoji,
                   federation_enabled=federation_enabled,
                   federation_debug=federation_debug,
                   federation_worker_count=federation_worker_count,
                   captcha_allow_bypass=captcha_allow_bypass,
                   slur_filter_regex=slur_filter_regex,
                   community_visibility=community_visibility,
                   notification_settings=notification_settings,
                   user_count=0, post_count=0, comment_count=0,
                   local_post_count=0, local_comment_count=0)
        thing._commit()
        return thing


class LemmyLocalSiteRateLimit(Thing):
    """Lemmy Local Site Rate Limit - rate limiting configuration"""
    _thing_type = "lemmy_local_site_rate_limit"
    _data_int_props = Thing._data_int_props + ('message', 'post', 'register',
                                                'image', 'comment', 'search')
    _essentials = ('local_site_id',)
    
    @classmethod
    def _new(cls, local_site_id, published_at=None, updated_at=None,
             message=60, post=600, register=30, image=60, comment=600, search=30):
        thing = cls(local_site_id=local_site_id,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at,
                   message=message, post=post, register=register,
                   image=image, comment=comment, search=search)
        thing._commit()
        return thing
