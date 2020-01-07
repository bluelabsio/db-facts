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

### Pulling auth tokens from the environment

```yaml
dbs:
  mybigquerydb-myserviceuser:
    jinja_context_name:
      - env
      - base64
    exports:
      type: bigquery
      protocol: bigquery
      bq_account: myserviceuser
      bq_service_account_json: "{{ env('GCP_SERVICE_ACCOUNT_JSON_BASE64') | b64decode }}"
      bq_default_project_id: 'my_gcp_project'
      bq_default_dataset_id: 'my_bigquery_dataset
```

With this config, `db-facts mybigquerydb-myserviceuser` will show you the credentials,
  including the decoded environment variable.  "Just Some Awesome

### Inline credentials

While this is not recommended (please save your secrets more securely
than a YAML file sitting on disk!), you can specify things this way if
you must.

Here is an example Redshift config with inline credentials:

```yaml
dbs:
  myconfig:
    exports:
      host: a.example.com
      port: 5432
      database: analytics
      type: redshift
      protocol: postgres
      user: janalyst
      password: thisisagreatpassword
```
