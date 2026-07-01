from abc import ABC, abstractmethod

from app.models.deletion_models import DeleteMetadata


class DatasetDeletionRepositoryInterface(ABC):
    """
    This interface defines how a repository
    for storing which datasets should be deleted looks

    """

    @abstractmethod
    def mark_dataset_for_deletion(
            self,
            delete_metadata: DeleteMetadata,
    ):
        """
        Create a new record for deleting a dataset

        :param delete_metadata: Delete metadata
        """
        raise NotImplementedError


