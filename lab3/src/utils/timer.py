"""
计时工具

提供精确的运行时间测量功能。
"""

import time


class Timer:
    """
    计时器，支持上下文管理器用法

    使用方法:
        with Timer() as t:
            # 执行代码
        print(f"耗时: {t.elapsed:.4f} 秒")
    """

    def __init__(self) -> None:
        self.start_time: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self) -> "Timer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, *args) -> None:
        self.elapsed = time.perf_counter() - self.start_time

    def __repr__(self) -> str:
        return f"Timer(elapsed={self.elapsed:.4f}s)"
