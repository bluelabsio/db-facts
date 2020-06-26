# Development

## Installing tools and dependencies

This assumes you have a configured and working pyenv and
pyenv-virtualenv installation:

```bash
./deps.sh
```

## Testing

Run the tests:

```bash
make test
```

## Semantic versioning

In this house, we use [semantic versioning](http://semver.org) to indicate
when we make breaking changes to interfaces.  If you don't want to live
dangerously, and you are currently using version a.y.z (see setup.py to see
what version we're at) specify your requirement like this in requirements.txt:

db_facts>=a.x.y,<b.0.0

This will make sure you don't get automatically updated into the next
breaking change.

## Documentation

API reference documentation is pushed up to
[readthedocs](https://db-facts.readthedocs.io/en/published_docs/) by a
GitHub webhook.

To create docs, run this from the `docs/` directory:

* `make html`

To view docs:

* `open build/html/index.html`
