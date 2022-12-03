import httpx
import sqlite3


def reset_db():
    url = "http://127.0.0.1:8000/reset_db"
    response = httpx.post(url, follow_redirects=True)
    response.raise_for_status()


def test_add_team():
    reset_db()
    url = "http://127.0.0.1:8000/add_team"
    response = httpx.post(url, follow_redirects=True, data={"name": "devs"})
    response.raise_for_status()
    db = sqlite3.connect("../../../backend/db.sqlite3")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    rows = cursor.execute("SELECT name FROM hr_team").fetchall()
    teams_names = [x["name"] for x in rows]
    assert teams_names == ["devs"]
