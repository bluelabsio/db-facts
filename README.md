# TODO: Follow these initial steps and then remove them

Welcome to create-python-app!

This app includes:

* A working Dockerfile
* Nosetests test suite and test coverage
* Quality ruby gem
* Scripts to build, test, and run the app
* And more!

## Getting started

### Push to github

Visit [github](https://github.com/new) and create your private project
there under bluelabsio, then follow the instructions to push your repo
up.

### Configuring CircleCI to build

1. [Add your project](https://circleci.com/add-projects/gh/bluelabsio)
   in CircleCI.
2. Go to the settings for your project (gear icon)
3. Environment Variables
4. Import Variables
5. `bluelabs-joblib-python`
6. Select `ARTIFACTORY_PYPI_INDEX_URL` and `PRONTO_GITHUB_ACCESS_TOKEN`
7. Import

### Create your feature branch

```sh
git checkout -b initial
```

### Adding your requirements

Add your python requirements to the [requirements.txt](./requirements.txt)
file and they will be automatically imported on build by the default
[Dockerfile](./Dockerfile).

### Configure your arguments

The `job_config_schema` variable in `__main__.py` describes the
arguments you can pass on the command line. See [schema
examples](http://json-schema.org/examples.html) to help craft
arguments that make sense for your job.

### Clean up this README

Drop from here above, replace `## Boilerplate README` with `# Db Facts`, and
start hacking using the instructions below to develop!

## Boilerplate README

This, and the below sections, should be included in your project:

## Development

### Code locations

* `db_facts/db_facts.py`
  contains the main logic.
* `db_facts/__main__.py` will let you define new
  config to take in.
* `tests/` has some example unit tests.

### Installing development tools

#### pyenv

For instructions on installing pyenv visit the wiki
page:
[Using different versions of python in the same environment](https://github.com/bluelabsio/knowledge/wiki/Python-cheatsheet#using-different-versions-of-python-in-the-same-environment)

#### virtualenv

Follow the installation instructions from the wiki
page:
[Set up a Virtual Environment for your project](https://github.com/bluelabsio/knowledge/wiki/Python-cheatsheet#set-up-a-virtual-environment-for-your-project)

### Building

Download Python dependencies and create a virtual environment:

```bash
./deps.sh
```

### Running on the command line

To run on the command line:

```sh
with-db redshift db_facts $(redshift-username) job_test
```

### Pushing to Docker

#### Configuring Jenkins to build (developers)

See [these instructions](https://github.com/bluelabsio/knowledge/wiki/Jenkins#to-set-up-a-build)
to set up Jenkins.  The Jenkinsfile here should work fine.

### Testing

Run all of the tests except for the slow ones:

```bash
make test
```

To build a docker image and run your tests, you can call `./test.sh`.

### Semantic versioning

In this house, we use [semantic versioning](http://semver.org) to indicate
when we make breaking changes to interfaces.  If you don't want to live
dangerously, and you are currently using version a.y.z (see setup.py to see
what version we're at) specify your requirement like this in requirements.txt:

db_facts>=a.x.y,<b.0.0

This will make sure you don't get automatically updated into the next
breaking change.
