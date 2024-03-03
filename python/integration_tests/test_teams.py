import httpx
import psycopg
from psycopg.rows import namedtuple_row



def test_add_team():
    # Reset the db
    url = "http://127.0.0.1:8000/reset_db"
    response = httpx.post(url, follow_redirects=True)
    response.raise_for_status()

    # Create a new team named 'devs'
    url = "http://127.0.0.1:8000/add_team"
    response = httpx.post(url, follow_redirects=True, data={"name": "devs"})
    response.raise_for_status()

    # Check that the team is in the db
    database_url = "postgresql://hr:hr@localhost:5433/hr"
    connection = psycopg.connect(database_url)
    with connection.cursor() as cursor:
        cursor.row_factory = namedtuple_row
        rows = cursor.execute("SELECT name FROM hr_team").fetchall()
        team_names = [row.name for row in rows]
        assert team_names == ['devs']
