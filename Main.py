import os
from pathlib import Path

import psycopg
import certifi
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)

print("ENV file exists:", env_path.exists())



def print_table(cursor, max_width=50):
    columns = [col.name for col in cursor.description]
    rows = cursor.fetchall()

    if not rows:
        print("No results found.")
        return

    # Convert values to strings
    data = [
        [str(value) if value is not None else "" for value in row]
        for row in rows
    ]

    # Calculate column widths
    widths = [
        min(max(len(columns[i]), *(len(row[i]) for row in data)), max_width)
        for i in range(len(columns))
    ]

    def format_row(row):
        return "| " + " | ".join(
            value[:width - 3] + "..." if len(value) > width
            else value.ljust(width)
            for value, width in zip(row, widths)
        ) + " |"

    separator = "+-" + "-+-".join("-" * w for w in widths) + "-+"

    print(separator)
    print(format_row(columns))
    print(separator)

    for row in data:
        print(format_row(row))

    print(separator)
    print(f"{len(rows)} rows returned.")


with psycopg.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        sslmode="verify-full",
        sslrootcert=certifi.where(),
        connect_timeout=10,
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, name
            FROM recipe
            ORDER BY name;
        """)

        print_table(cursor)

