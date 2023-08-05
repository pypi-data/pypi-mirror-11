# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

from __future__ import absolute_import, print_function, unicode_literals

from sickle import Sickle

from .errors import NameOrUrlMissing, WrongDateCombination
from .utils import get_oaiharvest_object


def list_records(metadata_prefix=None, from_date=None, until_date=None,
                 url=None, name=None, setSpec=None):
    """Harvest records from an OAI repo, based on datestamp and/or set parameters.

    :param metadata_prefix: The prefix for the metadata return (defaults to 'oai_dc').
    :param from_date: The lower bound date for the harvesting (optional).
    :param until_date: The upper bound date for the harvesting (optional).
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :param setSpec: The 'set' criteria for the harvesting (optional).
    :return: An iterator of harvested records.
    """
    if url:
        request = Sickle(url)
    elif name:
        request, _metadata_prefix, lastrun = get_from_oai_name(name)

        # In case we provide a prefix, we don't want it to be
        # overwritten by the one we get from the name variable.
        if metadata_prefix is None:
            metadata_prefix = _metadata_prefix
    else:
        raise NameOrUrlMissing("Retry using the parameters -n <name> or -u <url>.")

    # By convention, when we have a url we have no lastrun, and when we use
    # the name we can either have from_date (if provided) or lastrun.
    dates = {
        'from': lastrun if from_date is None else from_date,
        'until': until_date
    }

    # Sanity check
    if (dates['until'] is not None) and (dates['from'] > dates['until']):
        raise WrongDateCombination("'Until' date larger than 'from' date.")

    if metadata_prefix is None:
        metadata_prefix = "oai_dc"

    return request.ListRecords(metadataPrefix=metadata_prefix,
                               set=setSpec,
                               **dates)


def get_records(identifiers, metadata_prefix=None, url=None, name=None):
    """Harvest specific records from an OAI repo, based on their unique identifiers.

    :param metadata_prefix: The prefix for the metadata return (defaults to 'oai_dc').
    :param identifiers: A list of unique identifiers for records to be harvested.
    :param url: The The url to be used to create the endpoint.
    :param name: The name of the OaiHARVEST object that we want to use to create the endpoint.
    :return: An iterator of harvested records.
    """
    if url:
        request = Sickle(url)
    elif name:
        request, _metadata_prefix, _ = get_from_oai_name(name)

        # In case we provide a prefix, we don't want it to be
        # overwritten by the one we get from the name variable.
        if metadata_prefix is None:
            metadata_prefix = _metadata_prefix
    else:
        raise NameOrUrlMissing("Retry using the parameters -n <name> or -u <url>.")

    if metadata_prefix is None:
        metadata_prefix = "oai_dc"

    for identifier in identifiers:
        arguments = {
            'identifier': identifier,
            'metadataPrefix': metadata_prefix
        }
        yield request.GetRecord(**arguments)


def get_from_oai_name(name):
    """Get basic OAI request data from the OaiHARVEST model.

    :param name: name of the source (OaiHARVEST.name)

    :return: (Sickle obj, metadataprefix, lastrun)
    """
    obj = get_oaiharvest_object(name)

    req = Sickle(obj.baseurl)
    metadata_prefix = obj.metadataprefix
    lastrun = obj.lastrun
    return req, metadata_prefix, lastrun
