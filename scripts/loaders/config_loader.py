import yaml
from pydantic import BaseModel, Field

from constants.constants import ArchEnum


class PackageConfig(BaseModel):
    name: str = Field(..., description="name")
    source: str
    fetch_url: str
    upstream: str
    parser: str
    pkgbuild: str
    arch: list[str] = Field(default_factory=list, description="支持的架构列表")
    update_source_url: bool = Field(
        default=True, description="是否更新PKGBUILD中的source URL"
    )
    force_update_hash: bool = Field(
        default=False, description="是否强制更新哈希值（即使版本未变化）"
    )

    class Config:
        # 允许通过 . 访问属性
        extra = "ignore"
        validate_by_name = True

    def get_supported_archs(self) -> list[ArchEnum]:
        """获取支持的架构枚举列表"""
        supported_archs = []
        for arch_str in self.arch:
            for arch_enum in ArchEnum:
                if arch_enum.value == arch_str:
                    supported_archs.append(arch_enum)
                    break
        return supported_archs


class ConfigLoader(BaseModel):
    packages: dict[str, PackageConfig]

    class Config:
        extra = "ignore"

    @classmethod
    def load_from_yaml(cls, filepath: str = "packages.yaml") -> "ConfigLoader":
        """从 YAML 文件加载"""
        with open(filepath, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)
