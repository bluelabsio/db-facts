from .db_facts import DbFacts
from bluelabs_joblib.job_context import create_job_context
from odictliteral import odict


def main():
    # This is JSON Schema - see http://json-schema.org/learn/miscellaneous-examples.html
    job_config_schema = {
        "type": "object",
        "properties": odict[
            'schema': {
                'type': 'string'
            },
            'table': {
                'type': 'string'
            },
        ],
        "required": ["schema", "table"],
    }
    with create_job_context('db_facts',
                            config_json_schema=job_config_schema) as job_context:
        try:
            job_context.logger.info('Starting...')
            DbFacts(job_context).run()
            job_context.logger.info('Done')
        except Exception as e:
            job_context.logger.error(e)
            raise


if __name__ == '__main__':
    main()
