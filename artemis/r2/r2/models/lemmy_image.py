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


class LemmyLocalImage(Thing):
    """Lemmy Local Image - images stored locally"""
    _thing_type = "lemmy_local_image"
    _data_int_props = Thing._data_int_props + ('width', 'height', 'size')
    _essentials = ('local_user_id', 'pictrs_alias', 'pictrs_delete_token')
    
    @classmethod
    def _new(cls, local_user_id, pictrs_alias, pictrs_delete_token,
             published_at=None, updated_at=None, width=None, height=None,
             size=None, original_url=None, dethumbnail_url=None):
        thing = cls(local_user_id=local_user_id, pictrs_alias=pictrs_alias,
                   pictrs_delete_token=pictrs_delete_token,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, width=width, height=height,
                   size=size, original_url=original_url,
                   dethumbnail_url=dethumbnail_url)
        thing._commit()
        return thing


class LemmyRemoteImage(Thing):
    """Lemmy Remote Image - links to remote images"""
    _thing_type = "lemmy_remote_image"
    _data_int_props = Thing._data_int_props + ('width', 'height', 'size')
    _essentials = ('link_id', 'url')
    
    @classmethod
    def _new(cls, link_id, url, published_at=None, updated_at=None,
             width=None, height=None, size=None, local=True, ap_id=""):
        thing = cls(link_id=link_id, url=url,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at, width=width, height=height,
                   size=size, local=local, ap_id=ap_id)
        thing._commit()
        return thing


class LemmyImageDetails(Thing):
    """Lemmy Image Details - detailed image metadata"""
    _thing_type = "lemmy_image_details"
    _data_int_props = Thing._data_int_props + ('width', 'height', 'size')
    _essentials = ('image_id',)
    
    @classmethod
    def _new(cls, image_id, width=None, height=None, size=None,
             published_at=None, updated_at=None):
        thing = cls(image_id=image_id, width=width, height=height, size=size,
                   published_at=published_at or datetime.utcnow(),
                   updated_at=updated_at)
        thing._commit()
        return thing
