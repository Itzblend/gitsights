import json
from collections import namedtuple
import os
import requests
from requests.auth import HTTPBasicAuth


def get_config():

    github_vault_resp = requests.get(f'{os.environ.get("VAULT_ADDR")}/v1/kv/github', headers={'X-Vault-Token': os.environ.get("VAULT_TOKEN")})
    github_vault_config = json.loads(github_vault_resp.text)

    postgres_vault_resp = requests.get(f'{os.environ.get("VAULT_ADDR")}/v1/kv/postgres', headers={'X-Vault-Token': os.environ.get("VAULT_TOKEN")})
    postgres_vault_config = json.loads(postgres_vault_resp.text)

    git_config = {
        "baseurl": "https://api.github.com",
        "user": "huhta.lauri@gmail.com",
        "api_token": github_vault_config["data"]["api_token"]
    }

    db_settings = {
        'dbhost': postgres_vault_config["data"]["dbhost"],
        'dbname': 'gitsights',
        'dbuser': postgres_vault_config["data"]["dbuser"],
        'password': postgres_vault_config["data"]["password"],
        'port': postgres_vault_config["data"]["port"]
    }

    schema = 'git'
    schema_t = f'{schema}_t'

    sql_config = {
        'SCHEMA': schema,
        'SCHEMA_TABLES': schema_t,
        'ORGANIZATION_T': f'{schema_t}.organizations_t',
        'ORGANIZATION_V': f'{schema}.organizations',
        'REPOSITORIES_T': f'{schema_t}.repositories_t',
        'REPOSITORIES_V': f'{schema}.repositories',
        'EVENTS_T': f'{schema_t}.events_t',
        'EVENTS_V': f'{schema}.events'
    }


    conf = namedtuple('conf', ['git_config', 'db_settings', 'sql_config'])

    return conf(git_config=git_config, db_settings=db_settings, sql_config=sql_config)