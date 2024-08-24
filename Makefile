DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = main-app
STORAGES_FILE = docker_compose/storages.yaml


.PHONY: app
app:
	$(DC) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) down

.PHONY: app-shell
app-shell:
	$(EXEC) ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	$(LOGS) -f $(APP_CONTAINER) -f 

.PHONY: test
test:
	$(EXEC) ${APP_CONTAINER} pytest

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV) up --build -d

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) $(ENV) down

.PHONY: all
all:
	$(DC) -f $(STORAGES_FILE) -f $(APP_FILE) $(ENV) up --build -d

.PHONY: all-down
all-down:
	$(DC) -f $(STORAGES_FILE) -f $(APP_FILE) $(ENV) down
