from unittest.mock import MagicMock, patch

import pytest
from google.cloud import exceptions as gcp_exceptions

from app.exception.exceptions import ExceptionTopicNotFound
from app.services.shared.publisher_service import PublisherService
from tests.test_data import schema_test_data


# --------------------------------------------------------------------------- #
# __init__
# --------------------------------------------------------------------------- #

def test_publisher_service_init_sets_publisher_client(publisher_service_factory):
    """
    When PublisherService is initialised, the publisher_client attribute must be set.
    """
    service, publisher_client = publisher_service_factory()

    assert service.publisher_client is publisher_client


def test_publisher_service_init_in_docker_dev_creates_topic_when_not_found():
    """
    When CONF is 'docker-dev' and the topic does not exist, __init__ must create the topic.
    """
    publisher_client = MagicMock()
    publisher_client.topic_path.return_value = "projects/mock/topics/mock-topic"
    # Simulate topic not found on get_topic
    publisher_client.get_topic.side_effect = gcp_exceptions.NotFound("not found")

    with patch("app.services.shared.publisher_service.settings") as mock_settings:
        mock_settings.PROJECT_ID = "mock-project"
        mock_settings.PUBLISH_SCHEMA_TOPIC_ID = "mock-topic"
        mock_settings.CONF = "docker-dev"
        service = PublisherService(publisher_client)

    publisher_client.create_topic.assert_called_once_with(
        request={"name": "projects/mock/topics/mock-topic"}
    )


def test_publisher_service_init_in_docker_dev_does_not_create_topic_when_found():
    """
    When CONF is 'docker-dev' and the topic already exists, __init__ must not create the topic.
    """
    publisher_client = MagicMock()
    publisher_client.topic_path.return_value = "projects/mock/topics/mock-topic"
    publisher_client.get_topic.return_value = MagicMock()  # topic exists

    with patch("app.services.shared.publisher_service.settings") as mock_settings:
        mock_settings.PROJECT_ID = "mock-project"
        mock_settings.PUBLISH_SCHEMA_TOPIC_ID = "mock-topic"
        mock_settings.CONF = "docker-dev"
        service = PublisherService(publisher_client)

    publisher_client.create_topic.assert_not_called()


# --------------------------------------------------------------------------- #
# publish_data_to_topic
# --------------------------------------------------------------------------- #

def test_publish_data_to_topic_publishes_serialised_metadata(publisher_service_factory):
    """
    When publish_data_to_topic is called with valid metadata, it must encode the
    metadata and call publisher_client.publish once with the correct payload.
    """
    import json

    service, publisher_client = publisher_service_factory()
    publisher_client.topic_path.return_value = "projects/mock/topics/mock-topic"
    publisher_client.get_topic.return_value = MagicMock()

    with patch("app.services.shared.publisher_service.settings") as mock_settings:
        mock_settings.PROJECT_ID = "mock-project"
        mock_settings.PUBLISH_SCHEMA_TOPIC_ID = "mock-topic"
        mock_settings.CONF = "unit"
        service.publish_data_to_topic(
            schema_test_data.test_schema_metadata_1,
            "mock-topic",
        )

    publisher_client.publish.assert_called_once()
    call_kwargs = publisher_client.publish.call_args
    published_dict = json.loads(call_kwargs[1]["data"].decode("utf-8"))
    assert published_dict == schema_test_data.test_schema_metadata_1.__dict__


def test_publish_data_to_topic_raises_runtime_error_on_publish_failure(publisher_service_factory):
    """
    When publisher_client.publish raises RuntimeError, publish_data_to_topic must
    re-raise a RuntimeError.
    """
    service, publisher_client = publisher_service_factory()
    publisher_client.topic_path.return_value = "projects/mock/topics/mock-topic"
    publisher_client.get_topic.return_value = MagicMock()
    publisher_client.publish.side_effect = RuntimeError("publish failed")

    with patch("app.services.shared.publisher_service.settings") as mock_settings:
        mock_settings.PROJECT_ID = "mock-project"
        mock_settings.PUBLISH_SCHEMA_TOPIC_ID = "mock-topic"
        mock_settings.CONF = "unit"
        with pytest.raises(RuntimeError, match="Error publishing message"):
            service.publish_data_to_topic(
                schema_test_data.test_schema_metadata_1,
                "mock-topic",
            )


# --------------------------------------------------------------------------- #
# _verify_topic_exists
# --------------------------------------------------------------------------- #

def test_verify_topic_exists_returns_true_when_topic_found(publisher_service_factory):
    """
    When get_topic succeeds, _verify_topic_exists must return True.
    """
    service, publisher_client = publisher_service_factory()

    with patch("app.services.shared.publisher_service.settings") as mock_settings:
        mock_settings.CONF = "unit"
        result = service._verify_topic_exists("projects/mock/topics/mock-topic")

    assert result is True


def test_verify_topic_exists_raises_exception_topic_not_found_in_non_docker_dev(publisher_service_factory):
    """
    When get_topic raises NotFound and CONF is not 'docker-dev',
    _verify_topic_exists must raise ExceptionTopicNotFound.
    """
    service, publisher_client = publisher_service_factory()
    publisher_client.get_topic.side_effect = gcp_exceptions.NotFound("not found")

    with patch("app.services.shared.publisher_service.settings") as mock_settings:
        mock_settings.CONF = "unit"
        with pytest.raises(ExceptionTopicNotFound):
            service._verify_topic_exists("projects/mock/topics/mock-topic")


def test_verify_topic_exists_returns_false_in_docker_dev_when_not_found(publisher_service_factory):
    """
    When get_topic raises NotFound and CONF is 'docker-dev',
    _verify_topic_exists must return False instead of raising.
    """
    service, publisher_client = publisher_service_factory()
    publisher_client.get_topic.side_effect = gcp_exceptions.NotFound("not found")

    with patch("app.services.shared.publisher_service.settings") as mock_settings:
        mock_settings.CONF = "docker-dev"
        result = service._verify_topic_exists("projects/mock/topics/mock-topic")

    assert result is False


# --------------------------------------------------------------------------- #
# _create_topic
# --------------------------------------------------------------------------- #

def test_create_topic_calls_publisher_client(publisher_service_factory):
    """
    _create_topic must call publisher_client.create_topic with the correct topic path.
    """
    service, publisher_client = publisher_service_factory()
    topic_path = "projects/mock/topics/new-topic"

    service._create_topic(topic_path)

    publisher_client.create_topic.assert_called_once_with(request={"name": topic_path})

