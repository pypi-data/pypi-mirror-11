"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals

import json
import os

from atomic_reactor.build import InsideBuilder
from atomic_reactor.util import ImageName
from atomic_reactor.plugin import (PreBuildPlugin, PrePublishPlugin, PostBuildPlugin, ExitPlugin,
                                   AutoRebuildCanceledException)
from atomic_reactor.plugin import PluginFailedException
import atomic_reactor.plugin
import logging
from flexmock import flexmock
import pytest
from tests.constants import MOCK_SOURCE, SOURCE
from tests.docker_mock import mock_docker
import inspect

from atomic_reactor.inner import BuildResults, BuildResultsEncoder, BuildResultsJSONDecoder
from atomic_reactor.inner import DockerBuildWorkflow


BUILD_RESULTS_ATTRS = ['build_logs',
                       'built_img_inspect',
                       'built_img_info',
                       'base_img_info',
                       'base_plugins_output',
                       'built_img_plugins_output']


def test_build_results_encoder():
    results = BuildResults()
    expected_data = {}
    for attr in BUILD_RESULTS_ATTRS:
        setattr(results, attr, attr)
        expected_data[attr] = attr

    data = json.loads(json.dumps(results, cls=BuildResultsEncoder))
    assert data == expected_data


def test_build_results_decoder():
    data = {}
    expected_results = BuildResults()
    for attr in BUILD_RESULTS_ATTRS:
        setattr(expected_results, attr, attr)
        data[attr] = attr

    results = json.loads(json.dumps(data), cls=BuildResultsJSONDecoder)
    for attr in set(BUILD_RESULTS_ATTRS) - set(['build_logs']):
        assert getattr(results, attr) == getattr(expected_results, attr)


class MockDockerTasker(object):
    def inspect_image(self, name):
        return {}


class X(object):
    pass


class MockInsideBuilder(object):
    def __init__(self):
        self.tasker = MockDockerTasker()
        self.base_image = ImageName(repo='Fedora', tag='22')
        self.image_id = 'asd'

    @property
    def source(self):
        result = X()
        setattr(result, 'dockerfile_path', '/')
        setattr(result, 'path', '/tmp')
        return result

    def pull_base_image(self, source_registry, insecure=False):
        pass

    def build(self):
        result = X()
        setattr(result, 'logs', None)
        setattr(result, 'is_failed', lambda: False)
        return result

    def inspect_built_image(self):
        return None


class RaisesMixIn(object):
    """
    Mix-in class for plugins that should raise exceptions.
    """

    can_fail = False

    def __init__(self, tasker, workflow, *args, **kwargs):
        super(RaisesMixIn, self).__init__(tasker, workflow,
                                          *args, **kwargs)

    def run(self):
        raise RuntimeError


class PreRaises(RaisesMixIn, PreBuildPlugin):
    """
    This plugin must run and cause the build to abort.
    """

    key = 'pre_raises'


class WatchedMixIn(object):
    """
    Mix-in class for plugins we want to watch.
    """

    def __init__(self, tasker, workflow, watcher, *args, **kwargs):
        super(WatchedMixIn, self).__init__(tasker, workflow,
                                           *args, **kwargs)
        self.watcher = watcher

    def run(self):
        self.watcher.call()


class PreWatched(WatchedMixIn, PreBuildPlugin):
    """
    A PreBuild plugin we can watch.
    """

    key = 'pre_watched'


class PrePubWatched(WatchedMixIn, PrePublishPlugin):
    """
    A PrePublish plugin we can watch.
    """

    key = 'prepub_watched'


class PostWatched(WatchedMixIn, PostBuildPlugin):
    """
    A PostBuild plugin we can watch.
    """

    key = 'post_watched'


class ExitWatched(WatchedMixIn, ExitPlugin):
    """
    An Exit plugin we can watch.
    """

    key = 'exit_watched'


class ExitRaises(RaisesMixIn, ExitPlugin):
    """
    An Exit plugin that should raise an exception.
    """

    key = 'exit_raises'


class ExitCompat(WatchedMixIn, ExitPlugin):
    """
    An Exit plugin called as a Post-build plugin.
    """

    key = 'store_logs_to_file'


class Watcher(object):
    def __init__(self):
        self.called = False

    def call(self):
        self.called = True

    def was_called(self):
        return self.called


