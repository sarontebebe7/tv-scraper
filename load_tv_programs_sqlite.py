import re
from datetime import datetime
from pathlib import Path
import sqlite3

DB_PATH = "tvguide.db"
INPUT_FILES = ["tv_programs_BBC.txt","tv_programs_Disc.txt","tv_programs_NatGeo.txt"]
RECORD_SEP = re.compile(r"^-{3,}\s*$")
KV_LINE     = re.compile(r"^\s*([^:]+)\s*:\s*(.*)\s*$")

DDL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS program_info (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  title         TEXT,
  original_name TEXT,
  prod_year     INTEGER,
  description   TEXT,
  score_pct     INTEGER,
  duration_min  INTEGER,
  channel       TEXT,
  link          TEXT,
  genre         TEXT,
  source_file   TEXT,
  UNIQUE(title, channel)
);

CREATE TABLE IF NOT EXISTS program_schedule (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  program_id    INTEGER,
  day_name      TEXT,
  air_date      TEXT,   -- ISO date string 'YYYY-MM-DD'
  start_time    TEXT,   -- ISO time string 'HH:MM:SS'
  end_time      TEXT,
  viewer_count  INTEGER,
  timestamp     TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(program_id) REFERENCES program_info(id)
);
"""


UPSERT_INFO = """
INSERT INTO program_info
  (title, original_name, prod_year, description, score_pct,
   duration_min, channel, link, genre, source_file)
VALUES
  (:title, :original_name, :prod_year, :description, :score_pct,
   :duration_min, :channel, :link, :genre, :source_file)
ON CONFLICT(title, channel) DO UPDATE SET
  original_name=excluded.original_name,
  prod_year=excluded.prod_year,
  description=excluded.description,
  score_pct=excluded.score_pct,
  duration_min=excluded.duration_min,
  link=excluded.link,
  genre=excluded.genre,
  source_file=excluded.source_file;


"""

INSERT_SCHEDULE = """
INSERT INTO program_schedule
  (program_id, day_name, air_date, start_time, end_time, viewer_count)
VALUES
  (?, ?, ?, ?, ?, NULL);
"""


def parse_file(path: Path):
    items = []
    with path.open("r", encoding="utf-8") as f:
        block = []
        for line in f:
            if RECORD_SEP.match(line):
                if block:
                    rec = parse_block(block, path.name)
                    if rec: items.append(rec)
                    block = []
            else:
                if line.strip():
                    block.append(line.rstrip("\n"))
        if block:
            rec = parse_block(block, path.name)
            if rec: items.append(rec)
    return items

def parse_block(lines, source_file):
    d = {}
    for ln in lines:
        m = KV_LINE.match(ln)
        if m:
            key, val = m.group(1).strip(), m.group(2).strip()
            d[key] = val

    def to_date_str(s):
        if not s: return None
        try:
            return datetime.strptime(s, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None

    def to_time_str(s):
        if not s: return None
        try:
            # normalize to HH:MM:SS
            return datetime.strptime(s, "%H:%M").strftime("%H:%M:%S")
        except ValueError:
            return None

    def first_int(s):
        if not s: return None
        m = re.search(r"\d+", s)
        return int(m.group(0)) if m else None

    return {
        "title":         d.get("Title") or None,
        "day_name":      d.get("Day") or None,
        "air_date":      to_date_str(d.get("Date")),           # TEXT
        "start_time":    to_time_str(d.get("Start Time")),     # TEXT
        "end_time":      to_time_str(d.get("End Time")),       # TEXT
        "duration_min":  first_int(d.get("Duration")),
        "channel":       d.get("Channel") or None,
        "link":          d.get("Link") or None,
        "original_name": d.get("Original Name") or None,
        "prod_year":     first_int(d.get("Year")),
        "description":   d.get("Description") or None,
        "score_pct":     first_int(d.get("Score")),
        "genre":         d.get("Genre") or None,
        "source_file":   source_file,
    }

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA synchronous=NORMAL;")
    for stmt in filter(None, DDL.split(";")):
        s = stmt.strip()
        if s: conn.execute(s + ";")

    for fname in INPUT_FILES:
        p = Path(fname)
        if not p.exists():
            print(f"WARNING: {fname} not found, skipping.")
            continue

        rows = parse_file(p)
        if not rows:
            continue

        with conn:
            for row in rows:
                # Insert or update static info
                conn.execute(UPSERT_INFO, row)

                # Get program_id
                cur = conn.execute("""
                    SELECT id FROM program_info
                    WHERE title=? AND channel=?
                """, (row["title"], row["channel"]))


                result = cur.fetchone()
                if not result:
                    print(f"Missing program_id for {row['title']}")
                    continue
                program_id = result[0]

                # Insert schedule
                conn.execute(INSERT_SCHEDULE, (
                    program_id,
                    row["day_name"],
                    row["air_date"],
                    row["start_time"],
                    row["end_time"]
                ))

    print(f"Data inserted into {DB_PATH}.")
    conn.close()


if __name__ == "__main__":
    main()