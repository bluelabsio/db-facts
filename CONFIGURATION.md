# db-facts configuration

db-facts currently bundles a default configuration located at
[db_facts/dbcli.yml](./db_facts/dbcli.yml). You can add additional configs or
override existing ones by using custom configs. db-facts looks for configs in
the following order:

* `/etc/dbfacts.yml`
* All files in `/etc/dbfacts.d` in lexicographic order
* `/usr/local/etc/dbfacts.yml`
* All files in `/usr/local/etc/dbfacts.d` in lexicographic order
* `~/.dbfacts.yml`
* All files in `~/.dbfacts.d` in lexicographic order
* `./.dbfacts.yml`
* All files in `./.dbfacts.d` in lexicographic order

Each time it encounters a file in the list above, it merges the config in that
file into the existing config to generate a new one. Top-level config
dictionaries are merged with the last-loaded config values taking precedence.
For example, if your `~/.dbfacts.yml` contains:

```yaml
dbs:
  mydb1:
    exports:
      user: cwegrzyn
      hostname: a.example.com
  mydb2:
    exports:
      user: cwegrzyn2
      hostname: b.example.com
orgs:
  org1:
    full_name: My Org
```

and `~/.dbfacts.d/001_mydb2.yml` contains:

```yaml
dbs:
  mydb2:
    exports:
      user: cwegrzyn3
orgs:
  org2:
    full_name: My Other Org
```

then the effective configuration for db-facts is:

```yaml
dbs:
  mydb1:
    exports:
      user: cwegrzyn
      hostname: a.example.com
  mydb2:
    exports:
      user: cwegrzyn3
orgs:
  org1:
    full_name: My Org
  org2:
    full_name: My Other Org
```

Note that the entry for `mydb2` has been COMPLETELY replaced; the two different
configurations were NOT merged. Only the top-levels are merged.

## Common configuration patterns

### Standard LastPass credentials

```yaml
dbs:
  staticlpass:
    jinja_context_name: standard
    db_connect_method: lpass
    lastpass_entry: "Just Some Awesome Database Credentials"
  dynamiclpass:
    jinja_context_name: standard
    db_connect_method: lpass
    lastpass_entry: "{{ username }} Specific Database Credentials"
```

With this config:

* `db-facts staticlpass` will give you the credentials in the lastpass entry
  "Just Some Awesome Database Credentials"
* `db-facts dynamiclpass` will give you the credentials in the lastpass entry
  "auser Awesome Database Credentials" assuming your name is Alice User and
  therefore your first initial + last name is `auser`
* `db-facts dynamiclpass-anadmin` will give you the credentials in the lastpass
  entry "anadmin Awesome Database Credentials" (in other words, the username is
  replaced by whatever comes after the dashes)

### Inline credentials

While this is not recommended for local laptop use (please use a lastpass
config), it is currently the only supported strategy for JupyterHub.

Here is an example redshift config with inline credentials:

```yaml
dbs:
  myconfig:
    exports:
      host: a.example.com
      port: 5432
      database: analytics
      type: redshift
      protocol: postgres
      user: cwegrzyn
      password: thisisagreatpassword
```
