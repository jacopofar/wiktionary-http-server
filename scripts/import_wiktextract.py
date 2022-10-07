import json
import sqlite3
from sys import argv

PARTITIONS = 6

if __name__ == "__main__":
    connection = sqlite3.connect(argv[2])
    connection.execute(
        """CREATE TABLE words(
            word TEXT PRIMARY KEY,
            entries TEXT
        )"""
    )
    for p in range(PARTITIONS):
        print(f"Processing partition {p}")
        with open(argv[1]) as fr:
            rows: dict[str, list] = {}
            for idx, line in enumerate(fr):
                if idx % 400_000 == 0:
                    print(
                        f"Read {idx} lines, {len(rows)} pending rows [partition {p}/{PARTITIONS}]"
                    )
                entry = json.loads(line)
                word = entry.pop("word")
                if hash(word) % PARTITIONS != p:
                    continue
                if word in rows:
                    rows[word].append(entry)
                else:
                    rows[word] = [entry]
        print(
            f"All definitions for partition {p}/{PARTITIONS} loaded, now writing to the DB"
        )
        with connection:
            connection.executemany(
                """INSERT INTO words(word, entries)
                    VALUES(?,?)""",
                ((word, json.dumps(entries)) for word, entries in rows.items()),
            )
