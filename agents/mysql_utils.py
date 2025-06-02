import aiomysql
from config.settings import settings

async def excute_sql(query: str, params:tuple=()):
    conn=await aiomysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        db=settings.MYSQL_DB
    )

    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(query,params)
        result= await cursor.fetchall()

    await conn.close()
    return result

