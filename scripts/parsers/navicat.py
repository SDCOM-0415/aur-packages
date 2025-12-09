from typing import Any
import re
from constants.constants import ArchEnum, NAVICAT_URLS
from .base_parser import BaseParser


class NavicatPremiumCSParser(BaseParser):
    def parse_version(self, response_data: str | Any) -> str | None:
        """
        解析响应数据，提取 Navicat 版本号

        Args:
            response_data: API响应数据

        Returns:
            Navicat 版本号字符串，如果解析失败则返回None
        """
        pattern = r"(Navicat[^()]*\(Linux\)[^v]*version[^\d]*)(\d+\.\d+\.\d+)"
        matched = re.search(pattern, response_data, re.IGNORECASE)
        if matched:
            return matched.group(2)
        return None

    def parse_url(self, arch: ArchEnum | str, response_data: str | Any) -> str | None:
        """
        解析响应数据，提取 Navicat deb 包 URL

        Args:
            arch: 架构类型（e.g., 'x86_64'）
            response_data: API响应数据

        Returns:
            Navicat deb 包 URL 字符串，如果解析失败则返回None
        """

        # 特殊情况，直接写死URL映射
        match arch:
            case ArchEnum.X86_64:
                return NAVICAT_URLS[ArchEnum.X86_64]
            case ArchEnum.AARCH64:
                return NAVICAT_URLS[ArchEnum.AARCH64]
            case _:
                return None

        pass
