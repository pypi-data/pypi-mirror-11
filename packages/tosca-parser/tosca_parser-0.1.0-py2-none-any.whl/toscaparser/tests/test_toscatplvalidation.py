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

import os
import six

from toscaparser.common import exception
from toscaparser.nodetemplate import NodeTemplate
from toscaparser.parameters import Input
from toscaparser.parameters import Output
from toscaparser.relationship_template import RelationshipTemplate
from toscaparser.tests.base import TestCase
from toscaparser.tosca_template import ToscaTemplate
import toscaparser.utils.yamlparser


class ToscaTemplateValidationTest(TestCase):

    def test_well_defined_template(self):
        tpl_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/tosca_single_instance_wordpress.yaml")
        self.assertIsNotNone(ToscaTemplate(tpl_path))

    def test_first_level_sections(self):
        tpl_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/test_tosca_top_level_error1.yaml")
        err = self.assertRaises(exception.MissingRequiredFieldError,
                                ToscaTemplate, tpl_path)
        self.assertEqual('Template is missing required field: '
                         '"tosca_definitions_version".', err.__str__())

        tpl_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/test_tosca_top_level_error2.yaml")
        err = self.assertRaises(exception.UnknownFieldError,
                                ToscaTemplate, tpl_path)
        self.assertEqual('Template contain(s) unknown field: '
                         '"node_template", refer to the definition '
                         'to verify valid values.', err.__str__())

    def test_inputs(self):
        tpl_snippet = '''
        inputs:
          cpus:
            type: integer
            description: Number of CPUs for the server.
            constraint:
              - valid_values: [ 1, 2, 4, 8 ]
        '''
        inputs = (toscaparser.utils.yamlparser.
                  simple_parse(tpl_snippet)['inputs'])
        name, attrs = list(inputs.items())[0]
        input = Input(name, attrs)
        try:
            input.validate()
        except Exception as err:
            self.assertTrue(isinstance(err, exception.UnknownFieldError))
            self.assertEqual('Input cpus contain(s) unknown field: '
                             '"constraint", refer to the definition to '
                             'verify valid values.', err.__str__())

    def test_outputs(self):
        tpl_snippet = '''
        outputs:
          server_address:
            description: IP address of server instance.
            values: { get_property: [server, private_address] }
        '''
        outputs = (toscaparser.utils.yamlparser.
                   simple_parse(tpl_snippet)['outputs'])
        name, attrs = list(outputs.items())[0]
        output = Output(name, attrs)
        try:
            output.validate()
        except Exception as err:
            self.assertTrue(
                isinstance(err, exception.MissingRequiredFieldError))
            self.assertEqual('Output server_address is missing required '
                             'field: "value".', err.__str__())

        tpl_snippet = '''
        outputs:
          server_address:
            descriptions: IP address of server instance.
            value: { get_property: [server, private_address] }
        '''
        outputs = (toscaparser.utils.yamlparser.
                   simple_parse(tpl_snippet)['outputs'])
        name, attrs = list(outputs.items())[0]
        output = Output(name, attrs)
        try:
            output.validate()
        except Exception as err:
            self.assertTrue(isinstance(err, exception.UnknownFieldError))
            self.assertEqual('Output server_address contain(s) unknown '
                             'field: "descriptions", refer to the definition '
                             'to verify valid values.',
                             err.__str__())

    def _custom_types(self):
        custom_types = {}
        def_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/custom_types/wordpress.yaml")
        custom_type = toscaparser.utils.yamlparser.load_yaml(def_file)
        node_types = custom_type['node_types']
        for name in node_types:
            defintion = node_types[name]
            custom_types[name] = defintion
        return custom_types

    def _single_node_template_content_test(self, tpl_snippet, expectederror,
                                           expectedmessage):
        nodetemplates = (toscaparser.utils.yamlparser.
                         simple_ordered_parse(tpl_snippet))['node_templates']
        name = list(nodetemplates.keys())[0]
        try:
            nodetemplate = NodeTemplate(name, nodetemplates,
                                        self._custom_types())
            nodetemplate.validate()
            nodetemplate.requirements
            nodetemplate.get_capabilities_objects()
            nodetemplate.get_properties_objects()
            nodetemplate.interfaces

        except Exception as err:
            self.assertTrue(isinstance(err, expectederror))
            self.assertEqual(expectedmessage, err.__str__())

    def test_node_templates(self):
        tpl_snippet = '''
        node_templates:
          server:
            capabilities:
              host:
                properties:
                  disk_size: 10
                  num_cpus: 4
                  mem_size: 4096
              os:
                properties:
                  architecture: x86_64
                  type: Linux
                  distribution: Fedora
                  version: 18.0
        '''
        expectedmessage = ('Template server is missing '
                           'required field: "type".')
        self._single_node_template_content_test(
            tpl_snippet,
            exception.MissingRequiredFieldError,
            expectedmessage)

    def test_node_template_with_wrong_properties_keyname(self):
        """Node template keyname 'properties' given as 'propertiessss'."""
        tpl_snippet = '''
        node_templates:
          mysql_dbms:
            type: tosca.nodes.DBMS
            propertiessss:
              root_password: aaa
              port: 3376
        '''
        expectedmessage = ('Node template mysql_dbms '
                           'contain(s) unknown field: "propertiessss", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_with_wrong_requirements_keyname(self):
        """Node template keyname 'requirements' given as 'requirement'."""
        tpl_snippet = '''
        node_templates:
          mysql_dbms:
            type: tosca.nodes.DBMS
            properties:
              root_password: aaa
              port: 3376
            requirement:
              - host: server
        '''
        expectedmessage = ('Node template mysql_dbms '
                           'contain(s) unknown field: "requirement", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_with_wrong_interfaces_keyname(self):
        """Node template keyname 'interfaces' given as 'interfac'."""
        tpl_snippet = '''
        node_templates:
          mysql_dbms:
            type: tosca.nodes.DBMS
            properties:
              root_password: aaa
              port: 3376
            requirements:
              - host: server
            interfac:
              Standard:
                configure: mysql_database_configure.sh
        '''
        expectedmessage = ('Node template mysql_dbms '
                           'contain(s) unknown field: "interfac", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_with_wrong_capabilities_keyname(self):
        """Node template keyname 'capabilities' given as 'capabilitiis'."""
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            properties:
              db_name: { get_input: db_name }
              db_user: { get_input: db_user }
              db_password: { get_input: db_pwd }
            capabilitiis:
              database_endpoint:
                properties:
                  port: { get_input: db_port }
        '''
        expectedmessage = ('Node template mysql_database '
                           'contain(s) unknown field: "capabilitiis", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_with_wrong_artifacts_keyname(self):
        """Node template keyname 'artifacts' given as 'artifactsss'."""
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            artifactsss:
              db_content:
                implementation: files/my_db_content.txt
                type: tosca.artifacts.File
        '''
        expectedmessage = ('Node template mysql_database '
                           'contain(s) unknown field: "artifactsss", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_with_multiple_wrong_keynames(self):
        """Node templates given with multiple wrong keynames."""
        tpl_snippet = '''
        node_templates:
          mysql_dbms:
            type: tosca.nodes.DBMS
            propertieees:
              root_password: aaa
              port: 3376
            requirements:
              - host: server
            interfacs:
              Standard:
                configure: mysql_database_configure.sh
        '''
        expectedmessage = ('Node template mysql_dbms '
                           'contain(s) unknown field: "propertieees", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            properties:
              name: { get_input: db_name }
              user: { get_input: db_user }
              password: { get_input: db_pwd }
            capabilitiiiies:
              database_endpoint:
              properties:
                port: { get_input: db_port }
            requirementsss:
              - host:
                  node: mysql_dbms
            interfac:
              Standard:
                 configure: mysql_database_configure.sh

        '''
        expectedmessage = ('Node template mysql_database '
                           'contain(s) unknown field: "capabilitiiiies", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_type(self):
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Databases
            properties:
              db_name: { get_input: db_name }
              db_user: { get_input: db_user }
              db_password: { get_input: db_pwd }
            capabilities:
              database_endpoint:
                properties:
                  port: { get_input: db_port }
            requirements:
              - host: mysql_dbms
            interfaces:
              Standard:
                 configure: mysql_database_configure.sh
        '''
        expectedmessage = ('Type "tosca.nodes.Databases" is not '
                           'a valid type.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.InvalidTypeError,
                                                expectedmessage)

    def test_node_template_requirements(self):
        tpl_snippet = '''
        node_templates:
          webserver:
            type: tosca.nodes.WebServer
            requirements:
              host: server
            interfaces:
              Standard:
                create: webserver_install.sh
                start: d.sh
        '''
        expectedmessage = ('Requirements of template webserver '
                           'must be of type: "list".')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.TypeMismatchError,
                                                expectedmessage)

        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            properties:
              db_name: { get_input: db_name }
              db_user: { get_input: db_user }
              db_password: { get_input: db_pwd }
            capabilities:
              database_endpoint:
                properties:
                  port: { get_input: db_port }
            requirements:
              - host: mysql_dbms
              - database_endpoint: mysql_database
            interfaces:
              Standard:
                 configure: mysql_database_configure.sh
        '''
        expectedmessage = ('Requirements of template mysql_database '
                           'contain(s) unknown field: "database_endpoint", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_requirements_with_wrong_node_keyname(self):
        """Node template requirements keyname 'node' given as 'nodes'."""
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            requirements:
              - host:
                  nodes: mysql_dbms

        '''
        expectedmessage = ('Requirements of template mysql_database '
                           'contain(s) unknown field: "nodes", refer to the '
                           'definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_requirements_with_wrong_capability_keyname(self):
        """Incorrect node template requirements keyname

        Node template requirements keyname 'capability' given as
        'capabilityy'.
        """
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            requirements:
              - host:
                  node: mysql_dbms
              - log_endpoint:
                  node: logstash
                  capabilityy: log_endpoint
                  relationship:
                    type: tosca.relationships.ConnectsTo

        '''
        expectedmessage = ('Requirements of template mysql_database '
                           'contain(s) unknown field: "capabilityy", refer to '
                           'the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_requirements_with_wrong_relationship_keyname(self):
        """Incorrect node template requirements keyname

        Node template requirements keyname 'relationship' given as
        'relationshipppp'.
        """
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            requirements:
              - host:
                  node: mysql_dbms
              - log_endpoint:
                  node: logstash
                  capability: log_endpoint
                  relationshipppp:
                    type: tosca.relationships.ConnectsTo

        '''
        expectedmessage = ('Requirements of template mysql_database '
                           'contain(s) unknown field: "relationshipppp", refer'
                           ' to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_requirements_with_multiple_wrong_keynames(self):
        """Node templates given with multiple wrong requirements keynames."""
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            requirements:
              - host:
                  node: mysql_dbms
              - log_endpoint:
                  nod: logstash
                  capabilit: log_endpoint
                  relationshipppp:
                    type: tosca.relationships.ConnectsTo

        '''
        expectedmessage = ('Requirements of template mysql_database '
                           'contain(s) unknown field: "nod", refer'
                           ' to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            requirements:
              - host:
                  node: mysql_dbms
              - log_endpoint:
                  node: logstash
                  capabilit: log_endpoint
                  relationshipppp:
                    type: tosca.relationships.ConnectsTo

        '''
        expectedmessage = ('Requirements of template mysql_database '
                           'contain(s) unknown field: "capabilit", refer'
                           ' to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_capabilities(self):
        tpl_snippet = '''
        node_templates:
          mysql_database:
            type: tosca.nodes.Database
            properties:
              db_name: { get_input: db_name }
              db_user: { get_input: db_user }
              db_password: { get_input: db_pwd }
            capabilities:
              http_endpoint:
                properties:
                  port: { get_input: db_port }
            requirements:
              - host: mysql_dbms
            interfaces:
              Standard:
                 configure: mysql_database_configure.sh
        '''
        expectedmessage = ('Capabilities of template mysql_database '
                           'contain(s) unknown field: "http_endpoint", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_properties(self):
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.Compute
            properties:
              os_image: F18_x86_64
            capabilities:
              host:
                properties:
                  disk_size: 10 GB
                  num_cpus: { get_input: cpus }
                  mem_size: 4096 MB
              os:
                properties:
                  architecture: x86_64
                  type: Linux
                  distribution: Fedora
                  version: 18.0
        '''
        expectedmessage = ('Properties of template server contain(s) '
                           'unknown field: "os_image", refer to the '
                           'definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_node_template_interfaces(self):
        tpl_snippet = '''
        node_templates:
          wordpress:
            type: tosca.nodes.WebApplication.WordPress
            requirements:
              - host: webserver
              - database_endpoint: mysql_database
            interfaces:
              Standards:
                 create: wordpress_install.sh
                 configure:
                   implementation: wordpress_configure.sh
                   inputs:
                     wp_db_name: { get_property: [ mysql_database, db_name ] }
                     wp_db_user: { get_property: [ mysql_database, db_user ] }
                     wp_db_password: { get_property: [ mysql_database, \
                     db_password ] }
                     wp_db_port: { get_property: [ SELF, \
                     database_endpoint, port ] }
        '''
        expectedmessage = ('Interfaces of template wordpress '
                           'contain(s) unknown field: '
                           '"Standards", '
                           'refer to the definition to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

        tpl_snippet = '''
        node_templates:
          wordpress:
            type: tosca.nodes.WebApplication.WordPress
            requirements:
              - host: webserver
              - database_endpoint: mysql_database
            interfaces:
              Standard:
                 create: wordpress_install.sh
                 config:
                   implementation: wordpress_configure.sh
                   inputs:
                     wp_db_name: { get_property: [ mysql_database, db_name ] }
                     wp_db_user: { get_property: [ mysql_database, db_user ] }
                     wp_db_password: { get_property: [ mysql_database, \
                     db_password ] }
                     wp_db_port: { get_property: [ SELF, \
                     database_endpoint, port ] }
        '''
        expectedmessage = ('Interfaces of template wordpress contain(s) '
                           'unknown field: "config", refer to the definition'
                           ' to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

        tpl_snippet = '''
        node_templates:
          wordpress:
            type: tosca.nodes.WebApplication.WordPress
            requirements:
              - host: webserver
              - database_endpoint: mysql_database
            interfaces:
              Standard:
                 create: wordpress_install.sh
                 configure:
                   implementation: wordpress_configure.sh
                   inputs:
                     wp_db_name: { get_property: [ mysql_database, db_name ] }
                     wp_db_user: { get_property: [ mysql_database, db_user ] }
                     wp_db_password: { get_property: [ mysql_database, \
                     db_password ] }
                     wp_db_port: { get_ref_property: [ database_endpoint, \
                     database_endpoint, port ] }
        '''
        expectedmessage = ('Interfaces of template wordpress contain(s) '
                           'unknown field: "inputs", refer to the definition'
                           ' to verify valid values.')
        self._single_node_template_content_test(tpl_snippet,
                                                exception.UnknownFieldError,
                                                expectedmessage)

    def test_relationship_template_properties(self):
        tpl_snippet = '''
        relationship_templates:
            storage_attachto:
                type: AttachesTo
                properties:
                  device: test_device
        '''
        expectedmessage = ('Properties of template '
                           'storage_attachto is missing required field: '
                           '"[\'location\']".')
        self._single_rel_template_content_test(
            tpl_snippet,
            exception.MissingRequiredFieldError,
            expectedmessage)

    def _single_rel_template_content_test(self, tpl_snippet, expectederror,
                                          expectedmessage):
        rel_template = (toscaparser.utils.yamlparser.
                        simple_parse(tpl_snippet))['relationship_templates']
        name = list(rel_template.keys())[0]
        rel_template = RelationshipTemplate(rel_template[name], name)
        err = self.assertRaises(expectederror, rel_template.validate)
        self.assertEqual(expectedmessage, six.text_type(err))

    def test_invalid_template_version(self):
        tosca_tpl = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/test_invalid_template_version.yaml")
        err = self.assertRaises(exception.InvalidTemplateVersion,
                                ToscaTemplate, tosca_tpl)
        valid_versions = ', '.join(ToscaTemplate.VALID_TEMPLATE_VERSIONS)
        ex_err_msg = ('The template version "tosca_xyz" is invalid. '
                      'The valid versions are: "%s"' % valid_versions)
        self.assertEqual(six.text_type(err), ex_err_msg)

    def test_node_template_capabilities_properties(self):
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.Compute
            capabilities:
              host:
                properties:
                  disk_size: 10 GB
                  num_cpus: { get_input: cpus }
                  mem_size: 4096 MB
              os:
                properties:
                  architecture: x86_64
                  type: Linux
                  distribution: Fedora
                  version: 18.0
              scalable:
                properties:
                  min_instances: 1
                  default_instances: 5
        '''
        expectedmessage = ('Properties of template server is missing '
                           'required field: '
                           '"[\'max_instances\']".')

        self._single_node_template_content_test(
            tpl_snippet,
            exception.MissingRequiredFieldError,
            expectedmessage)

        # validatating capability property values
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.WebServer
            capabilities:
              data_endpoint:
                properties:
                  initiator: test
        '''
        expectedmessage = ('initiator: test is not an valid value '
                           '"[source, target, peer]".')

        self._single_node_template_content_test(
            tpl_snippet,
            exception.ValidationError,
            expectedmessage)

        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.Compute
            capabilities:
              host:
                properties:
                  disk_size: 10 GB
                  num_cpus: { get_input: cpus }
                  mem_size: 4096 MB
              os:
                properties:
                  architecture: x86_64
                  type: Linux
                  distribution: Fedora
                  version: 18.0
              scalable:
                properties:
                  min_instances: 1
                  max_instances: 3
                  default_instances: 5
        '''
        expectedmessage = ('Properties of template server : '
                           'default_instances value is not between'
                           ' min_instances and max_instances')

        self._single_node_template_content_test(
            tpl_snippet,
            exception.ValidationError,
            expectedmessage)

    def test_node_template_objectstorage_without_required_property(self):
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.ObjectStorage
            properties:
              maxsize: 1 GB
        '''
        expectedmessage = ('Properties of template server is missing '
                           'required field: '
                           '"[\'name\']".')

        self._single_node_template_content_test(
            tpl_snippet,
            exception.MissingRequiredFieldError,
            expectedmessage)

    def test_node_template_objectstorage_with_invalid_scalar_unit(self):
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.ObjectStorage
            properties:
              name: test
              maxsize: -1
        '''
        expectedmessage = ('"-1" is not a valid scalar-unit')
        self._single_node_template_content_test(
            tpl_snippet,
            ValueError,
            expectedmessage)

    def test_node_template_objectstorage_with_invalid_scalar_type(self):
        tpl_snippet = '''
        node_templates:
          server:
            type: tosca.nodes.ObjectStorage
            properties:
              name: test
              maxsize: 1 XB
        '''
        expectedmessage = ('"1 XB" is not a valid scalar-unit')
        self._single_node_template_content_test(
            tpl_snippet,
            ValueError,
            expectedmessage)
