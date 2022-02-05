# coding: utf-8

import json
import os
import requests
from requests.auth import HTTPBasicAuth

SLACK_CHANNEL = os.environ['slackChannel']
SLACK_WEBHOOK_URL = os.environ['slackWebhookUrl']
TOGGL_API = os.environ['togglApi']
TOGGL_API_TOKEN = os.environ['togglApiToken']

cache = {}


def lambda_handler(event, context):
    '''
    Main Lambda function

    :param event: <dict> AWS Cloudwatch Scheduled Event
    :param context: <object> AWS running context

    :return: None
    '''

    entry = current_entry()

    if entry['data'] is None:
        print('Not tracking, so skip post.')
    else:
        global cache
        if 'last_id' in cache and cache['last_id'] == entry['data']['id']:
            print('The entry is the same as the previous one, so skip post.')
        else:
            cache['last_id'] = entry['data']['id']
            project = convert_pid(entry['data'])
            message = create_message(entry['data'], project)
            post_message(message)

    print(event)


def current_entry():
    '''
    Get current Toggl entry

    :return: <object>
    '''

    r = requests.get('{api}/time_entries/current'.format(api=TOGGL_API),
                     auth=HTTPBasicAuth(TOGGL_API_TOKEN, 'api_token'),
                     headers={'Content-Type': 'application/json'})

    return r.json()


def convert_pid(data):
    '''
    Convert pid to project name

    :param data: <object> Toggl entry response

    :return: <str>
    '''

    if 'pid' in data:
        r = requests.get('{api}/projects/{pid}'.format(api=TOGGL_API,
                                                       pid=data['pid']),
                         auth=HTTPBasicAuth(TOGGL_API_TOKEN, 'api_token'),
                         headers={'Content-Type': 'application/json'})

        project = r.json()
        pname = project['data']['name']
    else:
        pname = 'No Project'

    return pname


def create_message(data, project):
    '''
    Create a message to post

    :param data: <object> Toggl entry response
    :param project: <str> Project name

    :return: <str>
    '''

    if 'tags' in data:
        message = 'It seems to be in the {tag} of {prj}.'.format(
            prj=project, tag=', '.join(data['tags']))
    else:
        message = 'It seems to be in the work of {prj}.'.format(prj=project)

    return message


def post_message(message):
    '''
    Post a message to Slack

    :param message: <str> message to post

    :return: <int>
    '''

    params = {'channel': SLACK_CHANNEL, 'text': message}

    r = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(params),
                      headers={'Content-Type': 'application/json'})

    return r.status_code
