help: # Magic trick to gather command comments into a handy help message.
	@grep -E '^[a-zA-Z_-]+:.*?#- .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?#- "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv = venv
bin = ${venv}/bin/
python = ${bin}python
pip = ${bin}pip
pysources = server/ tools/ tests/
git_current_ref = $(shell git rev-parse --verify --short HEAD)

install: install-server install-client #- Install all dependencies (server and client)

install-server: #- Install server dependencies
	python3 -m venv ${venv}
	${pip} install -U pip wheel setuptools
	${pip} install -r requirements.txt

install-client: #- Install client dependencies
	cd client && npm ci && npx playwright install firefox

build: #- Build production assets
	cd client && npm run build

serve: #- Serve both the server and the client in parallel
	make -j 2 serve-server serve-client

serve-server: #- Run API server
	./tools/colorize_prefix.sh [server] 34 "${python} -m server.main"

serve-client: #- Run the client
	./tools/colorize_prefix.sh [client] 33 "cd client && npm run dev"

serve-dist: #- Serve both the server and the built client in parallel
	make -j 2 serve-server serve-dist-client

serve-dist-client: #- Run the built client 
	./tools/colorize_prefix.sh [client] 33 "cd client && npm start"

compose-up: #- Start Docker Compose setup
	docker-compose up --build -d
	docker-compose run migrate
	docker-compose run initdata

compose-down: #- Stop and teardown Docker Compose setup
	docker-compose down

migrate: #- Apply pending migrations
	${bin}alembic upgrade head

migration: #- Create a migration
	${bin}alembic revision --autogenerate -m $(name)

currentmigration: #- Show current migraiton
	${bin}alembic show current

initdata: #- Initialize data
	${bin}python -m tools.initdata tools/initdata.yml

dedupe-tags: #- Dedupe tags
	${bin}python -m tools.remove_duplicated_tags

initdatareset: #- Initialize data, resetting any changed target entities
	${bin}python -m tools.initdata --reset tools/initdata.yml

n ?= 500
randomdatasets: #- Add 500 random datasets
	${bin}python -m tools.addrandomdatasets $(n) $(siret)

id: #- Generate an ID suitable for use in database entities
	${bin}python -m tools.makeid

apikey: #- Generate an API key token
	${bin}python -m tools.makeapikey

secretkey: #- Generate a cookie signing secret key using Django 
	${bin}python -m tools.makesecretkey

changepassword: #- Change password of a user account
	${bin}python -m tools.changepassword

dbdiagram: #- Generate database diagram image
	${bin}python -m tools.erd docs/db.erd.json -o docs/db.dot
	dot docs/db.dot -T png -o docs/db.png

dsfr-icon-extras: #- Generate CSS for extra DSFR icons
	${bin}python -m tools.iconextras \
		--prefix fr-icon-x- \
		--output client/src/styles/dsfr-icon-extras.css

test: test-server test-client #- Run the server and client test suite

test-ci: test-server test-client-ci #- Run the server and client test suite in CI mode

test-server: #- Run the server test suite
	${bin}pytest

test-client: test-client-unit test-client-e2e #- Run the client's unit and e2e tests

test-client-ci: test-client-unit test-client-e2e-ci #- Run the client's unit and e2e tests in CI mode

test-client-unit: #- Run the client test suite
	cd client && npm run test:coverage

test-client-e2e: #- Run the client e2e test suite
	cd client && npm run test-e2e

test-client-e2e-ci: #- Run the client e2e test suite in a CI mode
	cd client && npm run test-e2e:ci

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

ops-install: #- Install ops dependencies
	cd ops && make install

ops-secrets: #- Edit environment secrets
	cd ops && make secrets env=$(env)

ops-provision: #- Provision environment
	cd ops && make provision env=$(env)

ops-deploy: #- Deploy environment
	cd ops && make deploy env=$(env)

ops-initdata: #- Run initdata in environment
	cd ops && make initdata env=$(env)

ops-staging: #- Sync staging branch with changes from current branch 
	git checkout staging 
	git pull --rebase origin staging
	git merge --no-edit $(git_current_ref)
	@echo "Success. You may now push and deploy"

ops-staging-sync: #- Sync staging branch with master
	git checkout master
	git pull --rebase origin master
	git branch -D staging
	git checkout -b staging
	@echo "Almost done. You must now force-push (hint: git push --set-upstream origin staging --force)"
