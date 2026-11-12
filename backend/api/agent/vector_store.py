from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from decouple import config

class VectorStore:

    def __init__(
        self,
        persist_directory=None,
        embedding_model=None,
    ):

        # Load configuration
        self.persist_directory = (
            persist_directory or config("PERSIST_DIRECTORY")
        )

        self.embedding_model = (
            embedding_model or config("EMBEDDING_MODEL")
        )

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )

        # Initialize Chroma
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
        )

    # --------------------
    # Search document
    # --------------------

    def search(self, query: str, k: int = 4):

        return self.vectorstore.similarity_search_with_score(
            query,
            k=k,
        )
