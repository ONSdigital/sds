from fastapi import status

from tests.test_data import dataset_test_data


def test_post_collection_exercise_end_200_response(dataset_collection_mock, deletion_collection_mock, test_client):
    """
    When a valid collection exercise end message is posted with a dataset_guid,
    the endpoint must return 200 with an accepted message.
    """
    response = test_client.post(
        "/collection-exercise-end",
        json=dataset_test_data.test_data_collection_end.__dict__,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "accepted"}


def test_post_collection_exercise_end_missing_dataset_guid_200_response(test_client):
    """
    When a collection exercise end message is posted without a dataset_guid,
    the endpoint must still return 200 (no deletion is triggered but the message is accepted).
    """
    response = test_client.post(
        "/collection-exercise-end",
        json=dataset_test_data.test_data_collection_end_missing_id.__dict__,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "accepted"}

