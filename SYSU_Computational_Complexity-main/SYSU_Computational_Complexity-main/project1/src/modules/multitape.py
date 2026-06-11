import time
from typing import Dict, List, Optional, Tuple

from core.models import Tape, MultiTapeTransition
from core.errors import AppError


BLANK_SYMBOL = " "
TAPE_SEPARATOR = "-" * 40


class MultiTapeTM:
    def __init__(self, num_tapes: int, initial_state: str, accept_states: Optional[set] = None):
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
        if not 0 <= tape_index < self.num_tapes:
            raise IndexError(f"磁带索引 {tape_index} 超出范围 [0, {self.num_tapes - 1}]")
        
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
        return tuple(tape.read() for tape in self.tapes)
    
    def step(self) -> bool:
        if self.halted:
            return False
        
        current_symbols = self.get_current_symbols()
        key = (self.current_state, current_symbols)
        
        if key not in self.transitions:
            self.halted = True
            return False
        
        transition = self.transitions[key]
        
        for i, tape in enumerate(self.tapes):
            tape.write(transition.write_symbols[i])
            tape.move(transition.moves[i])
        
        self.current_state = transition.next_state
        self.step_count += 1
        
        if self.current_state in self.accept_states:
            self.halted = True
        
        return True
    
    def is_accepted(self) -> bool:
        return self.current_state in self.accept_states
    
    def is_halted(self) -> bool:
        return self.halted
    
    def get_state(self) -> str:
        return self.current_state
    
    def get_tape_content(self, tape_index: int) -> str:
        if not 0 <= tape_index < self.num_tapes:
            raise IndexError(f"磁带索引 {tape_index} 超出范围")
        return "".join(self.tapes[tape_index].content)
    
    def get_head_position(self, tape_index: int) -> int:
        if not 0 <= tape_index < self.num_tapes:
            raise IndexError(f"磁带索引 {tape_index} 超出范围")
        return self.tapes[tape_index].head_position
    
    def print_status(self, show_head_marker: bool = True):
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
    mode: str = "interactive",  # "auto"(自动模式)
    interval: float = 0.5,
    max_steps: int = 10000
) -> bool:
    tm = MultiTapeTM(num_tapes, initial_state, accept_states)
    
    for i, content in enumerate(tape_contents):
        tm.set_tape(i, content)
    
    for t in transitions:
        tm.add_transition(
            current_state=t["state"],
            read_symbols=tuple(t["read"]),
            write_symbols=tuple(t["write"]),
            moves=tuple(t["move"]),
            next_state=t["next_state"]
        )
    

    print("=" * 50)
    print("初始状态")
    print("=" * 50)
    tm.print_status()
    print()
    

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
    return run_multitape(
        num_tapes=config.get("num_tapes", 1),
        initial_state=config.get("initial_state", "q1"),
        transitions=config.get("transitions", []),
        tape_contents=config.get("tape_contents", [""]),
        accept_states=set(config.get("accept_states", [])),
        mode=mode,
        interval=interval
    )