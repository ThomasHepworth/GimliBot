import json
from functools import lru_cache
from typing import Tuple


@lru_cache(maxsize=None)
def parse_json(config_path: str) -> Tuple[str, str]:
    with open(config_path, "r") as file:
        config = json.load(file)
    return config
