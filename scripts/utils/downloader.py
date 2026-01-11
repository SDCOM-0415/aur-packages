"""
异步文件下载器
支持并行下载、智能重试和进度条显示
"""

import asyncio
import time
from dataclasses import dataclass
from httpx import AsyncClient
from pathlib import Path
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


@dataclass(frozen=True)
class DownloadResult:
    """下载结果"""

    arch: str
    success: bool
    file_path: Path | None = None
    error: str | None = None
    retry_count: int = 0
    download_time: float = 0.0
    downloaded_size: int = 0


class Downloader:
    """
    现代化异步下载器

    特性：
    - 异步并发下载（asyncio + httpx）
    - 智能重试（指数退避）
    - 流式下载（内存高效）
    - Rich 进度条（实时显示速度、进度、剩余时间）
    - 完整类型注解
    """

    def __init__(
        self,
        client: AsyncClient,
        *,
        max_concurrent: int = 3,
        max_retries: int = 3,
        base_delay: float = 1.0,
        chunk_size: int = 8192,
        show_progress: bool = True,
    ) -> None:
        self.client = client
        self.max_concurrent = max_concurrent
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.chunk_size = chunk_size
        self.show_progress = show_progress
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def download_file(
        self,
        url: str,
        file_path: Path,
        *,
        arch: str = "unknown",
    ) -> DownloadResult:
        """下载单个文件（支持智能重试）"""
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    delay = self.base_delay * (2 ** (attempt - 1))
                    await asyncio.sleep(delay)

                start_time = time.perf_counter()
                file_path.parent.mkdir(parents=True, exist_ok=True)

                async with self._semaphore, self.client.stream("GET", url) as response:
                    response.raise_for_status()

                    downloaded_size = 0
                    with file_path.open("wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=self.chunk_size):
                            f.write(chunk)
                            downloaded_size += len(chunk)

                download_time = time.perf_counter() - start_time

                return DownloadResult(
                    arch=arch,
                    success=True,
                    file_path=file_path,
                    retry_count=attempt,
                    download_time=download_time,
                    downloaded_size=downloaded_size,
                )

            except Exception as e:
                if attempt == self.max_retries:
                    return DownloadResult(
                        arch=arch,
                        success=False,
                        error=str(e),
                        retry_count=attempt,
                    )

        return DownloadResult(
            arch=arch,
            success=False,
            error="Max retries exceeded",
            retry_count=self.max_retries,
        )

    async def download_file_with_progress(
        self,
        url: str,
        file_path: Path,
        progress: Progress,
        task_id: TaskID,
        *,
        arch: str = "unknown",
    ) -> DownloadResult:
        """
        下载单个文件（带实时进度更新）

        这个方法专门用于 Rich 进度条，会实时更新下载进度
        """
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    delay = self.base_delay * (2 ** (attempt - 1))
                    await asyncio.sleep(delay)

                start_time = time.perf_counter()
                file_path.parent.mkdir(parents=True, exist_ok=True)

                async with self._semaphore, self.client.stream("GET", url) as response:
                    response.raise_for_status()

                    # 获取文件总大小（用于进度条）
                    content_length = response.headers.get("content-length")
                    total_size = int(content_length) if content_length else None

                    # 更新进度条的总大小并启动任务
                    if total_size:
                        progress.update(task_id, total=total_size)
                        progress.start_task(task_id)

                    downloaded_size = 0
                    with file_path.open("wb") as f:
                        async for chunk in response.aiter_bytes(chunk_size=self.chunk_size):
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            # 实时更新进度条（包括速度）
                            progress.update(task_id, advance=len(chunk), refresh=True)

                download_time = time.perf_counter() - start_time

                return DownloadResult(
                    arch=arch,
                    success=True,
                    file_path=file_path,
                    retry_count=attempt,
                    download_time=download_time,
                    downloaded_size=downloaded_size,
                )

            except Exception as e:
                if attempt == self.max_retries:
                    return DownloadResult(
                        arch=arch,
                        success=False,
                        error=str(e),
                        retry_count=attempt,
                    )

        return DownloadResult(
            arch=arch,
            success=False,
            error="Max retries exceeded",
            retry_count=self.max_retries,
        )

    async def download_all(
        self,
        downloads: dict[str, tuple[str, Path]],
        package_name: str = "package",
    ) -> dict[str, DownloadResult]:
        """
        并行下载多个文件（带进度条）

        Args:
            downloads: {arch: (url, file_path)} 字典
            package_name: 包名称（用于进度条标题）

        Returns:
            {arch: DownloadResult} 字典
        """
        if not downloads:
            return {}

        results: dict[str, DownloadResult] = {}

        if not self.show_progress:
            # 不显示进度条，直接并发下载
            tasks = [
                self.download_file(url, file_path, arch=arch)
                for arch, (url, file_path) in downloads.items()
            ]
            completed_results = await asyncio.gather(*tasks)

            for arch, result in zip(downloads.keys(), completed_results):
                results[arch] = result

            return results

        # 显示 Rich 进度条
        # 配置进度条列：描述、进度条、百分比、下载量、速度、剩余时间
        progress = Progress(
            TextColumn("[bold blue]{task.description}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            refresh_per_second=10,  # 每秒刷新 10 次，确保速度显示流畅
        )

        with progress:
            # 为每个下载任务创建独立的进度条任务
            tasks = []
            for arch, (url, file_path) in downloads.items():
                task_id = progress.add_task(
                    f"[{package_name}] {arch}",
                    total=None,  # 初始时未知总大小，等待 HTTP 响应
                )
                tasks.append(
                    self.download_file_with_progress(
                        url, file_path, progress, task_id, arch=arch
                    )
                )

            # 并发执行所有下载任务
            completed_results = await asyncio.gather(*tasks)

            # 收集结果
            for arch, result in zip(downloads.keys(), completed_results):
                results[arch] = result

        return results
