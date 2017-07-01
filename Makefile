DIRTY=$(shell python -c "import versioneer; print versioneer.get_versions()['dirty']")

all: doc package

setup: devenv
	. devenv/bin/activate && tools/git/setup_git_hooks.sh

devenv:
	tox -e devenv -v

.PHONY : clean-tox
clean-tox:
	rm -rf devenv .tox

.PHONY : clean-python
clean-python:
	find ./ -name '*.pyc' -delete
	find ./ -name '__pycache__' -delete

.PHONY : clean-package
clean-package:
	rm -rf non-git dist nflex_connector_utils.egg-info

.PHONY: clean-docs
clean-docs:
	cd doc && make clean

.PHONY : clean
clean: clean-tox clean-python clean-package clean-docs

.PHONY : test
test:
	tox

.PHONY : test-coverage
test-coverage: devenv
	devenv/bin/py.test -v --cov-report=term-missing --cov=nflex_connector_utils

.PHONY : doc
doc:
	cd doc && make html

.PHONY: watch-docs-mac
watch-docs-mac:
	cd doc && ./watch-docs-mac.sh

.PHONY : package
package: clean-package
	python setup.py sdist

.PHONY : upload
upload:
	@test -z "$$(git status --short)" || (echo branch is not clean && git status --short && false)
	python setup.py sdist upload -r https://upload.pypi.org/legacy/
