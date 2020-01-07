mock_dbcli_config = {
    'db_connect_method': {
        'lpass': {
            'pull_lastpass_from': "{{ lastpass_entry }}",
        },
        'lpass_user_and_pass_only': {
            'pull_lastpass_username_password_from': "{{ lastpass_entry }}",
        },
        'my-json-script': {
            'json_script': [
                'some-custom-json-script'
            ]
        },
        'invalid-method': {
        },
    },
    'dbs': {
        'baz': {
            'db_connect_method': 'my-json-script',
        },
        'bing': {
            'db_connect_method': 'invalid-method',
        },
        'bazzle': {
            'db_connect_method': 'lpass',
            'lastpass_entry': 'lpass entry name'
        },
        'bazzle-bing': {
            'db_connect_method': 'lpass',
            'lastpass_entry': 'different lpass entry name'
        },
        'frazzle': {
            'db_connect_method': 'lpass',
            'lastpass_entry': 'lpass entry name'
        },
        'frink': {
            'db_connect_method': 'lpass_user_and_pass_only',
            'lastpass_entry': 'lpass entry name',
            'jinja_context_name': 'standard',
            'exports': {
                'some_additional': 'export',
                'a_numbered_export': 123
            },
        },
        'gaggle': {
            'jinja_context_name': [
                'env',
                'base64',
            ],
            'exports': {
                'type': 'bigquery',
                'protocol': 'bigquery',
                'bq_account': 'bq_itest',
                'bq_service_account_json':
                "{{ env('ITEST_BIGQUERY_SERVICE_ACCOUNT_JSON_BASE64') | b64decode }}",
                'bq_default_project_id': 'bluelabs-tools-dev',
                'bq_default_dataset_id': 'bq_itest',
            },
        },
    },
    'orgs': {
        'myorg': {
            'full_name': 'MyOrg',
        },
    },
}
