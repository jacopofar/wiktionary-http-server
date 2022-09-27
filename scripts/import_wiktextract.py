import json
import sqlite3
from sys import argv

if __name__ == "__main__":
    connection = sqlite3.connect(argv[2])
    connection.execute(
        """CREATE TABLE words(
            word TEXT PRIMARY KEY,
            entries TEXT
        )"""
    )
    with open(argv[1]) as fr:
        rows = {}
        for idx, line in enumerate(fr):
            if idx % 100_000 == 0:
                print(f'Read {idx} lines')
            entry = json.loads(line)
            word = entry.pop("word")
            if word in rows:
                rows[word].append(entry)
            else:
                rows[word] = [entry]
    print('All definitions loaded, now writing to the DB')
    with connection:
        connection.executemany(
            """INSERT INTO words(word, entries)
                VALUES(?,?)""",
            ((word, json.dumps(entries)) for word, entries in rows.items()),
        )
