from abc import ABC, abstractmethod
from typing import Any
from constants.constants import ArchEnum


class BaseParser(ABC):
    """
    版本抽象基类
    """

    @abstractmethod
    def parse_version(self, response_data: str | Any) -> str | None:
        """
        解析响应数据，提取版本号

        Args:
            response_data: API响应数据

        Returns:
            版本号字符串，如果解析失败则返回None
        """
        pass

    @abstractmethod
    def parse_url(self, arch: ArchEnum | str, response_data: str | Any) -> str | None:
        """
        解析响应数据，提取 deb 包 URL

        Args:
            response_data: API响应数据

        Returns:
            deb 包 URL 字符串，如果解析失败则返回None
        """
        pass
