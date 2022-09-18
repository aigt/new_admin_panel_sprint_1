import logging
import logging.config

from settings import settings

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


async def apply(pg_conn_context):
    # with pg_transaction(pg_conn_context) as curs:
    logger.info('Open DDL file')
    with open(
        settings.DB_DDL_SCHEMA_FILE,
        encoding='utf-8',
    ) as schema_file:
        logger.info('Read DDL file')
        db_schema_query = schema_file.read()

    logger.debug(f'Applying DB schema...\n\n{db_schema_query}')
    await pg_conn_context.execute(db_schema_query)
    logger.info('Content schema is applyed')
