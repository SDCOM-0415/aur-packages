"""
高级文件下载器
支持并行下载、进度显示和智能重试机制
"""

import asyncio
import time
from dataclasses import dataclass
from httpx import AsyncClient
from pathlib import Path


@dataclass(frozen=True)
class DownloadResult:
    """下载结果（不可变）"""

    arch: str
    success: bool
    file_path: Path | None = None
    error: str | None = None
    retry_count: int = 0
    download_time: float = 0.0


class Downloader:
    """
    现代化异步下载器

    特性：
    - 使用 TaskGroup 进行结构化并发（Python 3.11+）
    - 智能重试机制（指数退避）
    - 流式下载，内存高效
    - 完整的类型注解
    """

    def __init__(
        self,
        client: AsyncClient,
        *,
        max_concurrent: int = 3,
        max_retries: int = 3,
        base_delay: float = 1.0,
        show_progress: bool = True,
        chunk_size: int = 8192,
    ) -> None:
        """
        初始化下载器

        Args:
            client: httpx AsyncClient 实例
            max_concurrent: 最大并发下载数
            max_retries: 最大重试次数
            base_delay: 重试基础延迟（秒）
            show_progress: 是否显示进度
            chunk_size: 下载块大小（字节）
        """
        self.client = client
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.show_progress = show_progress
        self.chunk_size = chunk_size
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def download_file(
        self,
        url: str,
        file_path: Path,
        *,
        arch: str = "unknown",
    ) -> DownloadResult:
        """
        下载单个文件（支持智能重试）

        Args:
            url: 下载 URL
            file_path: 保存路径
            arch: 架构名称（用于日志）

        Returns:
            DownloadResult
        """
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    delay = self.base_delay * (2 ** (attempt - 1))
                    if self.show_progress:
                        print(
                            f"    [{arch}] 重试 {attempt}/{self.max_retries} (延迟 {delay:.1f}s)..."
                        )
                    await asyncio.sleep(delay)

                start_time = time.perf_counter()
                file_path.parent.mkdir(parents=True, exist_ok=True)

                async with self._semaphore, self.client.stream("GET", url) as response:
                    response.raise_for_status()

                    total_size = int(response.headers.get("content-length", 0))
                    downloaded_size = 0

                    with file_path.open("wb") as f:
                        async for chunk in response.aiter_bytes(
                            chunk_size=self.chunk_size
                        ):
                            f.write(chunk)
                            downloaded_size += len(chunk)

                            if self.show_progress and total_size > 0:
                                self._show_progress(arch, downloaded_size, total_size)

                download_time = time.perf_counter() - start_time

                if self.show_progress:
                    speed = downloaded_size / download_time if download_time > 0 else 0
                    print(
                        f"    [{arch}] 下载完成! "
                        f"大小: {self._format_size(downloaded_size)}, "
                        f"耗时: {download_time:.2f}s, "
                        f"速度: {self._format_size(speed)}/s"
                    )

                return DownloadResult(
                    arch=arch,
                    success=True,
                    file_path=file_path,
                    retry_count=attempt,
                    download_time=download_time,
                )

            except Exception as e:
                if attempt == self.max_retries:
                    if self.show_progress:
                        print(f"    [{arch}] 下载失败: {e}")
                    return DownloadResult(
                        arch=arch,
                        success=False,
                        error=str(e),
                        retry_count=attempt,
                    )

        # 理论上不会到达这里
        return DownloadResult(
            arch=arch,
            success=False,
            error="Max retries exceeded",
            retry_count=self.max_retries,
        )

    async def download_all(
        self,
        downloads: dict[str, tuple[str, Path]],
    ) -> dict[str, DownloadResult]:
        """
        并行下载多个文件（使用 TaskGroup）

        Args:
            downloads: {arch: (url, file_path)} 字典

        Returns:
            {arch: DownloadResult} 字典
        """
        if not downloads:
            return {}

        if self.show_progress:
            print(
                f"\n  并行下载 {len(downloads)} 个文件（并发: {self.max_concurrent}）..."
            )

        results: dict[str, DownloadResult] = {}

        # 使用 TaskGroup 进行结构化并发（Python 3.11+）
        async def download_task(arch: str, url: str, file_path: Path) -> None:
            result = await self.download_file(url, file_path, arch=arch)
            results[arch] = result

        async with asyncio.TaskGroup() as tg:
            for arch, (url, file_path) in downloads.items():
                tg.create_task(download_task(arch, url, file_path))

        return results

    def _show_progress(self, arch: str, downloaded: int, total: int) -> None:
        """显示下载进度"""
        progress = (downloaded / total) * 100
        print(
            f"    [{arch}] 下载中... {progress:.1f}% "
            f"({self._format_size(downloaded)}/{self._format_size(total)})"
        )

    @staticmethod
    def _format_size(size: int | float) -> str:
        """
        格式化文件大小

        Args:
            size: 字节数

        Returns:
            格式化后的字符串（如 "1.5MB"）
        """
        size_float = float(size)

        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size_float < 1024:
                return f"{size_float:.1f}{unit}"
            size_float /= 1024

        return f"{size_float:.1f}PB"
