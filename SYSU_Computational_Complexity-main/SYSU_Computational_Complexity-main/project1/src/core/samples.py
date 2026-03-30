from pathlib import Path
from typing import List, Optional

from core.errors import AppError, SampleNotFoundError
from core.models import SampleInfo

TEST_DIR_NAME = "test"


def discover_samples(project_root: Path) -> List[SampleInfo]:
    test_dir = project_root / TEST_DIR_NAME
    if not test_dir.exists() or not test_dir.is_dir():
        return []

    return [
        SampleInfo(
            name=path.name,
            path=path.resolve(),
            relative_path=path.resolve().relative_to(project_root.resolve()),
        )
        for path in sorted(test_dir.iterdir(), key=lambda item: item.name.lower())
        if path.is_file() and path.suffix.lower() == ".json"
    ]


def resolve_sample(project_root: Path, sample_reference: Optional[str]) -> SampleInfo:
    samples = discover_samples(project_root)
    if not samples:
        raise AppError("test 目录下未发现任何 JSON 测试样例。")
    if not sample_reference:
        raise SampleNotFoundError("未提供样例名称或路径。")

    candidates = _collect_reference_candidates(project_root, sample_reference)
    for candidate in candidates:
        if candidate.exists() and candidate.is_file() and candidate.suffix.lower() == ".json":
            resolved = candidate.resolve()
            return SampleInfo(
                name=resolved.name,
                path=resolved,
                relative_path=_relative_or_name(project_root, resolved),
            )

    normalized_reference = sample_reference.replace('\\', '/').lower()
    matches = [
        sample
        for sample in samples
        if sample.name.lower() == normalized_reference
        or sample.relative_path.as_posix().lower() == normalized_reference
        or sample.path.as_posix().lower() == normalized_reference
    ]

    if not matches and not normalized_reference.endswith('.json'):
        matches = [sample for sample in samples if sample.path.stem.lower() == normalized_reference]

    if not matches:
        raise SampleNotFoundError(f"未找到测试样例: {sample_reference}")
    if len(matches) > 1:
        paths = '、'.join(sample.relative_path.as_posix() for sample in matches)
        raise SampleNotFoundError(f"样例引用不唯一: {sample_reference} ({paths})")
    return matches[0]


def _collect_reference_candidates(project_root: Path, sample_reference: str) -> List[Path]:
    raw_reference = Path(sample_reference)
    candidates: List[Path] = []
    if raw_reference.is_absolute():
        candidates.append(raw_reference)
    else:
        candidates.append(project_root / raw_reference)
        candidates.append((project_root / TEST_DIR_NAME) / raw_reference)
    return candidates


def _relative_or_name(project_root: Path, path: Path) -> Path:
    try:
        return path.resolve().relative_to(project_root.resolve())
    except ValueError:
        return Path(path.name)