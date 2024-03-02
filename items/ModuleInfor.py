# _*_ encoding:utf-8 _*_
# Author     : KEKE
# Date       : 2024/3/2
# Description: ...
import json
from typing import Dict
from loguru import logger


class ModuleInfor(Dict):
    headers = ["url", "source", "mod_name", "running_environment", "dependencies", "version"]

    def __init__(self):
        super().__init__()
        self.update(Dict.fromkeys(self.headers, None))
        self["source"] = {}

    def append(self, data: dict) -> None:
        print(data)

    def save(self) -> None:
        ...

    def print(self) -> None:
        logger.info(json.dumps(self, ensure_ascii=False, indent=4))