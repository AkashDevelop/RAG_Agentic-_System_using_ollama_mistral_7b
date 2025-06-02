# data_pipeline/loader.py
import aiomysql
import logging
from config.settings import settings

async def load_to_mysql(documents):
    """Load processed documents into MySQL"""
    if not all([
        settings.MYSQL_HOST,
        settings.MYSQL_PORT,
        settings.MYSQL_USER,
        settings.MYSQL_PASSWORD,
        settings.MYSQL_DB
    ]):
        logging.error("MySQL settings are incomplete. Please check your .env file.")
        return False

    conn = None  
    try:
        conn = await aiomysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DB
        )
    except Exception as conn_err:
        logging.error(f"Failed to connect to MySQL: {conn_err}")
        return False

    try:
        async with conn.cursor() as cursor:
            # Suppress table exists warning
            await cursor.execute("SET sql_notes = 0;")

            # Create table if not exists
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    doc_id VARCHAR(50) PRIMARY KEY,
                    title TEXT NOT NULL,
                    abstract TEXT,
                    full_text TEXT,
                    agencies TEXT,
                    publication_date DATE,
                    url VARCHAR(255),
                    type VARCHAR(50)
                )
            """)
            await cursor.execute("SET sql_notes = 1;")

            # Insert or update documents
            for doc in documents:
                try:
                    await cursor.execute("""
                        INSERT INTO documents 
                        (doc_id, title, abstract, full_text, agencies, publication_date, url, type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            title = VALUES(title),
                            abstract = VALUES(abstract),
                            full_text = VALUES(full_text),
                            agencies = VALUES(agencies),
                            publication_date = VALUES(publication_date),
                            url = VALUES(url),
                            type = VALUES(type)
                    """, (
                        doc.get("doc_id"),
                        doc.get("title"),
                        doc.get("abstract"),
                        doc.get("full_text"),
                        doc.get("agencies"),
                        doc.get("publication_date"),
                        doc.get("url"),
                        doc.get("type")
                    ))
                except Exception as insert_err:
                    logging.error(f"Failed to insert document {doc.get('doc_id', 'unknown')}: {insert_err}")

            await conn.commit()
            return True

    except Exception as e:
        logging.error(f"MySQL operation error: {e}")
        return False

    finally:
        if conn:
            conn.close()  
