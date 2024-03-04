# _*_ encoding:utf-8 _*_
# Author     : KEKE
# Date       : 2024/3/2
# Description: ...i
import os
import parsel
import requests
from tqdm import tqdm
from utils.Crawler import Crawler
from settings import (MOD_VERSION, MOD_API, MOD_SAVE_PATH)
from loguru import logger


class CurseForgeDownloader(Crawler):
    api_id = {
        "forge": "1",
        "fabric": "4",
        "quilt": "5"
    }

    def __init__(self, *args, **kwargs):
        super(CurseForgeDownloader, self).__init__(*args, **kwargs)
        self.session = requests.session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"

    def send(self) -> None:
        self.response = self.session.get(self.url, stream=True)
        self.response.encoding = "utf-8"

    def set_version_link(self) -> None:
        self.url = f"{self.response.url}/files/all?page=1&pageSize=20&version={self.version}&gameVersionTypeId={self.api_id.get(self.api.lower())}"
        logger.info(f"download version url: {self.url}")

    def parse(self) -> None:
        root = parsel.Selector(self.response.text)
        jar_url_list = root.xpath('''//a[class="file-card"]/@href''').getall()
        if len(jar_url_list) == 0:
            logger.warning(f"There is no download link for the {self.version} of this mod.")
            self.url = None
        else:
            logger.info(jar_url_list)
            self.url = jar_url_list[0]

    def save_to_local(self) -> None:
        file_length = int(self.response.headers.get("Content-Length", 0))
        filename = os.path.split(self.url)[-1].replace("%2B", "-")
        filepath = os.path.join(self.to_dir, filename)

        with open(filepath, "wb") as fp:
            with tqdm(total=file_length, unit='B', unit_scale=True) as pbar:
                for chunk in self.response.iter_content(1024):
                    fp.write(chunk)
                    pbar.update(1024)

        logger.info(f"Saved: {os.path.abspath(filepath)}")

    def run(self) -> bool:
        self.send()
        self.set_version_link()
        self.send()
        print(self.session.headers)
        self.send()
        self.parse()
        # if self.url is None:
        #     return False
        # self.send()
        # self.save_to_local()
        # return True