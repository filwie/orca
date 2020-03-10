# Copyright 2020 OpenRCA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from orca.topology import linker
from orca.topology.infra.k8s import extractor
from orca.topology.infra.k8s import linker as k8s_linker


class EndpointsExtractor(extractor.Extractor):

    def get_kind(self):
        return 'endpoints'

    def _extract_properties(self, entity):
        properties = {}
        properties['name'] = entity.metadata.name
        properties['namespace'] = entity.metadata.namespace
        return properties


class EndpointsToServiceMatcher(linker.Matcher):

    def are_linked(self, endpoints, service):
        match_namespace = k8s_linker.match_namespace(endpoints, service)
        match_name = endpoints.properties.name == service.properties.name
        return match_namespace and match_name