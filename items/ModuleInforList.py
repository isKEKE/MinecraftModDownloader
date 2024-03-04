# _*_ encoding:utf-8 _*_
# Author     : KEKE
# Date       : 2024/3/2
# Description: ...
import json
import os.path

import pandas
from loguru import logger
from typing import Dict
from items.ModuleInfor import ModuleInfor


class ModuleInforList(Dict):
    headers = ["url", "mod_name", "running_environment", "version"]

    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath
        if os.path.exists(self.filepath):
            try:
                mod_infor_df = pandas.read_csv(self.filepath, encoding="ansi")
            except UnicodeError:
                mod_infor_df = pandas.read_csv(self.filepath, encoding="utf-8")
            for _, mod_infor in mod_infor_df.iterrows():
                mod_infor = mod_infor.to_dict()
                self[mod_infor.get("url")] = mod_infor

    def add(self, __object: ModuleInfor) -> None:
        if not isinstance(__object, ModuleInfor):
            logger.warning(f"The object `{__object}` doesn't belong class ModuleInfor.")
        else:
            if __object.get("url") is None:
                logger.warning("The url is null")
            else:
                for key in set(__object.headers) - set(self.headers):
                    __object.pop(key)
                self[__object.get("url")] = __object

    @logger.catch()
    def save(self) -> None:
        mod_infor_df = pandas.DataFrame(list(self.values()), columns=self.headers)
        mod_infor_df.to_csv(self.filepath, index=None)

    def __str__(self) -> str:
        return json.dumps(self, indent=4, ensure_ascii=False)

    def __repr__(self) -> str:
        return str(self)
