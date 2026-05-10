from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


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


# ============ 多带图灵机和UTM相关模型 ============

@dataclass
class Tape:
    """磁带类，模拟图灵机的单条磁带"""
    content: List[str] = field(default_factory=lambda: [" "])  # 磁带内容，默认一个空符号
    head_position: int = 0  # 磁头位置
    
    def __post_init__(self):
        """确保磁带至少有一个符号"""
        if not self.content:
            self.content = [" "]
    
    def read(self) -> str:
        """读取当前磁头位置的符号"""
        if 0 <= self.head_position < len(self.content):
            return self.content[self.head_position]
        return " "  # 超出范围返回空符号
    
    def write(self, symbol: str):
        """在当前磁头位置写入符号"""
        # 如果需要，扩展磁带
        while self.head_position < 0:
            self.content.insert(0, " ")
            self.head_position = 0
        while self.head_position >= len(self.content):
            self.content.append(" ")
        self.content[self.head_position] = symbol
    
    def move(self, direction: str):
        """移动磁头"""
        if direction == "left":
            self.head_position -= 1
            if self.head_position < 0:
                self.content.insert(0, " ")
                self.head_position = 0
        elif direction == "right":
            self.head_position += 1
            if self.head_position >= len(self.content):
                self.content.append(" ")
        # "stay" 不移动
    
    def get_display_content(self, padding: int = 5) -> Tuple[str, int]:
        """
        获取用于显示的磁带内容和磁头位置
        
        Args:
            padding: 磁带头尾的空符号数量
            
        Returns:
            (显示内容, 磁头在显示内容中的位置)
        """
        # 确保前后有足够的空符号
        display_content = [" "] * padding + self.content + [" "] * padding
        head_display_pos = padding + self.head_position
        return "".join(display_content), head_display_pos
    
    def __str__(self) -> str:
        """返回磁带的字符串表示"""
        content, head_pos = self.get_display_content()
        return content


@dataclass
class MultiTapeTransition:
    """多带图灵机的转移规则"""
    current_state: str
    read_symbols: Tuple[str, ...]  # 每条磁带读取的符号
    write_symbols: Tuple[str, ...]  # 每条磁带写入的符号
    moves: Tuple[str, ...]  # 每条磁带的移动方向
    next_state: str


@dataclass
class UTMTransition:
    """UTM解析出的转移规则"""
    current_state_id: int
    read_symbol_id: int
    next_state_id: int
    write_symbol_id: int
    move_id: int  # 1=left, 2=right, 3=stay


@dataclass
class UTMState:
    """UTM运行状态"""
    stage: str  # 当前阶段
    step_count: int = 0  # 步数计数
    accepted: bool = False  # 是否接受
    halted: bool = False  # 是否停机