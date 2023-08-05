
SHELL := /bin/bash

REDIS_RUNNING := $(shell if $$(pgrep redis-server &>/dev/null); then echo 1; else echo 0; fi)
MONGO_RUNNING := $(shell if $$(pgrep mongod &>/dev/null); then echo 1; else echo 0; fi)
REDIS_PORT := 39123
MONGO_PORT := 39124

VIRTUAL_ENV ?= $$(pwd)/env
ENV := $(VIRTUAL_ENV)
PYTHON := $(ENV)/bin/python
PIP := $(ENV)/bin/pip
TOX := $(ENV)/bin/tox

export VIRTUAL_ENV
export REDIS_RUNNING
export MONGO_RUNNING
export REDIS_PORT
export MONGO_PORT

.PHONY: venv
venv:
	@if [ ! -e $(ENV) ]; then virtualenv $(ENV); fi
	@if [ ! -e $(PIP) ]; then echo "pip not found in environment - $(ENV)"; exit 1; fi
	@if [ ! -e $(TOX) ]; then \
		echo "Installing tox in $(ENV)"; \
		$(PIP) install tox; \
	fi

.PHONY: buildout
buildout: venv
	@mkdir -p .buildout
	@if [ ! -e ".buildout/installed.cfg" ]; then \
		$(PYTHON) bootstrap.py; \
	fi;
	@./bin/buildout

.PHONY: apt-get-mongodb
apt-get-mongodb:
	@apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
	@echo "deb http://repo.mongodb.org/apt/ubuntu $$(lsb_release -sc)/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
	@apt-get update && apt-get -y install mongodb-org

.PHONY: redis
redis:
	@./bin/redis-server --port $(REDIS_PORT)

.PHONY: mongod
mongod:
	@./bin/mongod --port $(MONGO_PORT) --dbpath $$(pwd)/data --replSet rs0 --logpath $$(pwd)/logs/mongod.log --pidfilepath $$(pwd)/var/mongod.pid

.PHONY: mongo
mongo:
	@./bin/mongo --port $(MONGO_PORT)

.PHONY: test
test: venv
	@$(TOX)

.PHONY: shell
shell:
	@./bin/python

.PHONY: clean
clean:
	@rm -rf .tox
	@rm -rf .buildout
	@rm -rf bin
	@rm -rf *.egg-info

.PHONY: environ
environ:
	@echo "VIRTUAL_ENV: $(ENV)"
	@echo -n "MONGO_RUNNING: "
	@if [ $(MONGO_RUNNING) -eq 0 ]; then echo "no"; else echo "yes"; fi
	@echo -n "REDIS_RUNNING: "
	@if [ $(REDIS_RUNNING) -eq 0 ]; then echo "no"; else echo "yes"; fi

.PHONY: sdist
sdist:
	$(PYTHON) setup.py sdist

.PHONY: register
register:
	$(PYTHON) setup.py register

.PHONY: upload
upload:
	$(PYTHON) setup.py sdist upload

