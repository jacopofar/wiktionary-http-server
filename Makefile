run-server:
	python3 -m venv .venv
	.venv/bin/python3 -m pip install -r requirements.txt
	.venv/bin/sanic --access-logs wiktserver.app
.PHONY: run-server
