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
    headers = ["url", "source", "mod_name", "running_environment", "dependencies", "version"]

    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath
        if os.path.exists(self.filepath):
            mod_infor_df = pandas.read_csv(self.filepath, encoding="ansi")
            for _, mod_infor in mod_infor_df.iterrows():
                mod_infor = mod_infor.to_dict()
                for key, val in mod_infor.items():
                    mod_infor[key] = json.loads(val)
                self[mod_infor.get("url")] = mod_infor

    def add(self, __object: ModuleInfor) -> None:
        if not isinstance(__object, ModuleInfor):
            logger.warning(f"The object `{__object}` doesn't belong class ModuleInfor.")
        else:
            if __object.get("url") is None:
                logger.warning("The url is null")
            else:
                self[__object.get("url")] = __object
    @logger.catch()
    def save(self) -> None:
        print(json.dumps(list(self.values()), indent=4))
        mod_infor_df = pandas.DataFrame(list(self.values()), columns=self.headers, index=[0])
        mod_infor_df.to_csv(self.filepath, index=None)

    def __str__(self) -> str:
        return json.dumps(self, indent=4, ensure_ascii=False)

    def __repr__(self) -> str:
        return str(self)


if __name__ == "__main__":
    from settings import MOD_INFO_FILE_PATH

    mod_infor_list = ModuleInforList(filepath=MOD_INFO_FILE_PATH)
    mod_infor_list.add(None)
    mod_infor_list.add(ModuleInfor())
    mod_infor_list.save()
