import json
import os
import requests
from requests.utils import requote_uri
from functools import partial
import config
import shutil


def _set_config():
    conf = config.get_config()

    global BASEURL
    BASEURL = conf.git_config["baseurl"]

    global ORGANIZATION
    ORGANIZATION = 'Shy-Boys-Club'

    global reg_get_auth
    reg_get_auth = partial(requests.get, auth=(conf.git_config["user"], conf.git_config["api_token"]))


def _get_org_url():
    return requote_uri(f'{BASEURL}/orgs/{ORGANIZATION}')

def _get_org_repos_url():
    return requote_uri(f'{BASEURL}/orgs/{ORGANIZATION}/repos')


def _get_org_events_url():
    return requote_uri(f'{BASEURL}/orgs/{ORGANIZATION}/events')

def _get_org_members_url():
    return requote_uri(f'{BASEURL}/orgs/{ORGANIZATION}/members')


#def fetch


def fetch_events(save_folder: str):
    os.makedirs(save_folder, exist_ok=False)

    events_url = ORG_DATA["events_url"]
    resp = reg_get_auth(events_url)
    data = json.loads(resp.text)

    with open(f'{save_folder}/{ORGANIZATION}_events.json', 'w') as events_file:
        json.dump(data, events_file)



def fetch_repositories(save_folder: str):
    os.makedirs(save_folder, exist_ok=False)


    repository_url = ORG_DATA["repos_url"]
    resp = reg_get_auth(repository_url)
    data = json.loads(resp.text)

    with open(f'{save_folder}/{ORGANIZATION}_repositories.json', 'w') as repository_file:
        json.dump(data, repository_file)



def fetch_org(save_folder: str):
    os.makedirs(save_folder, exist_ok=False)

    url = _get_org_url()
    resp = reg_get_auth(url)
    data = json.loads(resp.text)

    with open(f'{save_folder}/{ORGANIZATION}_org.json', 'w') as org_file:
        json.dump(data, org_file)



if __name__ == '__main__':
    data_folder_prefix = 'data'
    data_folder_prefix = os.path.join(data_folder_prefix)
    shutil.rmtree(data_folder_prefix, ignore_errors=True)
    os.makedirs(data_folder_prefix, exist_ok=False)
    # Data folders
    org_folder_prefix = os.path.join(data_folder_prefix, 'organization')
    repository_folder_prefix = os.path.join(data_folder_prefix, 'repositories')
    events_folder_prefix = os.path.join(data_folder_prefix, 'events')


    _set_config()


    fetch_org(save_folder=org_folder_prefix)
    # Reference org file
    org_file = os.path.join(org_folder_prefix, f'{ORGANIZATION}_org.json')
    global ORG_DATA
    with open(org_file, 'r') as temp_org_file:
        ORG_DATA = json.loads(temp_org_file.read())

    fetch_repositories(save_folder=repository_folder_prefix)
    fetch_events(save_folder=events_folder_prefix)