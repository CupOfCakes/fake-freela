import pytest
import psycopg2
from requests_mock import Mocker
from src import scrap_remoteok

SAMPLE_JOB = {
    "id": 1,
    "slug": "python-dev-1",
    "company": "Acme",
    "position": "Python Dev",
    "tags": ["Python", "Django"],
    "location": "Worldwide",
    "description": "Very cool job",
    "date": "2025-07-05",
    "salary_min": 5000,
    "apply_url": "https://acme.jobs/123",
}

@pytest.fixture
def remoteok_mock():
    with Mocker() as m:
        m.get(scrap_remoteok.url, json=[{"legal": "don't abuse"}, SAMPLE_JOB])
        yield


@pytest.fixture(scope="function")
def pg_conn():
    conn = psycopg2.connect(
        dbname="testdb",
        user="testuser",
        password="testpass",
        host="localhost",
        port=5433,  # cuidado com o número!
    )
    yield conn
    conn.rollback()  # desfaz tudo pra manter isolado
    conn.close()
