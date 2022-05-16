## Wiktionary server

This is a very simple script to import a [Wiktextract dump](https://kaikki.org/dictionary/) into a SQLite instance, and make it available for access via HTTP.


## Create the database

`python3 scripts/import_wiktextract.py your-downloaded-file.json`
this does not require any dependency, it will create a `dict.db` file.

## Run the server

Create a virtualenv, install the dependencies in the requirements.txt file and run `sanic wiktserver.app`. Or use `make run-server` to do that for you (the virtualenv will be created as `.venv`)

Then, try visiting `http://localhost:8000/w/blabla` to get a JSON with the senses of the word `blabla`.

That's it.

## Wait, and the tests? The CI?

Nope, it's fine as is thanks

## License

MIT