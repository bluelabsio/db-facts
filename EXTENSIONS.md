# Extensions

You can create a plugin providing your own Jinja contexts by creating a Python package
implementing functions matching the 'JinjaContextPuller' type defined in
[db_facts_types.py](https://github.com/bluelabsio/db-facts/blob/master/db_facts/db_facts_types.py).
You can use the existing Jinja context pullers
(`pull_*_jinja_context`) referenced in
[jinja_context.py](https://github.com/bluelabsio/db-facts/blob/master/db_facts/jinja_context.py)
as examples.

To get `db_facts` to use your Jinja context pullers, you'll create
config similar to this in your `setup.py` file:

```python
setup(name='my_db_facts_plugin',
      ...
      entry_points={
          "db_facts.jinja_contexts": [
              'my_context = my_db_facts_plugin.my_jinja_context:pull_my_jinja_context',
          ]
      },
```

More details:

* [setuptools docs](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins)
* [Python packaging docs](https://packaging.python.org/guides/creating-and-discovering-plugins/#using-naming-convention)
