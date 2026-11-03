
ifeq ($(filter 4.%,$(MAKE_VERSION)),)
    $(error \
		Для работы требуется GNU Make версии 4.x. \
		У вас установлена версия: $(MAKE_VERSION). \
		Для windows версию 4.x можно найти тут: https://github.com/mbuilov/gnumake-windows/tree/master )
endif

ifeq ($(OS),Windows_NT)
	SHELL := powershell.exe
	.SHELLFLAGS := -NoProfile -Command
	RM := Remove-Item -Force -ErrorAction SilentlyContinue
	RM_DIR := Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
	EXT := .exe
else
	SHELL := /bin/bash
	.SHELLFLAGS := -c
	RM := rm -f
	RM_DIR := rm -rf
	EXT :=
endif

VENV := $(CURDIR)/.venv
VENV_PYTHON :=$(VENV)/Scripts/python$(EXT)
VENV_PIP := $(VENV)/Scripts/pip$(EXT)

DOCKER := docker
DOCKER_RUN := $(DOCKER) run -it --rm
DOCKER_COMPOSE := $(DOCKER) compose

env:
	python -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PIP) install -r "$(CURDIR)/requirements.txt"

prune:
	$(DOCKER) system prune -a --volumes

postgres-up:
	$(DOCKER_COMPOSE) up postgres -d

postgres-down:
	$(DOCKER_COMPOSE) down postgres --rmi all --volumes

spark-up:
	$(DOCKER_COMPOSE) up spark-master spark-worker spark-connect -d

spark-down:
	$(DOCKER_COMPOSE) down postgres --rmi all --volumes
