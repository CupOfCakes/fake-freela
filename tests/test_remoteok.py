from src import scrap_remoteok
import psycopg2


def test_fetch_ok(remoteok_mock):
    jobs = scrap_remoteok.fetch_jobs()
    assert jobs and jobs[0]["company"] == "Acme"


def test_filter_python(remoteok_mock):
    jobs = scrap_remoteok.fetch_jobs()
    py_jobs = scrap_remoteok.filter_python(jobs)
    assert len(py_jobs) == 1
    assert py_jobs[0]["slug"] == "python-dev-1"


def test_insert_unique(postgresql, remoteok_mock):
    """postgresql fixture fornece DSN de banco temporário"""
    conn = psycopg2.connect(**postgresql.dsn())
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE job (
          id serial primary key,
          title text, company text, location text, description text,
          date_of_publication date, salary numeric,
          remote boolean, url text unique,
          position text, tags text[], source text
        )
    """)
    scrap_remoteok.insert_jobs(conn, scrap_remoteok.filter_python(scrap_remoteok.fetch_jobs()))
    cur.execute("SELECT count(*) FROM job")
    assert cur.fetchone()[0] == 1