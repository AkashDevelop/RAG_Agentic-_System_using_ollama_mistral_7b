# data_pipeline/processor.py
import logging

def process_documents(raw_docs):
    """Convert raw API data to structured format for MySQL"""
    processed = []
    for doc in raw_docs:
        try:
            # Structure matches loader expectations
            processed.append({
                "doc_id": doc["document_number"],
                "title": doc["title"],
                "abstract": doc.get("abstract", ""),
                "full_text": doc.get("body_html", "")[:10000],
                "agencies": ", ".join(a.get("name", "") for a in doc.get("agencies", [])),
                "publication_date": doc["publication_date"],
                "url": doc["html_url"],
                "type": doc["type"]
            })
        except KeyError as e:
            logging.error(f"Missing key {e} in doc: {doc.get('document_number', 'unknown')}")
    return processed