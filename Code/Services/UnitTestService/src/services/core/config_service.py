
import json
from attr import fields

@classmethod
def from_json(cls, config_file_path):
    file = json.load(open(config_file_path))
    keys = [f.name for f in fields(cls)]
    # or: keys = cls.__dataclass_fields__.keys()
    json_data = file
    normal_json_data = {key: json_data[key] for key in json_data if key in keys}
    anormal_json_data = {key: json_data[key] for key in json_data if key not in keys}
    tmp = cls(**normal_json_data)
    for anormal_key in anormal_json_data:
        setattr(tmp,anormal_key,anormal_json_data[anormal_key])
    return tmp
