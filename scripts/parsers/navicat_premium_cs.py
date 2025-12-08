from typing import Any
from .base_parser import BaseParser


class NavicatPremiumCSParser(BaseParser):
    def parse_version(self, response_data: dict[str, Any]) -> str | None:
        """
        解析响应数据，提取 Navicat 版本号

        Args:
            response_data: API响应数据

        Returns:
            Navicat 版本号字符串，如果解析失败则返回None
        """
        pass

    def parse_deb_url(self, arch: str, response_data: dict[str, Any]) -> str | None:
        """
        解析响应数据，提取 Navicat deb 包 URL

        Args:
            arch: 架构类型（e.g., 'x86_64'）
            response_data: API响应数据

        Returns:
            Navicat deb 包 URL 字符串，如果解析失败则返回None
        """
        pass
