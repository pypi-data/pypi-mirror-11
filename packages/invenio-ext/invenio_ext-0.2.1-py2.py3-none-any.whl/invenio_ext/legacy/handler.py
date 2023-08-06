# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015 CERN.
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

"""Apache request handler mechanism.

It gives the tools to map url to functions, handles the legacy url
scheme (/search.py queries), HTTP/HTTPS switching, language
specification,...
"""

from invenio_base.i18n import wash_language


def wash_urlargd(form, content):
    """
    Wash the complete form based on the specification in
    content. Content is a dictionary containing the field names as a
    key, and a tuple (type, default) as value.

    'type' can be list, str, invenio.legacy.wsgi.utils.StringField, int, tuple, or
    invenio.legacy.wsgi.utils.Field (for
    file uploads).

    The specification automatically includes the 'ln' field, which is
    common to all queries.

    Arguments that are not defined in 'content' are discarded.

    Note that in case {list,tuple} were asked for, we assume that
    {list,tuple} of strings is to be returned.  Therefore beware when
    you want to use wash_urlargd() for multiple file upload forms.

    @Return: argd dictionary that can be used for passing function
    parameters by keywords.
    """

    result = {}

    content['ln'] = (str, '')

    for k, (dst_type, default) in content.items():
        try:
            value = form[k]
        except KeyError:
            result[k] = default
            continue

        # FIXES problems with unicode arguments from Flask
        if isinstance(value, unicode):
            value = value.encode('utf-8')

        src_type = type(value)

        # First, handle the case where we want all the results. In
        # this case, we need to ensure all the elements are strings,
        # and not Field instances.
        if src_type in (list, tuple):
            if dst_type is list:
                result[k] = [str(x) for x in value]
                continue

            if dst_type is tuple:
                result[k] = tuple([str(x) for x in value])
                continue

            # in all the other cases, we are only interested in the
            # first value.
            value = value[0]

        # Maybe we already have what is expected? Then don't change
        # anything.
        if isinstance(value, dst_type):
            result[k] = value
            continue

        # Since we got here, 'value' is sure to be a single symbol,
        # not a list kind of structure anymore.
        if dst_type in (str, int):
            try:
                result[k] = dst_type(value)
            except Exception:
                result[k] = default

        elif dst_type is tuple:
            result[k] = (str(value), )

        elif dst_type is list:
            result[k] = [str(value)]

        else:
            raise ValueError(
                'cannot cast form value %s of type %r into type %r' %
                (value, src_type, dst_type))

    result['ln'] = wash_language(result['ln'])

    return result
