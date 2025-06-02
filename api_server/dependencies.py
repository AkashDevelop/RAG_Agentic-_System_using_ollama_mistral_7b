from agent.mysql_utils import execute_sql 
from config.settings import settings
import aiomysql

async def get_db_conn():
    return await aiomysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        db=settings.MYSQL_DB
    )
