
from unittest.mock import patch, MagicMock
from vector_store import VectorStore


@patch("vector_store.Chroma")
@patch("vector_store.HuggingFaceEmbeddings")
@patch("vector_store.config")
def test_vector_store_initialization(
    mock_config,
    mock_embeddings,
    mock_chroma
):

    mock_config.side_effect = [
        "./chroma_db",
        "sentence-transformers/all-MiniLM-L6-v2"
    ]

    store = VectorStore()

    mock_embeddings.assert_called_once_with(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    mock_chroma.assert_called_once()

    assert store.persist_directory == "./chroma_db"


@patch("vector_store.Chroma")
@patch("vector_store.HuggingFaceEmbeddings")
@patch("vector_store.config")
def test_vector_store_search(
    mock_config,
    mock_embeddings,
    mock_chroma
):

    mock_config.side_effect = [
        "./chroma_db",
        "test-model"
    ]

    mock_vectorstore = MagicMock()

    mock_chroma.return_value = mock_vectorstore

    expected_result = [
        ("Document 1", 0.25),
        ("Document 2", 0.50)
    ]

    mock_vectorstore.similarity_search_with_score.return_value = (
        expected_result
    )

    store = VectorStore()

    result = store.search("What is Python?", k=2)

    mock_vectorstore.similarity_search_with_score.assert_called_once_with(
        "What is Python?",
        k=2
    )

    assert result == expected_result
