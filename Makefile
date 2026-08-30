LIBRARY_NAME := $(shell hatch project metadata name 2> /dev/null)
LIBRARY_VERSION := $(shell hatch version 2> /dev/null)
REPO := $(shell git remote get-url origin)

.PHONY: usage version dev-deps check pre-commit qa pytest nopost tag build clean testdeploy deploy package.json
usage:
ifdef LIBRARY_NAME
	@echo "Library: ${LIBRARY_NAME}"
	@echo "Version: ${LIBRARY_VERSION}\n"
else
	@echo "WARNING: You should 'make dev-deps'\n"
endif
	@echo "Usage: make <target>, where target is one of:\n"
	@echo "dev-deps:     install Python dev dependencies"
	@echo "check:        verify CHANGELOG.md and package.json match the current version"
	@echo "pre-commit:   run pre-commit hooks (lint, whitespace) on all files"
	@echo "qa:           run package QA (check-manifest, build, twine)"
	@echo "pytest:       run Python test fixtures"
	@echo "package.json: regenerate package.json from the contents of src/"
	@echo "clean:        clean Python build and dist directories"
	@echo "build:        build Python distribution files"
	@echo "testdeploy:   build and upload to test PyPi"
	@echo "deploy:       build and upload to PyPi"
	@echo "tag:          tag the repository with the current version\n"

version:
	@hatch version

dev-deps:
	python3 -m pip install --group dev
	pre-commit install

check:
	@LIBRARY_VERSION=`hatch version | awk -F '.' '{print $$1"."$$2"."$$3}'`; \
	if grep -q "^$$LIBRARY_VERSION" CHANGELOG.md; then \
		echo "Changes found for version $$LIBRARY_VERSION."; \
	else \
		echo "Changes missing for version $$LIBRARY_VERSION! Please update CHANGELOG.md."; \
		exit 1; \
	fi; \
	JSON_VERSION=`python3 -c "import json; print(json.load(open('package.json'))['version'])"`; \
	if [ "$$LIBRARY_VERSION" = "$$JSON_VERSION" ]; then \
		echo "package.json is at version $$JSON_VERSION."; \
	else \
		echo "package.json version ($$JSON_VERSION) does not match library version ($$LIBRARY_VERSION)! Please 'make package.json'."; \
		exit 1; \
	fi

pre-commit:
	pre-commit run --all-files

qa:
	tox -e qa

pytest:
	tox -e py

package.json:
	./tools/mkpackagejson.py --ver ${LIBRARY_VERSION} --repo ${REPO} src/

nopost:
	@POST_VERSION=`hatch version | awk -F '.' '{print $$4}'`; \
	if [ -n "$$POST_VERSION" ]; then \
		echo "Found .$$POST_VERSION on library version; only use these for testpypi releases."; \
		exit 1; \
	fi

tag: version
	git tag -a "v${LIBRARY_VERSION}" -m "Version ${LIBRARY_VERSION}"

build: check
	uv build

clean:
	-rm -r dist

testdeploy: build
	twine upload --repository testpypi dist/*

deploy: nopost build
	twine upload dist/*
