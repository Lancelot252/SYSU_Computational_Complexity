"""
计时工具（副本）
"""

import time


class Timer:
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
