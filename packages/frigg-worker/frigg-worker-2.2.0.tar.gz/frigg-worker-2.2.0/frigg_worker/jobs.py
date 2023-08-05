# -*- coding: utf8 -*-
import json
import logging
import os

import requests

from frigg_worker.build_helpers import build_settings, cached_property

from . import api

logger = logging.getLogger(__name__)


class Result(object):
    log = ''
    return_code = None
    succeeded = None
    task = None
    pending = None

    def __init__(self, task):
        self.task = task
        self.pending = True

    def update_result(self, result):
        self.succeeded = result.succeeded
        self.return_code = result.return_code
        self.log = result.out
        self.pending = False

    def update_error(self, error):
        self.log = error
        self.succeeded = False
        self.pending = False

    @classmethod
    def serialize(cls, obj):
        if isinstance(obj, dict):
            return obj
        return obj.__dict__


class Job(object):
    MAIN_TASKS_KEY = 'tasks'

    id = ''
    results = None
    cloned = False
    branch = 'master'
    sha = None
    clone_url = None
    name = None
    owner = None
    pull_request_id = None
    coverage = None
    finished = False
    worker_host = None

    def __init__(self, build_id, obj, docker, worker_options=None):
        self.__dict__.update(obj)
        self.id = build_id
        self.results = {}
        self.tasks = []
        self.setup_tasks = []
        self.setup_results = {}
        self.finished = False
        self.docker = docker
        self.worker_options = worker_options
        if worker_options:
            self.api = api.APIWrapper(worker_options)
            if 'worker_host' in worker_options:
                self.worker_host = worker_options['worker_host']

    @property
    def working_directory(self):
        return os.path.join('~/builds', str(self.id))

    @property
    def succeeded(self):
        for key in self.results:
            if self.results[key].succeeded is False:
                return False
        return True

    @cached_property
    def settings(self):
        return build_settings(self.working_directory, self.docker)

    def clone_repo(self, depth=10):
        depth_string = ''
        if depth > 0:
            depth_string = '--depth={0}'.format(depth)
        if self.pull_request_id is None:
            command = (
                'git clone {depth} --branch={build.branch} {build.clone_url} '
                '{build.working_directory}'
            )
        else:
            command = (
                'git clone {depth} {build.clone_url} {build.working_directory} && '
                'cd {build.working_directory} && '
                'git fetch origin pull/{build.pull_request_id}/head:pull-{build.pull_request_id} &&'
                ' git checkout pull-{build.pull_request_id}'
            )

        command += (
            ' && cd {build.working_directory}'
            ' && git reset --hard {build.sha}'
        )

        clone = self.docker.run(command.format(build=self, depth=depth_string))
        if not clone.succeeded:
            if 'Could not parse object \'{0}\''.format(self.sha) in clone.out:
                logger.warning('Could not checkout commit', extra={'build': self.serializer(self)})
                self.delete_working_dir()
                if depth > 0:
                    return self.clone_repo(depth=0)
                return False
            message = 'Access denied to {build.owner}/{build.name}'.format(build=self)
            logger.error(message, extra={'stdout': clone.out, 'stderr': clone.err})
        return clone.succeeded

    def start_services(self):
        for service in self.settings['services']:
            if not self.docker.run('sudo service {0} start'.format(service)).succeeded:
                logger.warning('Service "{0}" did not start.'.format(service))

    def run_task(self, task_command):
        run_result = self.docker.run(task_command, self.working_directory)
        self.results[task_command].update_result(run_result)

    def run_setup_task(self, task_command):
        run_result = self.docker.run(task_command, self.working_directory)
        self.setup_results[task_command].update_result(run_result)

    def create_pending_tasks(self):
        """
        Creates pending task results in a dict on self.result with task string as key. It will also
        create a list on self.tasks that is used to make sure the serialization of the results
        creates a correctly ordered list.
        """
        for task in self.settings['setup_tasks']:
            self.setup_tasks.append(task)
            self.setup_results[task] = Result(task)

        for task in self.settings[self.MAIN_TASKS_KEY]:
            self.tasks.append(task)
            self.results[task] = Result(task)

    def delete_working_dir(self):
        if self.docker.directory_exist(self.working_directory):
            self.docker.run('rm -rf {build.working_directory}'.format(build=self))

    def error(self, task, message):
        self.errored = True
        if task in self.results:
            self.results[task].update_error(message)
        else:
            result = Result(task)
            result.update_error(message)
            self.tasks.append(task)
            self.results[task] = result

    def report_run(self):

        try:
            return self.api.report_run(
                type(self).__name__,
                self.id,
                json.dumps(self, default=self.serializer)
            ).status_code
        except requests.exceptions.ConnectionError as e:
            logger.exception(e)
            return 500

    @classmethod
    def serializer(cls, obj):
        out = {}
        if isinstance(obj, Job):
            unwanted = ['worker_options', 'api', 'docker']
            for key in obj.__dict__.keys():
                if key not in unwanted:
                    out[key] = obj.__dict__[key]

            out['setup_results'] = [Result.serialize(obj.setup_results[key])
                                    for key in obj.setup_tasks]

            out['results'] = [Result.serialize(obj.results[key])
                              for key in obj.tasks]

            try:
                out['settings'] = obj.settings
            except RuntimeError:
                pass

        return out
