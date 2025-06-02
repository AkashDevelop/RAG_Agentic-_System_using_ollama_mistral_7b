# data_pipeline/downloader.py
import aiohttp
import asyncio
from datetime import datetime, timedelta, timezone
import logging

FEDERAL_REG_URL = "https://www.federalregister.gov/api/v1/documents.json"

async def fetch_docs(days_back: int = 1):
    """Fetch documents from Federal Register API"""
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=days_back)

    params = {
        "conditions[publication_date][gte]": start_date.isoformat(),
        "conditions[publication_date][lte]": end_date.isoformat(),
        "per_page": 100,
        "order": "newest"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FEDERAL_REG_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
                logging.error(f"API error: {response.status}")
                return []
    except Exception as e:
        logging.error(f"Failed to fetch documents: {e}")
        return []