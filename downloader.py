# _*_ encoding:utf-8 _*_
# Author     : KEKE
# Date       : 2024/3/2
# Description: ...
import os
import parsel
from loguru import logger
from items import ModuleInfor, ModuleInforList
from utils import (Crawler, ModrinthDownloader, CurseForgeDownloader)
from settings import (MOD_SAVE_PATH, MOD_API, MOD_VERSION, MOD_INFO_FILE_PATH)


class MinecraftDownloader(Crawler):
    handler = {
        # "CurseForge": CurseForgeDownloader,
        "Modrinth": ModrinthDownloader
    }

    def __init__(self, url: str, version: str = MOD_VERSION, api: str = MOD_API, to_dir: str = MOD_SAVE_PATH,
                 infor_filepath: str = MOD_INFO_FILE_PATH):
        super(MinecraftDownloader, self).__init__(url, version, api, to_dir)
        self.flag = True
        os.path.exists(self.to_dir) or os.makedirs(self.to_dir)
        self.information = ModuleInfor()
        self.information["url"] = url
        self.mod_infor_list = ModuleInforList(infor_filepath)

    def parse(self) -> None:
        root = parsel.Selector(self.response.text)
        self.information["mod_name"] = root.xpath("//h3/text()").get()
        self.information["running_environment"] = root.xpath(
            '''//li[@class="col-lg-4"][contains(text(), "运行环境")]/text()''').get()
        download_source_list = root.xpath('''//ul[@class="common-link-icon-frame common-link-icon-frame-style-3"]/li''')

        for source_li in download_source_list:
            self.information["source"][source_li.xpath("./span/text()").get()] = \
                f'https:{source_li.xpath("./a/@href").get()}'
        self.information["dependencies"] = root.xpath('''//li[@class="col-lg-12 relation"]/ul/li/a/text()''').getall()

    def _downloading(self) -> None:
        for handler_name, handler_cls in self.handler.items():
            source_link = self.information["source"].get(handler_name)
            if source_link is None:
                continue
            logger.info(f"Using {handler_name}")
            if handler_cls(source_link, to_dir=self.to_dir, api=self.api, version=self.version).run() == True:
                break
        else:
            self.flag = False

    def _record_info(self) -> None:
        if self.flag == True:
            self.information["version"] = MOD_VERSION
            self.information.print()
            self.mod_infor_list.add(self.information)
            self.mod_infor_list.save()
        else:
            logger.warning("Download failed.")

    def run(self) -> None:
        super().run()
        self._downloading()
        self._record_info()


if __name__ == "__main__":
    MinecraftDownloader("https://www.mcmod.cn/class/609.html").run()
