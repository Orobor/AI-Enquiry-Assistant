import logging
import pytest


# Create your tests here.
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_error_logging():
    try:
        raise ValueError("Testing Django exception logging")

    except Exception as ex:
        logger.exception(
            "Test exception captured: %s", ex
        )
