"""
版本比较工具函数
用于比较软件包版本号
"""

from re import split


def parse_version(version: str) -> list[str]:
    """
    解析版本号为可比较的组成部分

    Args:
        version: 版本字符串，如 "3.2.22_251203", "17.3.5"

    Returns:
        版本组成部分列表

    Examples:
        >>> parse_version("3.2.22_251203")
        ['3', '2', '22', '251203']
        >>> parse_version("17.3.5")
        ['17', '3', '5']
    """
    # 移除常见的前缀（如 v, V, r, R 等）
    version = version.lstrip("vVrR")

    # 按照分隔符分割：., -, _, ~
    parts = split(r"[.\-~_]", version)

    # 过滤空字符串
    return [p for p in parts if p]


def compare_versions(version1: str, version2: str) -> int:
    """
    比较两个版本号

    Args:
        version1: 第一个版本号
        version2: 第二个版本号

    Returns:
        -1: version1 < version2
         0: version1 == version2
         1: version1 > version2

    Examples:
        >>> compare_versions("3.2.21", "3.2.22")
        -1
        >>> compare_versions("3.2.22", "3.2.22")
        0
        >>> compare_versions("3.2.23", "3.2.22")
        1
        >>> compare_versions("3.2.22_251203", "3.2.22")
        1
    """
    v1_parts = parse_version(version1)
    v2_parts = parse_version(version2)

    # 逐个比较版本号部分
    max_len = max(len(v1_parts), len(v2_parts))

    for i in range(max_len):
        # 获取版本号部分，如果不存在则视为 0
        v1_part = v1_parts[i] if i < len(v1_parts) else "0"
        v2_part = v2_parts[i] if i < len(v2_parts) else "0"

        # 尝试作为数字比较
        try:
            v1_num = int(v1_part)
            v2_num = int(v2_part)

            if v1_num < v2_num:
                return -1
            elif v1_num > v2_num:
                return 1
        except ValueError:
            # 如果无法转换为数字，则按字符串比较
            if v1_part < v2_part:
                return -1
            elif v1_part > v2_part:
                return 1

    # 所有部分都相等
    return 0
