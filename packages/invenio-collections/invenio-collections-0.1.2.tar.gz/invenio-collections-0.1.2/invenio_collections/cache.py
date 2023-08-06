# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2012, 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Implementation of collections caching."""

import warnings

from intbitset import intbitset
from werkzeug import cached_property

from invenio.base.globals import cfg
from invenio.legacy.miscutil.data_cacher import DataCacher, DataCacherProxy
from invenio.utils.memoise import memoize


class CollectionAllChildrenDataCacher(DataCacher):

    """Cache for all children of a collection."""

    def __init__(self):
        """Initilize cache."""
        def cache_filler():
            from .models import Collection
            collections = Collection.query.all()
            collection_index = dict([(c.id, c.name) for c in collections])

            return dict([
                (c.name, map(collection_index.get, c.descendants_ids))
                for c in collections
            ])

        def timestamp_verifier():
            from invenio.legacy.dbquery import get_table_update_time
            return max(get_table_update_time('collection'),
                       get_table_update_time('collection_collection'))

        DataCacher.__init__(self, cache_filler, timestamp_verifier)

collection_allchildren_cache = DataCacherProxy(CollectionAllChildrenDataCacher)


def get_collection_allchildren(coll, recreate_cache_if_needed=True):
    """Return the list of all children of a collection."""
    if recreate_cache_if_needed:
        collection_allchildren_cache.recreate_cache_if_needed()
    if coll not in collection_allchildren_cache.cache:
        return []  # collection does not exist; return empty list
    return collection_allchildren_cache.cache[coll]


@memoize
def get_collection_nbrecs(coll):
    """Return number of records in collection."""
    # FIXME
    return 0


class RestrictedCollectionDataCacher(DataCacher):
    def __init__(self):
        def cache_filler():
            from invenio_access.control import acc_get_action_id
            from invenio_access.local_config import VIEWRESTRCOLL
            from invenio_access.models import (
                AccAuthorization, AccARGUMENT
            )
            VIEWRESTRCOLL_ID = acc_get_action_id(VIEWRESTRCOLL)

            return [auth[0] for auth in AccAuthorization.query.join(
                AccAuthorization.argument
            ).filter(
                AccARGUMENT.keyword == 'collection',
                AccAuthorization.id_accACTION == VIEWRESTRCOLL_ID
            ).values(AccARGUMENT.value)]

        def timestamp_verifier():
            from invenio.legacy.dbquery import get_table_update_time
            return max(get_table_update_time('accROLE_accACTION_accARGUMENT'),
                       get_table_update_time('accARGUMENT'))

        DataCacher.__init__(self, cache_filler, timestamp_verifier)


restricted_collection_cache = DataCacherProxy(RestrictedCollectionDataCacher)


def collection_restricted_p(collection, recreate_cache_if_needed=True):
    if recreate_cache_if_needed:
        restricted_collection_cache.recreate_cache_if_needed()
    return collection in restricted_collection_cache.cache


class CollectionI18nNameDataCacher(DataCacher):
    """
    Provides cache for I18N collection names.  This class is not to be
    used directly; use function get_coll_i18nname() instead.
    """
    def __init__(self):
        def cache_filler():
            from .models import Collection, Collectionname
            res = Collection.query.join(
                Collection.collection_names
            ).filter(Collectionname.type == 'ln').values(
                Collection.name, 'ln', 'value'
            )
            ret = {}
            for c, ln, i18nname in res:
                if i18nname:
                    if c not in ret:
                        ret[c] = {}
                    ret[c][ln] = i18nname
            return ret

        def timestamp_verifier():
            from invenio.legacy.dbquery import get_table_update_time
            return get_table_update_time('collectionname')

        DataCacher.__init__(self, cache_filler, timestamp_verifier)

collection_i18nname_cache = DataCacherProxy(CollectionI18nNameDataCacher)


def get_coll_i18nname(c, ln=None, verify_cache_timestamp=True):
    """Return nicely formatted collection name for given language.

    This function uses collection_i18nname_cache, but it verifies
    whether the cache is up-to-date first by default.  This
    verification step is performed by checking the DB table update
    time.  So, if you call this function 1000 times, it can get very
    slow because it will do 1000 table update time verifications, even
    though collection names change not that often.

    Hence the parameter VERIFY_CACHE_TIMESTAMP which, when set to
    False, will assume the cache is already up-to-date.  This is
    useful namely in the generation of collection lists for the search
    results page.
    """
    ln = ln or cfg['CFG_SITE_LANG']
    if verify_cache_timestamp:
        collection_i18nname_cache.recreate_cache_if_needed()
    out = c
    try:
        out = collection_i18nname_cache.cache[c][ln]
    except KeyError:
        pass  # translation in LN does not exist
    return out
