import yaml
from pydantic import BaseModel, Field

from constants.constants import ArchEnum


class DownloadSettings(BaseModel):
    """下载设置模型"""

    # 单个包的多架构并行下载数量
    max_concurrent: int = 3
    # 下载重试次数
    max_retries: int = 3
    # 重试基础延迟（秒）
    base_delay: float = 1.0
    # 下载超时时间（秒）
    timeout: int = 30
    # 下载块大小（字节）
    chunk_size: int = 8192
    # 是否显示进度条
    show_progress: bool = True

    class Config:
        extra = "ignore"


class Settings(BaseModel):
    """全局设置模型"""

    download: DownloadSettings = Field(default_factory=DownloadSettings)

    class Config:
        extra = "ignore"


class PackageConfig(BaseModel):
    """包配置模型"""

    name: str
    source: str
    fetch_url: str
    upstream: str
    parser: str
    pkgbuild: str
    arch: list[str] = Field(default_factory=list)
    update_source_url: bool = Field(default=True)

    class Config:
        extra = "ignore"
        validate_by_name = True

    def get_supported_archs(self) -> list[ArchEnum]:
        """将字符串架构列表转换为 ArchEnum 列表"""
        supported_archs = []
        for arch_str in self.arch:
            for arch_enum in ArchEnum:
                if arch_enum.value == arch_str:
                    supported_archs.append(arch_enum)
                    break
        return supported_archs


class ConfigLoader(BaseModel):
    """配置加载器，管理全局设置和包配置"""

    settings: Settings = Field(default_factory=Settings)
    packages: dict[str, PackageConfig] = Field(default_factory=dict)

    class Config:
        extra = "ignore"

    @classmethod
    def load_from_yaml(cls, filepath: str = "config.yaml") -> "ConfigLoader":
        """从 YAML 文件加载配置"""
        with open(filepath, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
