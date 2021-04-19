from contextlib import contextmanager
from typing import Dict
import psycopg2
import logging


@contextmanager
def db_cursor(connection_string: str):
    # Wrapper for db connection
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except psycopg2.DatabaseError:
        logging.error('Error in database operations: ', exc_info=True, stack_info=True)
        raise
    finally:
        cur.close()
        conn.close()


def format_query(filename: str, kwargs: Dict[str, str]) -> str:

    with open(filename, 'r') as file:
        query = file.read()

    return query.format(**kwargs)