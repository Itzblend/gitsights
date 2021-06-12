import json
import config
import click
from utils import db_cursor, format_query
import os
from io import StringIO


@click.group()
def main():
    """
    Entrypoint for Gitsights database
    """
    _set_config()


def _set_config():
    conf = config.get_config()

    dbname = conf.db_settings['dbname']
    dbuser = conf.db_settings['dbuser']
    dbhost = conf.db_settings['dbhost']
    dbpassword = conf.db_settings['password']
    dbport = conf.db_settings['port']

    global CONNECTION_STRING
    CONNECTION_STRING = f'dbname={dbname} user={dbuser} host={dbhost} password={dbpassword} port={dbport}'

    global SQL_CONFIG
    SQL_CONFIG = conf.sql_config


@main.command()
def init_db():
    with db_cursor(CONNECTION_STRING) as cur:
        cur.execute(f"""
                    DROP SCHEMA {SQL_CONFIG['SCHEMA_TABLES']} CASCADE;
                    CREATE SCHEMA IF NOT EXISTS {SQL_CONFIG['SCHEMA_TABLES']};
                    CREATE SCHEMA IF NOT EXISTS {SQL_CONFIG['SCHEMA']};
                """)
        cur.execute(format_query('sql/organizations_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/repositories_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/commits_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/contents_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/events_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/issues_t.sql', SQL_CONFIG))


def _load_git_data(file: str, load_script: str):


    with open(file, 'r', encoding='utf8') as insertion_file:
        data = json.load(insertion_file)


        insertion_data_row_by_row = [json.dumps(row) for row in data]
        insertion_data = StringIO('\n'.join(insertion_data_row_by_row))

        with db_cursor(CONNECTION_STRING) as cur:
            cur.execute('CREATE TEMP TABLE staging(data JSON) ON COMMIT DROP;')
            cur.copy_expert("COPY staging FROM STDIN WITH CSV quote e'\x01' delimiter e'\x02'", insertion_data)
            cur.execute(format_query(load_script, SQL_CONFIG))


def _load_org_data(file: str, load_script: str):
    with open(file, 'r', encoding='utf8') as insertion_file:
        insertion_data = insertion_file

        with db_cursor(CONNECTION_STRING) as cur:
            cur.execute('CREATE TEMP TABLE staging(data JSON) ON COMMIT DROP;')
            cur.copy_expert("COPY staging FROM STDIN WITH CSV quote e'\x01' delimiter e'\x02'", insertion_data)
            cur.execute(format_query(load_script, SQL_CONFIG))



@main.command()
@click.option('--data_dir', default='data')
def upload_git_dirs(data_dir: str):
    data_files = []

    for dirpath, _, files in os.walk(data_dir):
        for filename in files:
            data_files.append(os.path.join(dirpath, filename))

    for file in data_files:
        identifier = file.split('/')[1]
        print(file)
        if identifier == 'organization':
            load_script = 'sql/load_organizations.sql'
            _load_org_data(file, load_script)
        if identifier == 'repositories':
            load_script = 'sql/load_repositories.sql'
            _load_git_data(file, load_script)
        if identifier == 'events':
            load_script = 'sql/load_events.sql'
            _load_git_data(file, load_script)
        if identifier == 'issues':
            load_script = 'sql/load_issues.sql'
            _load_git_data(file, load_script)
#        if identifier == 'contents' and 'commits' not in file.split('/'):
#            load_script = 'sql/load_contents.sql'
#            _load_org_data(file, load_script)
#        if identifier == 'contents' and 'commits' in file.split('/'):
#            load_script = 'sql/load_commits.sql'
#            _load_org_data(file, load_script)
        if identifier == 'contents' and 'commits_branch' in file.split('/'):
            load_script = 'sql/load_commits.sql'
            _load_org_data(file, load_script)

        else:
            print("invalid data")
            continue


if __name__ == '__main__':
    main()
    #_set_config()
    #upload_git_dirs()
    #TODO: Maybe remove the first load commit and find better if statement for load contents
