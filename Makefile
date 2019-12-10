all: typecheck coverageclean test coverage quality

coverageclean:
	rm -fr .coverage

realclean: clean
	rm -rf .cached_deps

clean:
	FILES=$$(find . -name \*.pyc); for f in $${FILES}; do rm $$f; done

typecheck:
	mypy --cobertura-xml-report typecover --html-report typecover .

test:
	ENV=test nosetests --cover-package=db_facts --with-coverage --with-xunit --cover-html --cover-xml --nocapture --cover-inclusive

citest:
	ENV=test nosetests --exclude='tests/integration' --cover-package=db_facts --with-coverage --with-xunit --cover-html --cover-xml --nocapture --cover-inclusive --xunit-file=test-reports/junit.xml

coverage:
	python setup.py coverage_ratchet

# to run a single item, you can do: make QUALITY_TOOL=bigfiles quality
quality:
	@quality_gem_version=$$(python -c 'import yaml; print(yaml.safe_load(open(".circleci/config.yml","r"))["quality_gem_version"])'); \
	docker run  \
	       -v "$$(pwd):/usr/app"  \
	       -v "$$(pwd)/Rakefile.quality:/usr/quality/Rakefile"  \
	       "apiology/quality:$${quality_gem_version}" ${QUALITY_TOOL}

package:
	python3 setup.py sdist bdist_wheel

docker:
	PIP_CONFIG_FILE=$${PIP_CONFIG_FILE:-/Library/Application\ Support/pip/pip.conf}; \
	DOCKER_BUILDKIT=1 docker build --progress=plain -t db_facts --secret id=pipconf,src="$${PIP_CONFIG_FILE:?}" .
