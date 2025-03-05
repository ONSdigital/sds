from dataclasses import dataclass
from src.app.models.dataset_models import DatasetMetadata
from src.app.models.schema_models import SchemaMetadata


@dataclass
class BaddyData:
    datasets: list[DatasetMetadata]
    schemas: list[SchemaMetadata]