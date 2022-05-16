from multiprocessing import connection
import sqlite3

from ujson import loads
from sanic import Sanic
from sanic.response import json


app = Sanic("wiktionary_app")
app.ctx.connection = sqlite3.connect("dict.db")
app.ctx.cur = app.ctx.connection.cursor()


@app.get("/w/<word:str>")
async def test(request, word: str):
    entries = loads(
        app.ctx.cur.execute(
            "SELECT entries from words where word = ?", (word,)
        ).fetchone()[0]
    )
    return json(entries)


if __name__ == "__main__":
    app.run()
