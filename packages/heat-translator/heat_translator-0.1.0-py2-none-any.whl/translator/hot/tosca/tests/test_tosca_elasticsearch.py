#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from translator.hot.tosca.custom_types.tosca_elasticsearch import (
    ToscaElasticsearch
    )
from translator.toscalib.tests.base import TestCase


class ToscaElasticsearchTest(TestCase):

    @mock.patch('translator.toscalib.nodetemplate.NodeTemplate')
    @mock.patch('translator.hot.tosca.custom_types.tosca_elasticsearch.'
                'HotResource.__init__')
    def test_init(self, mock_hotres_init, mock_node):
        ToscaElasticsearch(mock_node)
        # Make sure base class gets called
        mock_hotres_init.assert_called_once_with(mock_node)
        self.assertEqual(ToscaElasticsearch.toscatype,
                         'tosca.nodes.SoftwareComponent.Elasticsearch')

    @mock.patch('translator.toscalib.nodetemplate.NodeTemplate')
    @mock.patch('translator.hot.tosca.custom_types.tosca_elasticsearch.'
                'HotResource.__init__')
    def test_handle_properties(self, mock_hotres_init, mock_node):
        p = ToscaElasticsearch(mock_node)
        self.assertIsNone(p.handle_properties())
