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
        for line in fr:
            entry = json.loads(line)
            word = entry.pop("word")
            if ' ' in word:
                # TODO should these be ignored really?
                continue
            raw_definitions = []
            for sense in entry['senses']:
                if 'raw_glosses' in sense:
                    raw_definitions += sense['raw_glosses']
            if len(raw_definitions) == 0:
                if 'etymology_text' in entry:
                    raw_definitions.append(entry['etymology_text'])
            if word in rows:
                rows[word] += raw_definitions
            else:
                rows[word] = raw_definitions

    with connection:
        connection.executemany(
            """INSERT INTO words(word, entries)
                VALUES(?,?)""",
            ((word, json.dumps(entries)) for word, entries in rows.items()),
        )
