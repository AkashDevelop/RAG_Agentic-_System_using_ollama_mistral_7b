from agent.mysql_utils import excute_sql
from agent.chroma_utils import choromamanager
import json

chroma= choromamanager()

async def sql_search(keywords: str, date_range: str = "month"):
    "search the docs using structured sql queries"

    date_filters = {
        "day": "publication_date = CURDATE()",
        "week": "publication_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)",
        "month": "publication_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"
    }
    condition = date_filters.get(date_range, "1=1")
    
    query = f"""
        SELECT doc_id, title, abstract, publication_date, url, agencies
        FROM documents
        WHERE MATCH(title, abstract) AGAINST (%s IN NATURAL LANGUAGE MODE)
        AND {condition}
        LIMIT 5
    """

    return await excute_sql(query,(keywords,))

async def vector_search(query: str):
    # for chromaDB

    return await chroma.semantic_search(query)

TOOL_REGISTRY = {
    "vector_search": {
        "function": vector_search,
        "schema": {
            "name": "vector_search",
            "description": "Find documents using semantic similarity",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    "sql_search": {
        "function": sql_search,
        "schema": {
            "name": "sql_search",
            "description": "Search using structured database queries",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {"type": "string"},
                    "date_range": {
                        "type": "string", 
                        "enum": ["day", "week", "month"],
                        "default": "month"
                    }
                },
                "required": ["keywords"]
            }
        }
    }
}

