"""常量定义模块"""

from enum import Enum

DOWNLOAD_DIR = "downloads"


class ArchEnum(Enum):
    """支持的 CPU 架构"""

    X86_64 = "x86_64"
    AARCH64 = "aarch64"
    LOONG64 = "loong64"
    MIPS64EL = "mips64el"


class PackageEnum(Enum):
    """包标识符枚举"""

    QQ = "qq"
    NAVICAT_PREMIUM_CS = "navicat-premium-cs"


class HashAlgorithmEnum(Enum):
    """哈希算法"""

    SHA256 = "sha256"
    SHA512 = "sha512"

    @classmethod
    def get_all(cls) -> list[str]:
        """获取所有支持的哈希算法"""
        return [algo.value for algo in cls]


class ParserEnum(Enum):
    """解析器名称"""

    QQ = "QQParser"
    NAVICAT_PREMIUM_CS = "NavicatPremiumCSParser"


# Navicat 下载 URL 映射
NAVICAT_URLS = {
    ArchEnum.X86_64: "https://dn.navicat.com/download/navicat17-premium-cs-x86_64.AppImage",
    ArchEnum.AARCH64: "https://dn.navicat.com/download/navicat17-premium-cs-aarch64.AppImage",
}
