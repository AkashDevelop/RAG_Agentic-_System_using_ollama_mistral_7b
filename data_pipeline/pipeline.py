# data_pipeline/pipeline.py
import sys
import os
import asyncio
import logging

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_pipeline.downloader import fetch_docs
from data_pipeline.processor import process_documents
from data_pipeline.loader import load_to_mysql

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def run_daily_pipeline():
    try:
        logging.info("Starting data pipeline")

        # Fetch documents from API
        raw_docs = await fetch_docs(days_back=1)
        logging.info(f"Fetched {len(raw_docs)} documents")

        if not raw_docs:
            logging.warning("No documents fetched from API")
            return False

        # Process documents
        processed_docs = process_documents(raw_docs)
        if not processed_docs:
            logging.warning("No documents processed")
            return False

        # Load to MySQL
        success = await load_to_mysql(processed_docs)
        if success:
            logging.info("Data loaded to MySQL successfully")
            return True
        return False

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    asyncio.run(run_daily_pipeline())