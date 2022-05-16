import json
import sqlite3
from sys import argv

if __name__ == "__main__":
    connection = sqlite3.connect("dict.db")
    connection.execute(
        """CREATE TABLE words(
            word TEXT PRIMARY KEY,
            entries TEXT
        )"""
    )
    with open(argv[1]) as fr:
        rows = {}
        for line in fr:
            entry = json.loads(line)
            word = entry.pop("word")
            if word in rows:
                rows[word].append(entry)
            else:
                rows[word] = [entry]

    with connection:
        connection.executemany(
            """INSERT INTO words(word, entries)
                VALUES(?,?)""",
            ((word, json.dumps(entries)) for word, entries in rows.items()),
        )
