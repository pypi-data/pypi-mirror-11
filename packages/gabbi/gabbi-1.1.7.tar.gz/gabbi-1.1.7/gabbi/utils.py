#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Utility functions grab bag."""

from __future__ import print_function

import httplib2


try:  # Python 3
    ConnectionRefused = ConnectionRefusedError
except NameError:  # Python 2
    import socket
    ConnectionRefused = socket.error


class VerboseHttp(httplib2.Http):
    """A subclass of Http that verbosely reports on activity."""

    def _request(self, conn, host, absolute_uri, request_uri, method, body,
                 headers, redirections, cachekey):
        """Display request parameters before requesting."""

        print('\n%s %s\nHost: %s' % (method, request_uri, host))
        for key in headers:
            print('%s: %s' % (key, headers[key]))

        (response, content) = httplib2.Http._request(
            self, conn, host, absolute_uri, request_uri, method, body,
            headers, redirections, cachekey
        )

        print()
        for key in response.dict:
            print('%s: %s' % (key, response.dict[key]))

        return (response, content)


def decode_content(response, content):
    """Decode content to a proper string."""
    content_type = response.get('content-type',
                                'application/binary').strip().lower()
    charset = 'utf-8'
    if ';' in content_type:
        content_type, parameter_strings = (attr.strip() for attr
                                           in content_type.split(';', 1))
        try:
            parameter_pairs = [atom.strip().split('=')
                               for atom in parameter_strings.split(';')]
            parameters = {name: value for name, value in parameter_pairs}
            charset = parameters['charset']
        except (ValueError, KeyError):
            # KeyError when no charset found.
            # ValueError when the parameter_strings are poorly
            # formed (for example trailing ;)
            pass

    if not_binary(content_type):
        return content.decode(charset)
    else:
        return content


def get_http(verbose=False):
    """Return an Http class for making requests."""
    if verbose:
        return VerboseHttp()
    return httplib2.Http()


def not_binary(content_type):
    """Decide if something is content we'd like to treat as a string."""
    return (content_type.startswith('text/') or
            content_type.endswith('+xml') or
            content_type.endswith('+json') or
            content_type == 'application/javascript' or
            content_type == 'application/json')
