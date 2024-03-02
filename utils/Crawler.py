# _*_ encoding:utf-8 _*_
# Author     : KEKE
# Date       : 2024/3/2
# Description: ...
import requests
from settings import (MOD_SAVE_PATH, MOD_API, MOD_VERSION)


class Crawler(object):
    def __init__(self, url: str, version: str, api: str, to_dir: str):
        self.url = url
        self.version = version
        self.api = api
        self.to_dir = to_dir
        self.response: requests.Response = None

    def send(self) -> None:
        self.response = requests.get(self.url, stream=True)
        self.response.encoding = "utf-8"

    def parse(self) -> None:
        ...

    def run(self) -> None:
        self.send()
        self.parse()