def test_workflow():
    """
    Test normal workflow.
    """

    this_file = inspect.getfile(PreWatched)
    mock_docker()
    fake_builder = MockInsideBuilder()
    flexmock(InsideBuilder).new_instances(fake_builder)
    watch_pre = Watcher()
    watch_prepub = Watcher()
    watch_post = Watcher()
    watch_exit = Watcher()
    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image',
                                   prebuild_plugins=[{'name': 'pre_watched',
                                                      'args': {
                                                          'watcher': watch_pre
                                                      }}],
                                   postbuild_plugins=[{'name': 'post_watched',
                                                       'args': {
                                                           'watcher': watch_post
                                                       }}],
                                   prepublish_plugins=[{'name': 'prepub_watched',
                                                        'args': {
                                                            'watcher': watch_prepub,
                                                        }}],
                                   exit_plugins=[{'name': 'exit_watched',
                                                  'args': {
                                                      'watcher': watch_exit
                                                  }}],
                                   plugin_files=[this_file])

    workflow.build_docker_image()

    assert watch_pre.was_called()
    assert watch_prepub.was_called()
    assert watch_post.was_called()
    assert watch_exit.was_called()


class FakeLogger(object):
    def __init__(self):
        self.debugs = []
        self.infos = []
        self.warnings = []
        self.errors = []

    def log(self, logs, args):
        logs.append(args)

    def debug(self, *args):
        self.log(self.debugs, args)

    def info(self, *args):
        self.log(self.infos, args)

    def warning(self, *args):
        self.log(self.warnings, args)

    def error(self, *args):
        self.log(self.errors, args)


def test_workflow_compat():
    """
    Some of our plugins have changed from being run post-build to
    being run at exit. Let's test what happens when we try running an
    exit plugin as a post-build plugin.
    """

    this_file = inspect.getfile(PreWatched)
    mock_docker()
    fake_builder = MockInsideBuilder()
    flexmock(InsideBuilder).new_instances(fake_builder)
    watch_exit = Watcher()
    fake_logger = FakeLogger()
    atomic_reactor.plugin.logger = fake_logger
    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image',
                                   postbuild_plugins=[{'name': 'store_logs_to_file',
                                                       'args': {
                                                           'watcher': watch_exit
                                                       }}],
                                   plugin_files=[this_file])

    workflow.build_docker_image()
    assert watch_exit.was_called()
    assert len(fake_logger.errors) > 0


class Pre(PreBuildPlugin):
    """
    This plugin does nothing. It's only used for configuration testing.
    """

    key = 'pre'


class Post(PostBuildPlugin):
    """
    This plugin does nothing. It's only used for configuration testing.
    """

    key = 'post'


class Exit(ExitPlugin):
    """
    This plugin does nothing. It's only used for configuration testing.
    """

    key = 'exit'


@pytest.mark.parametrize(('plugins', 'should_fail', 'should_log'), [
    # No 'name' key, prebuild
    ({
        'prebuild_plugins': [{'args': {}},
                             {'name': 'pre_watched',
                              'args': {
                                  'watcher': Watcher(),
                              }
                             }],
      },
     True,  # is fatal
     True,  # logs error
    ),

    # No 'name' key, postbuild
    ({
        'postbuild_plugins': [{'args': {}},
                              {'name': 'post_watched',
                               'args': {
                                   'watcher': Watcher(),
                               }
                              }],
      },
     True,  # is fatal
     True,  # logs error
    ),

    # No 'name' key, exit
    ({
        'exit_plugins': [{'args': {}},
                         {'name': 'exit_watched',
                          'args': {
                              'watcher': Watcher(),
                          }
                         }],
      },
     False,  # not fatal
     True,   # logs error
    ),

    # No 'args' key, prebuild
    ({'prebuild_plugins': [{'name': 'pre'},
                           {'name': 'pre_watched',
                            'args': {
                                'watcher': Watcher(),
                            }
                           }]},
     False,  # not fatal
     False,  # no error logged
    ),

    # No 'args' key, postbuild
    ({'postbuild_plugins': [{'name': 'post'},
                            {'name': 'post_watched',
                             'args': {
                                 'watcher': Watcher(),
                             }
                            }]},
     False,  # not fatal,
     False,  # no error logged
    ),

    # No 'args' key, exit
    ({'exit_plugins': [{'name': 'exit'},
                       {'name': 'exit_watched',
                        'args': {
                            'watcher': Watcher(),
                        }
                       }]},
     False,  # not fatal
     False,  # no error logged
    ),

    # No such plugin, prebuild
    ({'prebuild_plugins': [{'name': 'no plugin',
                            'args': {}},
                           {'name': 'pre_watched',
                            'args': {
                                'watcher': Watcher(),
                            }
                           }]},
     True,  # is fatal
     True,  # logs error
    ),

    # No such plugin, postbuild
    ({'postbuild_plugins': [{'name': 'no plugin',
                             'args': {}},
                            {'name': 'post_watched',
                             'args': {
                                 'watcher': Watcher(),
                             }
                            }]},
     True,  # is fatal
     True,  # logs error
    ),

    # No such plugin, exit
    ({'exit_plugins': [{'name': 'no plugin',
                        'args': {}},
                       {'name': 'exit_watched',
                        'args': {
                            'watcher': Watcher(),
                        }
                       }]},
     False,  # not fatal
     True,   # logs error
    ),
])
def test_plugin_errors(plugins, should_fail, should_log):
    """
    Try bad plugin configuration.
    """

    this_file = inspect.getfile(PreRaises)
    mock_docker()
    fake_builder = MockInsideBuilder()
    flexmock(InsideBuilder).new_instances(fake_builder)
    fake_logger = FakeLogger()
    atomic_reactor.plugin.logger = fake_logger

    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image',
                                   plugin_files=[this_file],
                                   **plugins)

    # Find the 'watcher' parameter
    watchers = [conf.get('args', {}).get('watcher')
                for plugin in plugins.values()
                for conf in plugin]
    watcher = [x for x in watchers if x][0]

    if should_fail:
        with pytest.raises(PluginFailedException):
            workflow.build_docker_image()

        assert not watcher.was_called()
    else:
        workflow.build_docker_image()
        assert watcher.was_called()

    if should_log:
        assert len(fake_logger.errors) > 0
    else:
        assert len(fake_logger.errors) == 0


