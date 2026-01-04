import yaml
from pydantic import BaseModel, Field

from constants.constants import ArchEnum


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
    """配置加载器，管理所有包配置"""

    packages: dict[str, PackageConfig]

    class Config:
        extra = "ignore"

    @classmethod
    def load_from_yaml(cls, filepath: str = "packages.yaml") -> "ConfigLoader":
        """从 YAML 文件加载配置"""
        with open(filepath, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
