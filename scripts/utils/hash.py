"""哈希计算工具模块"""

import hashlib
from pathlib import Path
from typing import Callable

from constants.constants import HashAlgorithmEnum


def calculate_file_hash(
    file_path: str | Path, hash_algorithm: str = HashAlgorithmEnum.SHA512.value
) -> str:
    """
    计算文件哈希值

    支持 SHA256 和 SHA512 算法，分块读取大文件避免内存占用过高
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    supported_algorithms: dict[str, Callable[[], hashlib._Hash]] = {
        HashAlgorithmEnum.SHA256.value: hashlib.sha256,
        HashAlgorithmEnum.SHA512.value: hashlib.sha512,
    }

    if hash_algorithm.lower() not in supported_algorithms:
        raise ValueError(
            f"不支持的哈希算法: {hash_algorithm}，支持的算法: {list(supported_algorithms.keys())}"
        )

    hash_func: hashlib._Hash = supported_algorithms[hash_algorithm.lower()]()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def calculate_multiple_hashes(
    file_path: str | Path, algorithms: list[str] | None = None
) -> dict[str, str]:
    """一次性计算文件的多种哈希值"""
    if algorithms is None:
        algorithms = [HashAlgorithmEnum.SHA256.value, HashAlgorithmEnum.SHA512.value]

    results: dict[str, str] = {}
    for algorithm in algorithms:
        results[algorithm] = calculate_file_hash(file_path, algorithm)

    return results


def verify_file_hash(
    file_path: str | Path,
    expected_hash: str,
    hash_algorithm: str = HashAlgorithmEnum.SHA512.value,
) -> bool:
    """验证文件哈希值是否匹配预期值"""
    try:
        actual_hash = calculate_file_hash(file_path, hash_algorithm)
        return actual_hash.lower() == expected_hash.lower()
    except (FileNotFoundError, ValueError):
        return False


def download_and_verify(
    url: str,
    destination: str | Path,
    expected_hash: str,
    hash_algorithm: str = HashAlgorithmEnum.SHA512.value,
) -> bool:
    """下载文件并验证哈希值，失败时自动清理"""
    import httpx

    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        with httpx.stream("GET", url) as response:
            response.raise_for_status()
            with open(destination, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

        return verify_file_hash(destination, expected_hash, hash_algorithm)
    except Exception:
        if destination.exists():
            destination.unlink()
        return False


def format_checksum_for_pkgbuild(checksum: str, arch: str | None = None) -> str:
    """格式化校验和为 PKGBUILD 语法"""
    if arch:
        return f"{HashAlgorithmEnum.SHA512.value}sums_{arch}=('{checksum}')"
    else:
        return f"{HashAlgorithmEnum.SHA512.value}sums=('{checksum}')"
