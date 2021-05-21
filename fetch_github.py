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


def fetch_data(endpoint: str, save_folder: str, url = ''):
    """
    Prosessor to get data from all the github endpoints listed.
    HOX! When calling this function, do not use both endpoint and url arguements
    """
    os.makedirs(save_folder, exist_ok=False)

    if endpoint:
        data_url = ORG_DATA[f'{endpoint}_url']

    if url:
        data_url = url

    resp = reg_get_auth(data_url)
    data = json.loads(resp.text)

    with open(f'{save_folder}/{ORGANIZATION}_{endpoint}.json', 'w') as data_file:
        json.dump(data, data_file)

    return data


def fetch_org(save_folder: str):
    os.makedirs(save_folder, exist_ok=False)

    url = _get_org_url()
    resp = reg_get_auth(url)
    data = json.loads(resp.text)

    with open(f'{save_folder}/{ORGANIZATION}_org.json', 'w') as org_file:
        json.dump(data, org_file)



if __name__ == '__main__':

    endpoints = ["repos", "events", "issues", "hooks", "members"]

    data_folder_prefix = 'data'
    data_folder_prefix = os.path.join(data_folder_prefix)
    shutil.rmtree(data_folder_prefix, ignore_errors=True)
    os.makedirs(data_folder_prefix, exist_ok=False)
    # Data folders
    global data_folders
    data_folders = {}
    for endpoint in endpoints:
        data_folders[endpoint] = os.path.join(data_folder_prefix, f'{endpoint}')


    _set_config()


    org_folder_prefix = os.path.join(data_folder_prefix, 'organization')
    fetch_org(save_folder=org_folder_prefix)
    # Reference org file
    org_file = os.path.join(org_folder_prefix, f'{ORGANIZATION}_org.json')
    global ORG_DATA
    with open(org_file, 'r') as temp_org_file:
        ORG_DATA = json.loads(temp_org_file.read())

    for endpoint in data_folders:
        data = fetch_data(endpoint=endpoint, save_folder=data_folders[endpoint])
        if endpoint == 'repos' and data:
            repo_endpoints_list = ["contents", "git_tags"]
            #repos_sub_endpoints = data
            for repo_endpoint in repo_endpoints_list:
                print(data[f'{repo_endpoint}_url'])
                fetch_data(url=data[repo_endpoint], save_folder=f'{data_folder_prefix}/{repo_endpoint}')



    #fetch_repositories(save_folder=repository_folder_prefix)
    #fetch_events(save_folder=events_folder_prefix)
    #fetch_issues(save_folder=issues_folder_prefix)