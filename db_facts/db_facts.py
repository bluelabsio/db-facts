from pandas import option_context
from pandas.io import sql
from . import util


class DbFacts():
    def __init__(self, job_context):
        self.logger = job_context.logger
        self.logger.debug("Initialized class!")

        self.engine = job_context.get_default_db_engine()
        self.records = job_context.records

        # Get your job config
        self.config = job_context.request_config

    def run(self):
        # Populate SQL statement with table from config
        select_sql = "select * from public.job_test"
        self.logger.info(select_sql)

        # Read table into dataframe
        # Pandas requires a database engine rather than connection
        df = sql.read_sql(select_sql, self.engine)
        with option_context('display.max_rows', 1000):
            self.logger.info("Incoming Dataframe\n" + str(df))

        # Transform the score column of the dataframe
        df['score'] = df['score'].apply(lambda x: x + 1)
        with option_context('display.max_rows', 1000):
            self.logger.info("Transformed Dataframe\n" + str(df))

        # Replace the original table with the new table from the dataframe
        util.write_to_table(df, self.engine, self.config['schema'], self.config['table'], self.records)  # noqa

        self.logger.info("Complete!")
