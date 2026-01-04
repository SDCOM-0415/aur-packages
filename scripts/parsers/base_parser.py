from abc import ABC, abstractmethod
from typing import Any
from constants.constants import ArchEnum


class BaseParser(ABC):
    """解析器抽象基类，定义版本号和URL解析接口"""

    @abstractmethod
    def parse_version(self, response_data: str | Any) -> str | None:
        """从响应数据中提取版本号"""
        pass

    @abstractmethod
    def parse_url(self, arch: ArchEnum | str, response_data: str | Any) -> str | None:
        """从响应数据中提取下载 URL"""
        pass
