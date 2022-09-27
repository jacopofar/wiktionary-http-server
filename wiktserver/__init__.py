from multiprocessing import connection
import sqlite3

from ujson import loads
from sanic import Sanic
from sanic.response import json
from sanic import exceptions

app = Sanic("wiktionary_app")
app.ctx.connection = sqlite3.connect("dict.db")
app.ctx.cur = app.ctx.connection.cursor()


@app.get("/w/<word:str>")
async def test(_request, word: str):
    entries = app.ctx.cur.execute(
            "SELECT entries from words where word = ?", (word,)
        ).fetchone()

    if entries is None:
        raise exceptions.NotFound(f'Cannot find {word}')
    else:
        return json(loads(entries[0]))


if __name__ == "__main__":
    app.run()
