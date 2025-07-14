import requests
import psycopg2
from utils.env_loader import load_env

url = "https://remoteok.com/api"


def fetch_jobs():
    url = "https://remoteok.com/api"
    remoteok = requests.get(url)

    # run if api connect
    if remoteok.status_code == 200:
        # remove the warning
        return remoteok.json()[1:]
    else:
        return RuntimeError(f"ERRO: API remoteok, {remoteok.status_code}")


def filter_python(jobs):
    return [j for j in jobs if 'python' in [tag.lower() for tag in j.get("tags", [])]]


def get_conn():
    database_info = load_env()
    return psycopg2.connect(
        database=database_info["db_name"],
        user=database_info["user"],
        password=database_info["password"],
        host=database_info["host"])


def insert_jobs(conn, jobs):
    with conn, conn.cursor() as cur:
        for v in jobs:
            cur.execute("""
                INSERT INTO JOB 
                (title, company, location, description, date_of_publication, salary, remote, url, position, tags, 
                source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (company, position, date_of_publication) DO NOTHING
            """, (
                v["slug"],
                v["company"],
                v["location"],
                v["description"],
                v["date"],
                v.get("salary_min", 0),
                True,
                v["apply_url"],
                v["position"],
                v.get("tags", []),
                "remoteok"
            ))

    conn.commit()


jobs = fetch_jobs()
jobs_python = filter_python(jobs)
insert_jobs(get_conn(), jobs)
