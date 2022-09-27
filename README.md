## Wiktionary server

This is a very simple script to import a [Wiktextract dump](https://kaikki.org/dictionary/) into a SQLite instance, and make it available for access via HTTP.


## Create the database

`python3 scripts/import_wiktextract.py your-downloaded-file.json dict.db`
this does not require any dependency, it will create a `dict.db` file.

## Run the server

The server has no dependencies because it uses `SimpleHTTPServer`.

Just run `python3 server.py`, it will look for the `dict.db` file and serve its content.

Then, try visiting `http://localhost:8090/w/blabla` to get a JSON with the senses of the word `blabla`.

That's it.

## Wait, and the tests? The CI?

Nothing, it's literally an endpoint and SQLLite.

## License

MIT