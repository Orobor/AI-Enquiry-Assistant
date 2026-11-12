
from unittest.mock import patch, MagicMock
import pytest

from api.agent.llm_service import LLMService


@pytest.fixture
def service():
    with patch("api.agent.llm_service.ChatOpenAI") as mock_llm:
        with patch("api.agent.llm_service.config") as mock_config:

            mock_config.side_effect = lambda key, **kwargs: {
                "MODEL_PATH": "test-model",
                "API_KEY": "test-api-key",
            }.get(key, kwargs.get("default"))

            instance = LLMService()

            yield instance


def test_llm_initialization(service):
    assert service.llm is not None


def test_build_messages(service):

    messages = service.build_messages(
        system_prompt="You are a helpful assistant.",
        question="What is Python?",
        context=["Python is a programming language."]
    )

    assert len(messages) == 2
    assert messages[0].content == "You are a helpful assistant."
    assert "What is Python?" in messages[1].content
    assert "Python is a programming language." in messages[1].content


def test_build_messages_without_context(service):

    messages = service.build_messages(
        system_prompt="You are helpful.",
        question="Hello"
    )

    assert len(messages) == 2
    assert "Hello" in messages[1].content


def test_generate(service):

    mock_response = MagicMock()
    mock_response.content = "Python is a programming language."

    service.llm.invoke.return_value = mock_response

    result = service.generate([])

    assert result == "Python is a programming language."
    service.llm.invoke.assert_called_once()


def test_generate_non_string_response(service):

    mock_response = MagicMock()
    mock_response.content = ["Hello", "World"]

    service.llm.invoke.return_value = mock_response

    result = service.generate([])

    assert isinstance(result, str)


def test_generate_answer(service):

    mock_response = MagicMock()
    mock_response.content = "Python is easy to learn."

    service.llm.invoke.return_value = mock_response

    result = service.generate_answer(
        system_prompt="You are helpful.",
        question="What is Python?",
        context=["Python is a programming language."]
    )

    assert result == "Python is easy to learn."
    service.llm.invoke.assert_called_once()
