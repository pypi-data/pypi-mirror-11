#!/usr/bin/env python
"""
An example of converting from a dn string to APIC Cobra Python SDK.

Written by Mike Timm (mtimm@cisco.com)

Copyright (C) 2014 Cisco Systems Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from urlparse import urlparse, ResultMixin
from collections import OrderedDict, namedtuple
from cobra.mit.naming import Dn


class ApicParseResult(namedtuple('ApicParseResult',
                                 'scheme netloc path params query fragment'),
                      ResultMixin):

    """ApicParseResult.

    Mixin type of class that adds some apic specific properties to the urlparse
    named tuple
    """

    @property
    def dn_or_class(self):
        """Return the dn or the class."""
        pathparts = self._get_path_parts()
        if pathparts[1] != 'node':
            return self._get_dn_or_class(pathparts, 1)
        else:
            return self._get_dn_or_class(pathparts, 2)

    @property
    def api_format(self):
        """Return the api format."""
        return self._get_api_format(self.path)

    @property
    def api_method(self):
        """Return the api method."""
        pathparts = self._get_path_parts()
        if pathparts[1] == 'node':
            return pathparts[2]
        else:
            return pathparts[1]

    @property
    def classnode(self):
        """Return the class node."""
        if self.api_method != 'class':
            return ""
        pathparts = self._get_path_parts()
        if pathparts[1] != 'node':
            return self._get_classnode(pathparts, 3)
        else:
            return self._get_classnode(pathparts, 4)

    @staticmethod
    def _get_classnode(parts, index):
        """Get the class node."""
        if len(parts) <= index:
            return ""
        else:
            return "/".join(parts[index - 1:-1])

    def _get_path_parts(self):
        """Break the path up into a list and return it."""
        dn_str = self._remove_format_from_path(self.path, self.api_format)
        return dn_str[1:].split("/")

    @staticmethod
    def _remove_format_from_path(path, fmt):
        """Remove the api format from the path."""
        return path[:-len("." + fmt)]

    @staticmethod
    def _get_api_format(path):
        """Get the api format."""
        if path.endswith(".xml"):
            return 'xml'
        elif path.endswith(".json"):
            return 'json'

    @staticmethod
    def _get_dn_or_class(parts, index):
        """Get the dn or the class depending on the type of query."""
        if parts[index] == 'class':
            return parts[-1]
        elif parts[index] == 'mo':
            return "/".join(parts[index + 1:])
        else:
            return ""


def apic_rest_urlparse(url_str):
    """Parse an ACI REST API URL."""
    tpl = urlparse(url_str)
    scheme, netloc, path, params, query, fragment = tpl
    return ApicParseResult(scheme, netloc, path, params, query, fragment)


def convert_dn_to_cobra(dn_str):
    """Convert an ACI distinguished name to ACI Python SDK code."""
    cobra_dn = Dn.fromString(dn_str)
    parent_mo_or_dn = "''"
    dn_dict = OrderedDict()
    for rn_obj in cobra_dn.rns:
        rn_str = str(rn_obj)
        dn_dict[rn_str] = {}
        dn_dict[rn_str]['namingVals'] = list(rn_obj.namingVals)
        dn_dict[rn_str]['moClassName'] = rn_obj.meta.moClassName
        dn_dict[rn_str]['className'] = rn_obj.meta.className
        dn_dict[rn_str]['parentMoOrDn'] = parent_mo_or_dn
        parent_mo_or_dn = rn_obj.meta.moClassName
    for arn in dn_dict.items():
        if len(list(arn[1]['namingVals'])) > 0:
            nvals = [str(val) for val in arn[1]['namingVals']]
            nvals_str = ", '" + ", ".join(nvals) + "'"
        else:
            nvals_str = ""
        print "{0} = {1}({2}{3})".format(arn[1]['moClassName'],
                                         arn[1]['className'],
                                         arn[1]['parentMoOrDn'],
                                         nvals_str)


if __name__ == '__main__':
    convert_dn_to_cobra('topology/HDfabricOverallHealth5min-0')
    print("")
    convert_dn_to_cobra('uni/tn-mgmt/mgmtp-default/oob-default')
    print("")

    URL = 'https://10.122.254.211/api/node/mo/topology/HDfabricOverallHealt' + \
          'h5min-0.json'

    convert_dn_to_cobra(apic_rest_urlparse(URL).dn_or_class)
    print("")

    URL = 'https://10.122.254.211/api/node/mo/uni/tn-mgmt/mgmtp-default/oob' + \
          '-default.json'
    convert_dn_to_cobra(apic_rest_urlparse(URL).dn_or_class)
    print
