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
                    CREATE SCHEMA IF NOT EXISTS {SQL_CONFIG['SCHEMA_TABLES']};
                    CREATE SCHEMA IF NOT EXISTS {SQL_CONFIG['SCHEMA']};
                """)
        cur.execute(format_query('sql/organizations_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/repositories_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/commits_t.sql', SQL_CONFIG))
        cur.execute(format_query('sql/contents_t.sql', SQL_CONFIG))


def _load_git_data(file: str, load_script: str):
    def _insert(insertion_data):
        with db_cursor(CONNECTION_STRING) as cur:
            cur.execute('CREATE TEMP TABLE staging(data JSON) ON COMMIT DROP;')
            cur.copy_expert("COPY staging FROM STDIN WITH CSV quote e'\x01' delimiter e'\x02'", insertion_data)
            cur.execute(format_query(load_script, SQL_CONFIG))

    with open(file, 'r', encoding='utf8') as insertion_file:
        print(type(insertion_file))
        insertion_data = json.load(insertion_file)

        if type(insertion_data) is list:
            insertion_data_row_by_row = [json.dumps(row) for row in insertion_data]
            insertion_data = StringIO('\n'.join(insertion_data_row_by_row))
            _insert(insertion_data)

        elif type(insertion_data) is dict:

            insertion_data = insertion_file
            _insert(insertion_data)




@main.command()
@click.option('--data_dir', default='data')
def upload_git_dirs(data_dir: str):
    data_files = []

    for dirpath, _, files in os.walk(data_dir):
        for filename in files:
            data_files.append(os.path.join(dirpath, filename))

    for file in data_files:
        identifier = file.split('/')[1]
        print(identifier)
        if identifier == 'organization':
            load_script = 'sql/load_organizations.sql'
        elif identifier == 'repositories':
            load_script = 'sql/load_repositories.sql'
        if identifier == 'events':
            load_script = 'sql/load_events.sql'
        else:
            print("invalid data")
            continue

        _load_git_data(file, load_script)


if __name__ == '__main__':
    #main()
    _set_config()
    upload_git_dirs()