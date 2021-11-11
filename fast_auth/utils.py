from typing import List


def model_to_dict(obj) -> dict:
    return {key: value for key, value in obj.__dict__.items() if key[0] != "_"}


def models_to_dict(list_models) -> List[dict]:
    return [
        {key: value for key, value in model.__dict__.items() if key[0] != "_"}
        for model in list_models
    ]
