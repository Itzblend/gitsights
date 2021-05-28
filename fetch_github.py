import json
import os
import requests
from requests.utils import requote_uri
from functools import partial
import config
from enum import Enum
import shutil
import re
import queue
from collections import namedtuple
import itertools


def _set_config():
    conf = config.get_config()

    global BASEURL
    BASEURL = conf.git_config["baseurl"]

    global ORGANIZATION
    ORGANIZATION = 'Shy-Boys-Club'

    global reg_get_auth

    reg_get_auth = partial(requests.get, auth=('huhta.lauri@gmail.com', ''))


def _get_org_url():
    return requote_uri(f'{BASEURL}/orgs/{ORGANIZATION}')



def _get_org_events_url():
    return requote_uri(f'{BASEURL}/orgs/{ORGANIZATION}/events')

def _get_org_members_url():
    return requote_uri(f'{BASEURL}/orgs/{ORGANIZATION}/members')

def _get_files_url(repo: str):
    return requote_uri(f'{BASEURL}/repos/{ORGANIZATION}/{repo}/contents')

def _get_contents_url(repo: str, code_file: str):
    return requote_uri(f'{BASEURL}/repos/{ORGANIZATION}/{repo}/contents/{code_file}')

def _get_file_commits_url(repo: str, code_file: str):
    return requote_uri(f'{BASEURL}/repos/{ORGANIZATION}/{repo}/commits?path={code_file}&ref=main')

def _get_commits_branch_url(repo: str, branch: str):
    return requote_uri(f'{BASEURL}/repos/{ORGANIZATION}/{repo}/commits')#?sha={branch}')



def _get_api_results(url):

    resp = reg_get_auth(url)

    return resp.text, resp.headers, resp.links


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


# ------------------------------------------

def fetch_contents(repo_folder: str, save_folder: str):
    """ Get metainfo from repository.json file and fetch contents of a repository
    """
    os.makedirs(save_folder, exist_ok=False)
    # Collect repo files
    repo_files = []
    for dirpath, _, files in os.walk(repo_folder):
        for filename in files:
            repo_files.append(os.path.join(dirpath, filename))

    for file in repo_files:
        with open(file, 'r') as filer:
            repo_data = json.load(filer)

        repo_names = [repo["name"] for repo in repo_data]

        # Collect files and filenames
        for repo in repo_names:
            print(f"Fetching contents for repository: {repo}")
            os.makedirs(f'{save_folder}/{repo}', exist_ok=False)
            os.makedirs(f'{save_folder}/{repo}/commits', exist_ok=False)

            url = _get_files_url(repo=repo)
            resp = reg_get_auth(url)
            data = json.loads(resp.text)

            code_files = [(code_file["path"], code_file["type"], code_file["url"]) for code_file in data]

            _contents_queue(code_files=code_files,save_folder=save_folder, repo=repo)

            get_commits_branch(save_folder=save_folder, repo=repo)



def _contents_queue(code_files, save_folder, repo):

    [q.put(file) for file in code_files]

    while not q.empty():
        item = q.get()

        path = item[0]
        type = item[1]
        url = item[2]

        if type == 'file':
            _file_processor(path, type, url, save_folder, repo)
        else:
            _folder_processor(path, type, url, save_folder, repo)



def _file_processor(path, type, url, save_folder, repo):

    resp, headers, links = _get_api_results(url)
    data = json.loads(resp)
    data["repository"] = repo

    with open(os.path.join(save_folder, repo, path + '.json'), 'w') as output_file:
        json.dump(data, output_file)

    _get_file_commits(path, type, url, save_folder, repo)

def _folder_processor(path, type, url, save_folder, repo):

    resp, headers, links = _get_api_results(url)
    data = json.loads(resp)
    code_files = []
    for code_file in data:
        temp_path = code_file["path"].split('/')
        temp_path.pop()
        temp_path = '/'.join(temp_path)
        os.makedirs(os.path.join(save_folder, repo, temp_path), exist_ok=True)
        os.makedirs(os.path.join(save_folder, repo, 'commits', temp_path), exist_ok=True)

        code_files.append((code_file["path"], code_file["type"], code_file["url"]))


    [q.put(file) for file in code_files]


def _get_file_commits(path, type, url, save_folder, repo):

    url = _get_file_commits_url(repo, path)
    resp, headers, links = _get_api_results(url)
    data = json.loads(resp)
    for commit in data:
        _get_commit_data(url=commit["url"], save_folder=save_folder, repo=repo, path=path)



def _get_commit_data(url, save_folder, repo, path):

    resp, headers, links = _get_api_results(url)
    data = json.loads(resp)
    data["repository"] = repo


    with open(os.path.join(save_folder, repo, 'commits', path + '.json'), 'a') as output_file:
        json.dump(data, output_file)
        output_file.write('\n')



def get_commits_branch(save_folder, repo):

    

    branch = 'main'
    #repo = 'dotties'

    os.makedirs(os.path.join(save_folder, repo, 'commits_branch', branch), exist_ok=True)

    url = _get_commits_branch_url(repo=repo, branch=branch)

    for i in itertools.count():
        resp, headers, links = _get_api_results(url)
        data = json.loads(resp)

        for entry in data:
            entry["repository"] = repo

        print(links)


        with open(os.path.join(save_folder, repo, 'commits_branch', branch, f'data_{i}.json'), 'w') as output_file:
            json.dump(data, output_file)
            output_file.write('\n')


        if links["next"]["url"] is None:
            with open(os.path.join(save_folder, repo, 'commits_branch', branch, f'data_{i}.json'), 'w') as output_file:
                json.dump(data, output_file)
                output_file.write('\n')
            break
    


    



        




















if __name__ == '__main__':

    endpoints = ["repos", "events", "issues", "hooks", "members"]

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

    contents_folder_prefix = os.path.join(data_folder_prefix, 'contents')
    # repositories drill down
    q = queue.Queue()
    fetch_contents(repo_folder=repository_folder_prefix, save_folder=contents_folder_prefix)
