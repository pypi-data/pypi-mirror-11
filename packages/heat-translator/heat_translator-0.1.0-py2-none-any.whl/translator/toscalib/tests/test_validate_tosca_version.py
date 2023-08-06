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

from translator.toscalib.common.exception import (
    InvalidTOSCAVersionPropertyException)
from translator.toscalib.tests.base import TestCase
from translator.toscalib.utils.validateutils import TOSCAVersionProperty


class TOSCAVersionPropertyTest(TestCase):

    def test_tosca_version_property(self):
        version = '18.0.3.beta-1'
        expected_output = '18.0.3.beta-1'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = 18
        expected_output = '18.0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = 18.0
        expected_output = '18.0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = '18.0.3'
        expected_output = '18.0.3'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = 0
        expected_output = None
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = 00
        expected_output = None
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = 0.0
        expected_output = None
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = 00.00
        expected_output = None
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = '0.0.0'
        expected_output = None
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

    def test_tosca_version_property_invalid_major_version(self):

        version = 'x'
        exp_msg = ('Value of TOSCA version property "x" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_minor_version(self):

        version = '18.x'
        exp_msg = ('Value of TOSCA version property "18.x" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

        version = '18.x.y'
        exp_msg = ('Value of TOSCA version property "18.x.y" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

        version = '18-2'
        exp_msg = ('Value of TOSCA version property "18-2" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_fix_version(self):

        version = '18.0.a'
        exp_msg = ('Value of TOSCA version property "18.0.a" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_qualifier(self):

        version = '18.0.1-xyz'
        exp_msg = ('Value of TOSCA version property "18.0.1-xyz" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

        version = '0.0.0.abc'
        exp_msg = ('Value of TOSCA version property "0.0.0.abc" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_build_version(self):

        version = '18.0.1.abc-x'
        exp_msg = ('Value of TOSCA version property '
                   '"18.0.1.abc-x" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())

        version = '0.0.0.abc-x'
        exp_msg = ('Value of TOSCA version property "0.0.0.abc-x" is invalid.')
        try:
            TOSCAVersionProperty(version).get_version()
        except InvalidTOSCAVersionPropertyException as err:
            self.assertEqual(exp_msg, err.__str__())
