from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import VectorParams, Distance
from app.config import settings

class QdrantMemory:
    def __init__(self):
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection_name = "aether_history"
        self.ensure_collection()

    def ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except UnexpectedResponse as exc:
            # expected when collection does not exist (404)
            if getattr(exc, 'status', None) == 404 or 'Not found' in str(exc):
                self.client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
            else:
                raise

    async def search(self, session_id: str, history: list):
        # placeholder: async call not supported in this wrapper; use blocking for POC
        return ""

    async def upsert(self, session_id: str, payload: dict):
        # placeholder
        pass
