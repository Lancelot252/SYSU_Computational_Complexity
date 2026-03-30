"""
多带图灵机模块

实现多带图灵机模拟器，支持：
- 多条磁带和多个磁头
- 状态转移
- 交互式和自动两种展示模式
"""

import time
from typing import Dict, List, Optional, Tuple

from core.models import Tape, MultiTapeTransition
from core.errors import AppError


# 空符号
BLANK_SYMBOL = " "
# 分隔符，用于磁带显示
TAPE_SEPARATOR = "-" * 40


class MultiTapeTM:
    """多带图灵机类"""
    
    def __init__(self, num_tapes: int, initial_state: str, accept_states: Optional[set] = None):
        """
        初始化多带图灵机
        
        Args:
            num_tapes: 磁带数量
            initial_state: 初始状态
            accept_states: 接受状态集合，如果为None则停机状态即为接受
        """
        if num_tapes < 1:
            raise ValueError("磁带数量必须至少为1")
        
        self.num_tapes = num_tapes
        self.tapes: List[Tape] = [Tape() for _ in range(num_tapes)]
        self.current_state = initial_state
        self.initial_state = initial_state
        self.accept_states = accept_states or set()
        self.transitions: Dict[Tuple[str, Tuple[str, ...]], MultiTapeTransition] = {}
        self.halted = False
        self.step_count = 0
    
    def set_tape(self, tape_index: int, content: str, head_position: int = 0):
        """
        设置指定磁带的内容和磁头位置
        
        Args:
            tape_index: 磁带索引（从0开始）
            content: 磁带内容字符串
            head_position: 磁头初始位置（默认为0）
        """
        if not 0 <= tape_index < self.num_tapes:
            raise IndexError(f"磁带索引 {tape_index} 超出范围 [0, {self.num_tapes - 1}]")
        
        # 将字符串转换为字符列表
        if content:
            self.tapes[tape_index].content = list(content)
        else:
            self.tapes[tape_index].content = [BLANK_SYMBOL]
        
        self.tapes[tape_index].head_position = head_position
    
    def add_transition(
        self,
        current_state: str,
        read_symbols: Tuple[str, ...],
        write_symbols: Tuple[str, ...],
        moves: Tuple[str, ...],
        next_state: str
    ):
        """
        添加转移规则
        
        Args:
            current_state: 当前状态
            read_symbols: 每条磁带读取的符号元组
            write_symbols: 每条磁带写入的符号元组
            moves: 每条磁带的移动方向元组 ("left", "right", "stay")
            next_state: 下一状态
        """
        if len(read_symbols) != self.num_tapes:
            raise ValueError(f"读取符号数量 {len(read_symbols)} 与磁带数量 {self.num_tapes} 不匹配")
        if len(write_symbols) != self.num_tapes:
            raise ValueError(f"写入符号数量 {len(write_symbols)} 与磁带数量 {self.num_tapes} 不匹配")
        if len(moves) != self.num_tapes:
            raise ValueError(f"移动方向数量 {len(moves)} 与磁带数量 {self.num_tapes} 不匹配")
        
        transition = MultiTapeTransition(
            current_state=current_state,
            read_symbols=read_symbols,
            write_symbols=write_symbols,
            moves=moves,
            next_state=next_state
        )
        
        key = (current_state, read_symbols)
        self.transitions[key] = transition
    
    def get_current_symbols(self) -> Tuple[str, ...]:
        """获取所有磁带当前磁头位置的符号"""
        return tuple(tape.read() for tape in self.tapes)
    
    def step(self) -> bool:
        """
        执行一步转移
        
        Returns:
            是否成功执行转移（False表示无匹配转移，即停机）
        """
        if self.halted:
            return False
        
        current_symbols = self.get_current_symbols()
        key = (self.current_state, current_symbols)
        
        if key not in self.transitions:
            # 无匹配转移，停机
            self.halted = True
            return False
        
        transition = self.transitions[key]
        
        # 执行写入和移动
        for i, tape in enumerate(self.tapes):
            tape.write(transition.write_symbols[i])
            tape.move(transition.moves[i])
        
        # 更新状态
        self.current_state = transition.next_state
        self.step_count += 1
        
        # 检查是否进入接受状态
        if self.current_state in self.accept_states:
            self.halted = True
        
        return True
    
    def is_accepted(self) -> bool:
        """判断是否被接受"""
        return self.current_state in self.accept_states
    
    def is_halted(self) -> bool:
        """判断是否已停机"""
        return self.halted
    
    def get_state(self) -> str:
        """获取当前状态"""
        return self.current_state
    
    def get_tape_content(self, tape_index: int) -> str:
        """获取指定磁带的内容"""
        if not 0 <= tape_index < self.num_tapes:
            raise IndexError(f"磁带索引 {tape_index} 超出范围")
        return "".join(self.tapes[tape_index].content)
    
    def get_head_position(self, tape_index: int) -> int:
        """获取指定磁带的磁头位置"""
        if not 0 <= tape_index < self.num_tapes:
            raise IndexError(f"磁带索引 {tape_index} 超出范围")
        return self.tapes[tape_index].head_position
    
    def print_status(self, show_head_marker: bool = True):
        """
        打印当前状态、所有磁带内容和磁头位置
        
        Args:
            show_head_marker: 是否显示磁头标记（用'*'表示）
        """
        print(f"当前状态：{self.current_state}")
        print(f"步数：{self.step_count}")
        
        for i, tape in enumerate(self.tapes):
            content, head_pos = tape.get_display_content(padding=5)
            
            if show_head_marker:
                # 在磁头位置插入'*'标记
                display = content[:head_pos] + "*" + content[head_pos:]
                print(f"Tape {i + 1}: {display}")
            else:
                print(f"Tape {i + 1}: {content}")
            
            if i < self.num_tapes - 1:
                print(TAPE_SEPARATOR)
    
    def reset(self):
        """重置图灵机到初始状态"""
        self.tapes = [Tape() for _ in range(self.num_tapes)]
        self.current_state = self.initial_state
        self.halted = False
        self.step_count = 0