class StopAutorebuildPlugin(PreBuildPlugin):
    key = 'stopstopstop'

    def run(self):
        raise AutoRebuildCanceledException(self.key, 'message')


def test_autorebuild_stop_prevents_build():
    """
    test that a plugin that raises AutoRebuildCanceledException results in actually skipped build
    """
    this_file = inspect.getfile(PreWatched)
    mock_docker()
    fake_builder = MockInsideBuilder()
    flexmock(InsideBuilder).new_instances(fake_builder)
    watch_prepub = Watcher()
    watch_post = Watcher()
    watch_exit = Watcher()
    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image',
                                   prebuild_plugins=[{'name': 'stopstopstop',
                                                      'args': {
                                                      }}],
                                   postbuild_plugins=[{'name': 'post_watched',
                                                       'args': {
                                                           'watcher': watch_post
                                                       }}],
                                   prepublish_plugins=[{'name': 'prepub_watched',
                                                        'args': {
                                                            'watcher': watch_prepub,
                                                        }}],
                                   exit_plugins=[{'name': 'exit_watched',
                                                  'args': {
                                                      'watcher': watch_exit
                                                  }}],
                                   plugin_files=[this_file])

    with pytest.raises(AutoRebuildCanceledException):
        workflow.build_docker_image()

    assert not watch_prepub.was_called()
    assert not watch_post.was_called()
    assert watch_exit.was_called()
    assert workflow.autorebuild_canceled == True


def test_workflow_errors():
    """
    This is a test for what happens when plugins fail.

    When a prebuild or postbuild plugin fails, and doesn't have
    can_fail=True set, the whole build should fail. However, all the
    exit plugins should run.
    """

    this_file = inspect.getfile(PreRaises)
    mock_docker()
    fake_builder = MockInsideBuilder()
    flexmock(InsideBuilder).new_instances(fake_builder)
    watch_pre = Watcher()
    watch_post = Watcher()
    watch_exit = Watcher()
    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image',
                                   prebuild_plugins=[{'name': 'pre_raises',
                                                      'args': {}},
                                                     {'name': 'pre_watched',
                                                      'args': {
                                                          'watcher': watch_pre
                                                      }}],
                                   postbuild_plugins=[{'name': 'post_watched',
                                                       'args': {
                                                           'watcher': watch_post
                                                       }}],
                                   exit_plugins=[{'name': 'exit_raises',
                                                  'args': {}
                                                  },
                                                 {'name': 'exit_watched',
                                                  'args': {
                                                      'watcher': watch_exit
                                                  }}],
                                   plugin_files=[this_file])

    with pytest.raises(PluginFailedException):
        workflow.build_docker_image()

    # A pre-build plugin caused the build to fail, so post-build
    # plugins should not run.
    assert not watch_post.was_called()

    # But all exit plugins should run, even if one of them also raises
    # an exception.
    assert watch_exit.was_called()

    # Other than exit plugins, any unexpected plugin failure stops the
    # whole build immediately.
    assert not watch_pre.was_called()


class ExitUsesSource(ExitWatched):
    key = 'uses_source'

    def run(self):
        assert os.path.exists(self.workflow.source.get_dockerfile_path()[0])
        WatchedMixIn.run(self)


def test_source_not_removed_for_exit_plugins():
    this_file = inspect.getfile(PreRaises)
    mock_docker()
    fake_builder = MockInsideBuilder()
    flexmock(InsideBuilder).new_instances(fake_builder)
    watch_exit = Watcher()
    workflow = DockerBuildWorkflow(SOURCE, 'test-image',
                                   exit_plugins=[{'name': 'uses_source',
                                                  'args': {
                                                      'watcher': watch_exit,
                                                  }}],
                                   plugin_files=[this_file])

    workflow.build_docker_image()

    # Make sure that the plugin was actually run
    assert watch_exit.was_called()
