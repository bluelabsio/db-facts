import logging

logger = logging.getLogger(__name__)


def write_to_table(df, engine, schema_name, table_name, records):
    logger.info("Writing dataframe to database...")
    with records.sources.dataframe(df=df,
                                   schema_name=schema_name,
                                   table_name=table_name,
                                   db_engine=engine) as source,\
        records.targets.table(db_engine=engine,
                              schema_name=schema_name,
                              table_name=table_name) as target:
        records.move(source, target)
