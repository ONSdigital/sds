from database import get_data, set_data
from constants import UNIT_ID

dataset_id = "1"

unit_id = "2"

data = {
    UNIT_ID: unit_id
}

set_data(dataset_id, data)

data = get_data(dataset_id, unit_id)

print(data)
