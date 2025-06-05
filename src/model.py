from dataclasses import dataclass
from typing import Union


@dataclass
class KVPair:
    key: str
    value: Union[str, int, float, bool, None]