def run_multitape(
    num_tapes: int,
    initial_state: str,
    transitions: List[dict],
    tape_contents: List[str],
    accept_states: Optional[set] = None,
    mode: str = "interactive",
    interval: float = 0.5,
    max_steps: int = 10000
) -> bool:
    """
    运行多带图灵机的便捷函数
    
    Args:
        num_tapes: 磁带数量
        initial_state: 初始状态
        transitions: 转移规则列表，每个元素为字典格式：
            {
                "state": "q1",
                "read": ("0", " "),  # 每条磁带读取的符号
                "write": ("1", " "),  # 每条磁带写入的符号
                "move": ("right", "stay"),  # 每条磁带的移动方向
                "next_state": "q2"
            }
        tape_contents: 每条磁带的初始内容
        accept_states: 接受状态集合
        mode: 运行模式 - "interactive"（交互式）或 "auto"（自动）
        interval: 自动模式下的时间间隔（秒）
        max_steps: 最大步数限制，防止无限循环
    
    Returns:
        是否被接受
    """
    # 创建多带图灵机
    tm = MultiTapeTM(num_tapes, initial_state, accept_states)
    
    # 设置磁带内容
    for i, content in enumerate(tape_contents):
        tm.set_tape(i, content)
    
    # 添加转移规则
    for t in transitions:
        tm.add_transition(
            current_state=t["state"],
            read_symbols=tuple(t["read"]),
            write_symbols=tuple(t["write"]),
            moves=tuple(t["move"]),
            next_state=t["next_state"]
        )
    
    # 打印初始状态
    print("=" * 50)
    print("初始状态")
    print("=" * 50)
    tm.print_status()
    print()
    
    # 运行
    while not tm.is_halted() and tm.step_count < max_steps:
        if mode == "interactive":
            input("按 Enter 键继续下一步...")
        else:
            time.sleep(interval)
        
        success = tm.step()
        
        print("=" * 50)
        print(f"第 {tm.step_count} 步")
        print("=" * 50)
        tm.print_status()
        print()
        
        if not success:
            break
    
    # 最终结果
    print("=" * 50)
    if tm.is_accepted():
        print("结果：接受 (ACCEPTED)")
    else:
        print("结果：拒绝 (REJECTED)")
    print(f"总步数：{tm.step_count}")
    print("=" * 50)
    
    return tm.is_accepted()


# 用于CLI的接口
def run_multitape_from_config(config: dict, mode: str = "interactive", interval: float = 0.5) -> bool:
    """
    从配置字典运行多带图灵机
    
    Args:
        config: 配置字典，包含：
            - num_tapes: 磁带数量
            - initial_state: 初始状态
            - accept_states: 接受状态列表
            - transitions: 转移规则列表
            - tape_contents: 磁带初始内容列表
        mode: 运行模式
        interval: 时间间隔
    
    Returns:
        是否被接受
    """
    return run_multitape(
        num_tapes=config.get("num_tapes", 1),
        initial_state=config.get("initial_state", "q1"),
        transitions=config.get("transitions", []),
        tape_contents=config.get("tape_contents", [""]),
        accept_states=set(config.get("accept_states", [])),
        mode=mode,
        interval=interval
    )