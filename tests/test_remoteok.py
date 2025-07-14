import pytest
from src import scrap_remoteok
from test_conftest import remoteok_mock, pg_conn
import logging
import psycopg2

logging.basicConfig(level=logging.INFO)


def test_connection():
    try:
        conn = scrap_remoteok.get_conn()
        conn.close()
        logging.info("Conexão OK.")
        return True
    except psycopg2.OperationalError as e:
        logging.error("Falha na conexão com o banco de dados.")
        logging.error(str(e))
        return False


def test_fetch_ok(remoteok_mock):
    jobs = scrap_remoteok.fetch_jobs()
    assert jobs and jobs[0]["company"] == "Acme"


def test_filter_python(remoteok_mock):
    jobs = scrap_remoteok.fetch_jobs()
    py_jobs = scrap_remoteok.filter_python(jobs)
    assert len(py_jobs) == 1
    assert py_jobs[0]["slug"] == "python-dev-1"

@pytest.mark.skip(reason="test postgre in windows is a shit")
def test_insert_unique(pg_conn, remoteok_mock):
    cur = pg_conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS job""")
    cur.execute("""
        CREATE TABLE job (
          id serial primary key,
          title text, company text, location text, description text,
          date_of_publication date, salary numeric,
          remote boolean, url text unique,
          position text, tags text[], source text
        )
    """)
    pg_conn.commit()

    scrap_remoteok.insert_jobs(pg_conn, scrap_remoteok.filter_python(scrap_remoteok.fetch_jobs()))

    cur.execute("SELECT count(*) FROM job")
    assert cur.fetchone()[0] == 1
