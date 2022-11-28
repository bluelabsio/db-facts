mock_dbcli_config = {
    'exports_from': {
        'lpass': {
            'pull_lastpass_from': "{{ lastpass_entry }}",
        },
        'lpass_user_and_pass_only': {
            'pull_lastpass_username_password_from': "{{ lastpass_entry }}",
        },
        'lpass_aws_iam': {
            'pull_lastpass_aws_iam': "{{ lastpass_entry }}"
        },
        'my-json-script': {
            'json_script': [
                'some-custom-json-script'
            ]
        },
        'invalid-method': {
        },
        'secrets_manager': {
            'pull_secrets_manager_from': "{{ secrets_manager_entry }}"
        },
        'secrets_manager_user_and_pass_only': {
            'pull_secrets_manager_username_password_from': "{{ secrets_manager_entry }}"
        },
    },
    'dbs': {
        'baz': {
            'exports_from': 'my-json-script',
        },
        'bing': {
            'exports_from': 'invalid-method',
        },
        'bazzle': {
            'exports_from': 'lpass',
            'lastpass_entry': 'lpass entry name'
        },
        'bazzle-bing': {
            'exports_from': 'lpass',
            'lastpass_entry': 'different lpass entry name'
        },
        'bazzle-boozle': {
            'exports_from': 'lpass_aws_iam',
            'lastpass_entry': 'lpass entry name'
        },
        'fromage': {
            'exports_from': 'secrets_manager',
            'secrets_manager_entry': 'secrets manager entry name'
        },
        'frazzle': {
            'exports_from': 'lpass',
            'lastpass_entry': 'lpass entry name'
        },
        'frink': {
            'exports_from': 'lpass_user_and_pass_only',
            'lastpass_entry': 'lpass entry name',
            'jinja_context_name': 'standard',
            'exports': {
                'some_additional': 'export',
                'a_numbered_export': 123
            },
        },
        'fronk': {
            'exports_from': 'secrets_manager_user_and_pass_only',
            'secrets_manager_entry': 'secrets manager entry name',
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
