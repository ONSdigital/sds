from database import get_data, set_data


dataset_id = "1"

unit_id = "2"

data = {
    "unit_id": unit_id
}

set_data(dataset_id, data)

data = get_data(dataset_id, unit_id)

print(data)
