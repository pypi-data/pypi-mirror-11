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

from keystoneauth1.exceptions import base


class AuthPluginException(base.ClientException):
    message = "Unknown error with authentication plugins."


class MissingAuthPlugin(AuthPluginException):
    message = "An authenticated request is required but no plugin available."


class NoMatchingPlugin(AuthPluginException):
    """There were no auth plugins that could be created from the parameters
    provided.

    :param str name: The name of the plugin that was attempted to load.

    .. py:attribute:: name

        The name of the plugin that was attempted to load.
    """

    def __init__(self, name):
        self.name = name
        msg = 'The plugin %s could not be found' % name
        super(NoMatchingPlugin, self).__init__(msg)


class UnsupportedParameters(AuthPluginException):
    """A parameter that was provided or returned is not supported.

    :param list(str) names: Names of the unsupported parameters.

    .. py:attribute:: names

        Names of the unsupported parameters.
    """

    def __init__(self, names):
        self.names = names

        m = 'The following parameters were given that are unsupported: %s'
        super(UnsupportedParameters, self).__init__(m % ', '.join(self.names))


class MissingRequiredParameters(AuthPluginException):
    """One or more required parameters were not provided.

    :param string name: Name of the missing parameters.
    :param list(str) parameters: Name of the missing parameters.

    .. py:attribute:: plugin

        Plugin class that was attempted to load.

    .. py:attribute:: parameters

        List of the missing parameters.
    """

    def __init__(self, plugin, parameters):
        self.plugin = plugin
        self.parameters = parameters

        m = ('Auth plugin %(plugin)s requires parameters'
             ' which were not given: %(parameters)s')
        super(UnsupportedParameters, self).__init__(
            m % dict(
                plugin=self.plugin.plugin_class.__name__,
                parameters=', '.join(self.parameters)))
