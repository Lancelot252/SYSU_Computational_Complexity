from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class SampleInfo:
    name: str
    path: Path
    relative_path: Path


@dataclass(frozen=True)
class Transition:
    current_state: str
    read_symbol: str
    write_symbol: str
    move: str
    next_state: str


@dataclass(frozen=True)
class EncodedTransition:
    current_state: str
    read_symbol: str
    write_symbol: str
    move: str
    next_state: str
    encoding: str


@dataclass(frozen=True)
class EncodingResult:
    encoding: str
    state_ids: Dict[str, int]
    symbol_ids: Dict[str, int]
    transitions: List[EncodedTransition]