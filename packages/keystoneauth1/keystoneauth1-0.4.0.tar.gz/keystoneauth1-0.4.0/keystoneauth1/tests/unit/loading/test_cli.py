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

import argparse
import uuid

import fixtures
import mock

from keystoneauth1 import loading
from keystoneauth1 import plugin
from keystoneauth1.tests.unit.auth import utils


class TesterPlugin(plugin.BaseAuthPlugin):

    def get_token(self, *args, **kwargs):
        return None


class TesterLoader(loading.BaseLoader):

    @property
    def plugin_class(self):
        return TesterPlugin

    def get_options(self):
        # NOTE(jamielennox): this is kind of horrible. If you specify this as
        # a deprecated_name= value it will convert - to _ which is not what we
        # want for a CLI option.
        deprecated = [loading.Opt('test-other')]
        return [
            loading.Opt('test-opt', help='tester', deprecated=deprecated)
        ]


class CliTests(utils.TestCase):

    def setUp(self):
        super(CliTests, self).setUp()
        self.p = argparse.ArgumentParser()

    def env(self, name, value=None):
        if value is not None:
            # environment variables are always strings
            value = str(value)

        return self.useFixture(fixtures.EnvironmentVariable(name, value))

    def test_creating_with_no_args(self):
        ret = loading.register_argparse_arguments(self.p, [])
        self.assertIsNone(ret)
        self.assertIn('--os-auth-plugin', self.p.format_usage())

    def test_load_with_nothing(self):
        loading.register_argparse_arguments(self.p, [])
        opts = self.p.parse_args([])
        self.assertIsNone(loading.load_from_argparse_arguments(opts))

    @utils.mock_plugin
    def test_basic_params_added(self, m):
        name = uuid.uuid4().hex
        argv = ['--os-auth-plugin', name]
        ret = loading.register_argparse_arguments(self.p, argv)
        self.assertIsInstance(ret, utils.MockLoader)

        for n in ('--os-a-int', '--os-a-bool', '--os-a-float'):
            self.assertIn(n, self.p.format_usage())

        m.assert_called_once_with(name)

    @utils.mock_plugin
    def test_param_loading(self, m):
        name = uuid.uuid4().hex
        argv = ['--os-auth-plugin', name,
                '--os-a-int', str(self.a_int),
                '--os-a-float', str(self.a_float),
                '--os-a-bool', str(self.a_bool)]

        klass = loading.register_argparse_arguments(self.p, argv)
        self.assertIsInstance(klass, utils.MockLoader)

        opts = self.p.parse_args(argv)
        self.assertEqual(name, opts.os_auth_plugin)

        a = loading.load_from_argparse_arguments(opts)
        self.assertTestVals(a)

        self.assertEqual(name, opts.os_auth_plugin)
        self.assertEqual(str(self.a_int), opts.os_a_int)
        self.assertEqual(str(self.a_float), opts.os_a_float)
        self.assertEqual(str(self.a_bool), opts.os_a_bool)

    @utils.mock_plugin
    def test_default_options(self, m):
        name = uuid.uuid4().hex
        argv = ['--os-auth-plugin', name,
                '--os-a-float', str(self.a_float)]

        klass = loading.register_argparse_arguments(self.p, argv)
        self.assertIsInstance(klass, utils.MockLoader)

        opts = self.p.parse_args(argv)
        self.assertEqual(name, opts.os_auth_plugin)

        a = loading.load_from_argparse_arguments(opts)

        self.assertEqual(self.a_float, a['a_float'])
        self.assertEqual(3, a['a_int'])

    @utils.mock_plugin
    def test_with_default_string_value(self, m):
        name = uuid.uuid4().hex
        klass = loading.register_argparse_arguments(self.p, [], default=name)
        self.assertIsInstance(klass, utils.MockLoader)
        m.assert_called_once_with(name)

    @utils.mock_plugin
    def test_overrides_default_string_value(self, m):
        name = uuid.uuid4().hex
        default = uuid.uuid4().hex
        argv = ['--os-auth-plugin', name]
        klass = loading.register_argparse_arguments(self.p,
                                                    argv,
                                                    default=default)
        self.assertIsInstance(klass, utils.MockLoader)
        m.assert_called_once_with(name)

    @utils.mock_plugin
    def test_with_default_type_value(self, m):
        klass = loading.register_argparse_arguments(self.p,
                                                    [],
                                                    default=utils.MockLoader())
        self.assertIsInstance(klass, utils.MockLoader)
        self.assertEqual(0, m.call_count)

    @utils.mock_plugin
    def test_overrides_default_type_value(self, m):
        # using this test plugin would fail if called because there
        # is no get_options() function
        class TestLoader(object):
            pass
        name = uuid.uuid4().hex
        argv = ['--os-auth-plugin', name]
        klass = loading.register_argparse_arguments(self.p,
                                                    argv,
                                                    default=TestLoader)
        self.assertIsInstance(klass, utils.MockLoader)
        m.assert_called_once_with(name)

    @utils.mock_plugin
    def test_env_overrides_default_opt(self, m):
        name = uuid.uuid4().hex
        val = uuid.uuid4().hex
        self.env('OS_A_STR', val)

        klass = loading.register_argparse_arguments(self.p, [], default=name)
        opts = self.p.parse_args([])
        a = klass.load_from_argparse_arguments(opts)

        self.assertEqual(val, a['a_str'])

    def test_deprecated_cli_options(self):
        TesterLoader().register_argparse_arguments(self.p)
        val = uuid.uuid4().hex
        opts = self.p.parse_args(['--os-test-other', val])
        self.assertEqual(val, opts.os_test_opt)

    def test_deprecated_multi_cli_options(self):
        TesterLoader().register_argparse_arguments(self.p)
        val1 = uuid.uuid4().hex
        val2 = uuid.uuid4().hex
        # argarse rules say that the last specified wins.
        opts = self.p.parse_args(['--os-test-other', val2,
                                  '--os-test-opt', val1])
        self.assertEqual(val1, opts.os_test_opt)

    def test_deprecated_env_options(self):
        val = uuid.uuid4().hex

        with mock.patch.dict('os.environ', {'OS_TEST_OTHER': val}):
            TesterLoader().register_argparse_arguments(self.p)

        opts = self.p.parse_args([])
        self.assertEqual(val, opts.os_test_opt)

    def test_deprecated_env_multi_options(self):
        val1 = uuid.uuid4().hex
        val2 = uuid.uuid4().hex

        with mock.patch.dict('os.environ', {'OS_TEST_OPT': val1,
                                            'OS_TEST_OTHER': val2}):
            TesterLoader().register_argparse_arguments(self.p)

        opts = self.p.parse_args([])
        self.assertEqual(val1, opts.os_test_opt)
