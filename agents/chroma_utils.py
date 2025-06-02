import chromadb
from sentence_transformers import SentenceTransformer 
from config.settings import settings

class choromamanager:
    def __init__(self):
        self.client = chromadb.HttpClient(
            host=settings.CHROMA_HOST, 
            port=settings.CHROMA_PORT

        )

        self.embedder= SentenceTransformer('all-MiniLM-L6-v2')
        self.collection= self.client.get_or_create_collection("federal_register")

    def generate_embeddings(self, texts: list[str]):
        return self.embedder.encode(texts).tolist()
    
    async def semantic_search(self,query: str,k: int=5):
        query_embedding= self.generate_embeddings([query])[0]

        results=self.collection.query(
         query_embeddings= [query_embedding],
            n_results=k,
            include=["documents","metadatas"]

        )

        return [
            {
                "content": doc,
                "metadata": meta
            }
            for doc, meta in zip(
                results["documents"][0],
                results["metadatas"][0]
            )
        ]
    
    