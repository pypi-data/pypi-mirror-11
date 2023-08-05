# -*- coding: utf8 -*-
import json
import logging
import random
import socket
import time

import requests
from docker.manager import Docker

from .builds import Build
from .deployments import Deployment

logger = logging.getLogger(__name__)


def fetch_builds(**options):
    notify_of_upstart(options)
    while options['dispatcher_url']:
        task = fetch_task(options['dispatcher_url'], options['dispatcher_token'])
        if task:
            start_build(task, options)

        time.sleep(5.0 + random.randint(1, 100) / 100)


def fetch_deployments(**options):
    notify_of_upstart(options)
    while options['dispatcher_url']:
        task = fetch_task(options['dispatcher_url'], options['dispatcher_token'])
        if task:
            start_deployment(task, options)

        time.sleep(5.0 + random.randint(1, 100) / 100)


def start_build(task, options):
    docker_options = {
        'image': options['docker_image'],
        'combine_outputs': True,
        'privilege': True,
        'env_variables': {'CI': 'frigg'},
        'name_prefix': 'build'
    }
    with Docker(**docker_options) as docker:
        try:
            build = Build(task['id'], task, docker=docker, worker_options=options)
            logger.info('Starting {0}'.format(task))
            build.run_tests()
        except Exception as e:
            logger.exception(e)


def start_deployment(task, options):
    docker_options = {
        'image': task['image'],
        'timeout': task['ttl'],
        'combine_outputs': True,
        'privilege': True,
        'ports_mapping': ['{port}:8000'.format(**task)],
        'name_prefix': 'preview'
    }
    docker = Docker(**docker_options)
    docker.start()
    try:
        deployment = Deployment(task['id'], task, docker=docker, worker_options=options)
        deployment.run_deploy()
    except Exception as e:
        docker.stop()
        raise e


def fetch_task(dispatcher_url, dispatcher_token):
    logger.debug('Fetching new job from {0}'.format(dispatcher_url))
    try:
        response = requests.get(
            dispatcher_url,
            headers={
                'x-frigg-worker-token': dispatcher_token
            }
        )

        if response.status_code == 200:
            return response.json()['job']
    except requests.exceptions.ConnectionError as e:
        logger.exception(e)

    time.sleep(20)


def notify_of_upstart(options):
    if options['slack_url']:
        host = socket.gethostname()
        requests.post(options['slack_url'], json.dumps({
            'icon_emoji': options['slack_icon'],
            'channel': options['slack_channel'],
            'text': 'I just started on host {host}, looking for work now...'.format(host=host),
            'username': 'frigg-worker',
        }))
