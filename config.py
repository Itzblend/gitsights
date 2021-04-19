import json
from collections import namedtuple
import os


def get_config():

    git_config = {
        "baseurl": "https://api.github.com",
        "user": "huhta.lauri@gmail.com",
        "api_token": os.popen("vault kv get -field=api_token kv/github"),
    }

    db_settings = {
        'dbhost': os.popen("vault kv get -field=dbhost kv/postgres").read(),
        'dbname': 'gitsights',
        'dbuser': os.popen("vault kv get -field=dbuser kv/postgres").read(),
        'password': os.popen("vault kv get -field=password kv/postgres").read(),
        'port': os.popen("vault kv get -field=port kv/postgres").read()
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