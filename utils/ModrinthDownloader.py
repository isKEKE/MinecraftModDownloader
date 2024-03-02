# _*_ encoding:utf-8 _*_
# Author     : KEKE
# Date       : 2024/3/2
# Description: ...i
import os
import parsel
from tqdm import tqdm
from utils.Crawler import Crawler
from settings import (MOD_VERSION, MOD_API, MOD_SAVE_PATH)
from loguru import logger


class ModrinthDownloader(Crawler):
    def __init__(self, *args, **kwargs):
        super(ModrinthDownloader, self).__init__(*args, **kwargs)

    def set_version_link(self) -> None:
        self.url = f"{self.response.url}/versions?g={self.version}&l={self.api}"
        logger.info(f"download version url: {self.url}")

    def parse(self) -> None:
        root = parsel.Selector(self.response.text)
        jar_url_list = root.xpath('''//div[@class="version-button button-transparent"]/a[1]/@href''').getall()
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

    def run(self) -> None:
        self.send()
        self.set_version_link()
        self.send()
        self.parse()
        if self.url is None:
            return
        self.send()
        self.save_to_local()