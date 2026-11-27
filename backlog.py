"""Report open tickets by queue at the end of a given day."""
import argparse
import csv
import sqlite3
import sys
from contextlib import closing
from datetime import date
from pathlib import Path

FIELDS = ["ticket", "queue", "opened", "closed"]
QUERY = """
SELECT queue, COUNT(*), MAX(CAST(julianday(?) - julianday(opened) AS INTEGER))
FROM tickets
WHERE opened <= ? AND (closed IS NULL OR closed > ?)
GROUP BY queue ORDER BY queue
"""


def calendar_day(value):
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("use YYYY-MM-DD")
    return value


def snapshot(stream, cutoff):
    calendar_day(cutoff)
    reader = csv.reader(stream, strict=True)
    if next(reader, None) != FIELDS:
        raise ValueError("expected header: " + ",".join(FIELDS))
    with closing(sqlite3.connect(":memory:")) as db:
        db.execute("CREATE TABLE tickets(ticket TEXT PRIMARY KEY, queue TEXT, opened TEXT, closed TEXT)")
        for row in reader:
            try:
                ticket, queue, opened, closed = (field.strip() for field in row)
                calendar_day(opened)
                if closed:
                    calendar_day(closed)
                if not ticket or not queue or (closed and closed < opened):
                    raise ValueError("missing identifier or reversed dates")
                db.execute("INSERT INTO tickets VALUES (?, ?, ?, ?)", (ticket, queue, opened, closed or None))
            except (ValueError, sqlite3.IntegrityError) as error:
                raise ValueError(f"line {reader.line_num}: {error}") from error
        return db.execute(QUERY, (cutoff,) * 3).fetchall()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("cutoff")
    args = parser.parse_args()
    try:
        with args.csv_file.open(encoding="utf-8-sig", newline="") as stream:
            rows = snapshot(stream, args.cutoff)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"backlog: {error}\n")
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["queue", "open_tickets", "oldest_days"])
    writer.writerows(rows)


if __name__ == "__main__":
    main()
