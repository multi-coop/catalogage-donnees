help: # Magic trick to gather command comments into a handy help message.
	@grep -E '^[a-zA-Z_-]+:.*?#- .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?#- "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv = venv
bin = ${venv}/bin/
python = ${bin}python
pip = ${bin}pip
pysources = server/ tools/ tests/

install: install-server install-client #- Install all dependencies (server and client)

install-server: #- Install server dependencies
	python3 -m venv ${venv}
	${pip} install -U pip wheel setuptools
	${pip} install -r requirements.txt

install-client: #- Install client dependencies
	cd client && npm ci

build: #- Build production assets
	cd client && npm run build

serve: #- Serve both the server and the client in parallel
	make -j 2 serve-server serve-client

serve-server: #- Run API server
	./tools/colorize_prefix.sh [server] 34 "${bin}uvicorn server.main:app --port 3579 --reload --reload-dir server"

serve-client: #- Run the client
	./tools/colorize_prefix.sh [client] 33 "cd client && npm run dev"

serve-prod: #- Serve both the server and the production client in parallel
	make -j 2 serve-server serve-prod-client

serve-prod-client: #- Run the production client 
	./tools/colorize_prefix.sh [client] 33 "cd client && npm start"

migrate: #- Apply pending migrations
	${bin}alembic upgrade head

migration: #- Create a migration
	${bin}alembic revision --autogenerate -m $(name)

currentmigration: #- Show current migraiton
	${bin}alembic show current

dbdiagram: #- Generate database diagram image
	${bin}python -m tools.erd docs/db.erd.json -o docs/db.dot
	dot docs/db.dot -T png -o docs/db.png

test: test-server test-client #- Run the server and client test suite

test-server: #- Run the server test suite
	${bin}pytest

test-client: #- Run the client test suite
	cd client && npm run test && npm run test:coverage

format: format-server format-client #- Run code formatting on server and client sources

format-server: #- Run code formatting on the server sources
	${bin}black ${pysources}
	${bin}isort ${pysources}

format-client: #- Run code formatting on the client sources
	cd client && npm run format

check: check-server check-client #- Run server and client code checks

check-server: #- Run server code checks
	${bin}black --check ${pysources}
	${bin}flake8 ${pysources}
	${bin}mypy ${pysources}
	${bin}isort --check --diff ${pysources}

check-client: #- Run client code checks
	cd client && npm run lint && npm run check

install-ops: #- Install ops dependencies
	cd ops && make install

provision-staging: #- Provision staging server
	cd ops && make provision-staging

deploy-staging: #- Deploy to staging server
	cd ops && make deploy-staging
