"""
通用图灵机模块 (Universal Turing Machine)

基于多带图灵机模块实现通用图灵机模拟器。
UTM使用三条磁带：
- Tape1: 存储 M111w（被模拟图灵机的编码和输入）
- Tape2: 模拟被模拟图灵机的磁带
- Tape3: 存储当前状态

实现参考 tm2.ppt 中的定义。
"""

import json
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from core.models import Tape, UTMTransition, UTMState
from core.errors import AppError, ValidationError
from core.json_utils import load_json_object
from modules.encoding import encode_machine_file, encode_machine_definition
from modules.multitape import MultiTapeTM, BLANK_SYMBOL


# 阶段说明文本
STAGE_DESCRIPTIONS = {
    "step1": "Step 1: 检查输入 M 是否为合法的图灵机编码。（已跳过，假定输入合法）",
    "step2": "Step 2: The UTM examines M to see how many of its own tape squares it needs to represent one symbol of M.",
    "step3": "Step 3: Initialize Tape 2 to represent the tape of M with input w, and initialize Tape 3 to hold the start state.",
    "search_move": "Look for a move on Tape 1 that matches the state on Tape 3 and the tape symbol under the head on Tape 2.",
    "execute_move": "If found, change the symbol and move the head marker on Tape 2 and change the State on Tape 3.",
    "accept": "M accepts, the UTM also accepts.",
    "reject": "M rejects, the UTM also rejects.",
    "no_match": "No matching transition found. M halts.",
}

# 方向ID映射
DIRECTION_IDS = {"left": 1, "right": 2, "stay": 3}
DIRECTION_NAMES = {1: "left", 2: "right", 3: "stay"}

# 分隔符
TAPE_SEPARATOR = "-" * 40


class UniversalTuringMachine:
    """通用图灵机类"""
    
    def __init__(
        self,
        machine_encoding: str,
        input_string: str,
        state_ids: Dict[str, int],
        symbol_ids: Dict[str, int],
        start_state: str = "q1",
        accept_states: Optional[set] = None
    ):
        """
        初始化通用图灵机
        
        Args:
            machine_encoding: 被模拟图灵机的二进制编码(M)
            input_string: 被模拟图灵机的输入字符串(w)
            state_ids: 状态名到ID的映射
            symbol_ids: 符号到ID的映射
            start_state: 被模拟图灵机的起始状态
            accept_states: 被模拟图灵机的接受状态集合
        """
        self.machine_encoding = machine_encoding
        self.input_string = input_string
        self.state_ids = state_ids
        self.symbol_ids = symbol_ids
        self.start_state = start_state
        self.accept_states = accept_states or set()
        
        # 解析转移规则
        self.transitions = self._parse_transitions(machine_encoding)
        
        # 创建三条磁带
        self.tapes: List[Tape] = [Tape() for _ in range(3)]
        
        # 运行状态
        self.state = UTMState(stage="initial")
        self.simulated_state_id = state_ids.get(start_state, 1)  # 被模拟图灵机的当前状态ID
        
        # 计算符号表示需要的位数
        # 每个符号用 k 个 UTM 符号表示，其中 k = max(state_id位数, symbol_id位数)
        self.symbol_representation_length = self._calculate_representation_length()
    
    def _calculate_representation_length(self) -> int:
        """
        计算表示一个被模拟图灵机符号需要的UTM符号数量
        
        根据编码规则，状态ID和符号ID都用一进制表示，
        所以表示一个符号需要的位数取决于最大的ID值
        """
        max_state_id = max(self.state_ids.values()) if self.state_ids else 1
        max_symbol_id = max(self.symbol_ids.values()) if self.symbol_ids else 3
        return max(max_state_id, max_symbol_id)
    
    def _parse_transitions(self, encoding: str) -> List[UTMTransition]:
        """
        解析图灵机编码，提取转移规则
        
        编码格式：每个转移用 11 分隔
        每个转移格式：状态ID(一进制) 1 符号ID(一进制) 1 下一状态ID(一进制) 1 写入符号ID(一进制) 1 方向ID(一进制)
        一进制：数字n用n个0表示
        
        Args:
            encoding: 二进制编码字符串
        
        Returns:
            转移规则列表
        """
        transitions = []
        
        # 用 11 分隔各个转移
        transition_parts = encoding.split("11")
        
        for part in transition_parts:
            if not part:
                continue
            
            # 每个转移内部用 1 分隔各部分
            components = part.split("1")
            
            if len(components) != 5:
                continue  # 跳过无效格式
            
            # 解析一进制编码（0的数量表示数值）
            try:
                current_state_id = len(components[0])
                read_symbol_id = len(components[1])
                next_state_id = len(components[2])
                write_symbol_id = len(components[3])
                move_id = len(components[4])
                
                transition = UTMTransition(
                    current_state_id=current_state_id,
                    read_symbol_id=read_symbol_id,
                    next_state_id=next_state_id,
                    write_symbol_id=write_symbol_id,
                    move_id=move_id
                )
                transitions.append(transition)
            except Exception:
                continue  # 跳过解析失败的转移
        
        return transitions
    
    def _unary_encode(self, number: int) -> str:
        """将数字编码为一进制（n个0）"""
        return "0" * number
    
    def initialize_tapes(self):
        """
        初始化三条磁带
        
        Tape1: 存储 M111w
        Tape2: 初始化为输入 w 的内容
        Tape3: 存储起始状态的一进制编码
        """
        # Tape1: M111w
        tape1_content = self.machine_encoding + "111" + self.input_string
        self.tapes[0].content = list(tape1_content)
        self.tapes[0].head_position = 0
        
        # Tape2: 初始化为输入 w
        # 将输入字符串转换为符号ID的一进制表示
        tape2_content = self._encode_input_for_tape2(self.input_string)
        self.tapes[1].content = list(tape2_content) if tape2_content else [BLANK_SYMBOL]
        self.tapes[1].head_position = 0
        
        # Tape3: 存储起始状态
        start_state_encoding = self._unary_encode(self.simulated_state_id)
        self.tapes[2].content = list(start_state_encoding) if start_state_encoding else [BLANK_SYMBOL]
        self.tapes[2].head_position = 0
    
    def _encode_input_for_tape2(self, input_string: str) -> str:
        """
        将输入字符串编码为Tape2的格式
        
        每个输入符号用其符号ID的一进制表示，符号之间用1分隔
        """
        encoded_parts = []
        for char in input_string:
            symbol_id = self.symbol_ids.get(char, 3)  # 默认为空符号ID=3
            encoded_parts.append(self._unary_encode(symbol_id))
        return "1".join(encoded_parts)
    
    def _decode_symbol_from_tape2(self) -> int:
        """
        从Tape2当前磁头位置解码符号ID
        
        读取连续的0，遇到1或空符号时停止
        """
        count = 0
        pos = self.tapes[1].head_position
        
        # 向右扫描，读取连续的0
        while pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "0":
            count += 1
            pos += 1
        
        return count if count > 0 else 3  # 默认为空符号ID
    
    def _find_matching_transition(self, state_id: int, symbol_id: int) -> Optional[UTMTransition]:
        """
        在转移规则中查找匹配的转移
        
        Args:
            state_id: 当前状态ID
            symbol_id: 当前读取符号ID
        
        Returns:
            匹配的转移规则，如果没有则返回None
        """
        for transition in self.transitions:
            if transition.current_state_id == state_id and transition.read_symbol_id == symbol_id:
                return transition
        return None
    
    def _execute_transition(self, transition: UTMTransition):
        """
        执行转移规则
        
        1. 在Tape2上写入新符号
        2. 移动Tape2的磁头
        3. 更新Tape3上的状态
        """
        # 在Tape2上写入新符号（用一进制表示）
        # 首先清除当前位置的符号表示
        self._clear_symbol_on_tape2()
        
        # 写入新符号
        new_symbol_encoding = self._unary_encode(transition.write_symbol_id)
        for char in new_symbol_encoding:
            self.tapes[1].write(char)
            self.tapes[1].move("right")
        
        # 根据方向移动磁头
        direction = DIRECTION_NAMES.get(transition.move_id, "stay")
        if direction == "left":
            # 向左移动需要回退到前一个符号的开始位置
            self._move_tape2_left()
        elif direction == "right":
            # 已经在写入时向右移动了，需要定位到下一个符号
            self._skip_separator_on_tape2()
        
        # 更新Tape3上的状态
        self.tapes[2].content = list(self._unary_encode(transition.next_state_id))
        self.tapes[2].head_position = 0
        self.simulated_state_id = transition.next_state_id
    
    def _clear_symbol_on_tape2(self):
        """清除Tape2上当前符号的表示"""
        # 从当前位置向右清除连续的0，直到遇到1或边界
        while self.tapes[1].head_position < len(self.tapes[1].content):
            if self.tapes[1].content[self.tapes[1].head_position] == "0":
                self.tapes[1].content[self.tapes[1].head_position] = BLANK_SYMBOL
                self.tapes[1].head_position += 1
            else:
                break
        # 回到起始位置
        self.tapes[1].head_position = 0
    
    def _move_tape2_left(self):
        """将Tape2的磁头向左移动一个符号单位"""
        # 向左移动，跳过分隔符1，找到前一个符号的开始
        pos = self.tapes[1].head_position
        
        # 先向左找到分隔符或边界
        while pos > 0 and self.tapes[1].content[pos - 1] == BLANK_SYMBOL:
            pos -= 1
        
        if pos > 0 and self.tapes[1].content[pos - 1] == "1":
            pos -= 1  # 跨过分隔符
        
        # 继续向左找到符号的开始（连续0的起点）
        while pos > 0 and self.tapes[1].content[pos - 1] == "0":
            pos -= 1
        
        self.tapes[1].head_position = pos
    
    def _move_tape2_right(self):
        """将Tape2的磁头向右移动一个符号单位"""
        # 向右移动，跳过当前符号和分隔符
        pos = self.tapes[1].head_position
        
        # 跳过当前符号的0
        while pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "0":
            pos += 1
        
        # 跳过分隔符1
        if pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "1":
            pos += 1
        
        self.tapes[1].head_position = pos
    
    def _skip_separator_on_tape2(self):
        """跳过Tape2上的分隔符"""
        pos = self.tapes[1].head_position
        if pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "1":
            self.tapes[1].head_position += 1
    
    def print_stage(self, stage_name: str):
        """打印当前阶段说明"""
        description = STAGE_DESCRIPTIONS.get(stage_name, "")
        print(f"当前阶段说明：{description}")
    
    def print_tapes(self, show_head_marker: bool = True):
        """
        打印三条磁带的状态
        
        Args:
            show_head_marker: 是否显示磁头标记
        """
        tape_names = ["Tape1 (M111w)", "Tape2 (模拟磁带)", "Tape3 (状态)"]
        
        for i, tape in enumerate(self.tapes):
            content, head_pos = tape.get_display_content(padding=5)
            
            if show_head_marker:
                # 在磁头位置插入'*'标记
                display = content[:head_pos] + "*" + content[head_pos:]
                print(f"{tape_names[i]}: {display}")
            else:
                print(f"{tape_names[i]}: {content}")
            
            if i < 2:
                print(TAPE_SEPARATOR)
    
    def print_status(self):
        """打印完整的运行状态"""
        print("=" * 60)
        print(f"UTM 步数：{self.state.step_count}")
        print(f"被模拟图灵机状态ID：{self.simulated_state_id}")
        self.print_tapes()
        self.print_stage(self.state.stage)
        print("=" * 60)
    
    def step(self) -> bool:
        """
        执行一步UTM操作
        
        Returns:
            是否成功执行（False表示停机）
        """
        if self.state.halted:
            return False
        
        # 获取当前状态和符号
        current_symbol_id = self._decode_symbol_from_tape2()
        
        # 搜索匹配的转移
        self.state.stage = "search_move"
        transition = self._find_matching_transition(self.simulated_state_id, current_symbol_id)
        
        if transition is None:
            # 无匹配转移，停机
            self.state.stage = "no_match"
            self.state.halted = True
            return False
        
        # 执行转移
        self.state.stage = "execute_move"
        self._execute_transition(transition)
        self.state.step_count += 1
        
        # 检查是否进入接受状态
        # 将状态ID转换回状态名检查
        state_name = self._get_state_name_by_id(self.simulated_state_id)
        if state_name in self.accept_states:
            self.state.stage = "accept"
            self.state.accepted = True
            self.state.halted = True
        
        return True
    
    def _get_state_name_by_id(self, state_id: int) -> Optional[str]:
        """根据状态ID获取状态名"""
        for name, id_ in self.state_ids.items():
            if id_ == state_id:
                return name
        return None
    
    def run(self, mode: str = "interactive", interval: float = 0.5, max_steps: int = 10000):
        """
        运行UTM
        
        Args:
            mode: 运行模式 - "interactive" 或 "auto"
            interval: 自动模式下的时间间隔（秒）
            max_steps: 最大步数限制
        """
        # Step 2: 分析M
        self.state.stage = "step2"
        print("\n" + "=" * 60)
        print("UTM 初始化")
        print("=" * 60)
        self.print_stage("step2")
        print(f"符号表示长度：{self.symbol_representation_length} 个UTM符号")
        print()
        
        # Step 3: 初始化磁带
        self.state.stage = "step3"
        self.print_stage("step3")
        self.initialize_tapes()
        print()
        
        # 打印初始状态
        print("=" * 60)
        print("初始状态")
        print("=" * 60)
        self.print_status()
        print()
        
        # 主循环
        while not self.state.halted and self.state.step_count < max_steps:
            if mode == "interactive":
                input("按 Enter 键继续下一步...")
            else:
                time.sleep(interval)
            
            success = self.step()
            self.print_status()
            print()
            
            if not success:
                break
        
        # 最终结果
        print("=" * 60)
        print("运行结束")
        print("=" * 60)
        if self.state.accepted:
            self.print_stage("accept")
            print("结果：接受 (ACCEPTED)")
        else:
            self.print_stage("reject")
            print("结果：拒绝 (REJECTED)")
        print(f"总步数：{self.state.step_count}")
        print("=" * 60)
        
        return self.state.accepted
    
    def reset(self):
        """重置UTM"""
        self.tapes = [Tape() for _ in range(3)]
        self.state = UTMState(stage="initial")
        self.simulated_state_id = self.state_ids.get(self.start_state, 1)


def run_utm(
    json_path: Union[str, Path],
    mode: str = "interactive",
    interval: float = 0.5,
    max_steps: int = 10000,
    details: bool = False
) -> bool:
    """
    运行UTM的便捷函数
    
    Args:
        json_path: 图灵机JSON定义文件路径
        mode: 运行模式
        interval: 时间间隔
        max_steps: 最大步数
        details: 是否输出详细信息
    
    Returns:
        是否被接受
    """
    # 编码图灵机
    result = encode_machine_file(json_path)
    
    if details:
        print("编码结果：")
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        print()
    
    # 获取输入字符串
    machine_definition = load_json_object(json_path)
    input_list = machine_definition.get("input", [])
    input_string = BLANK_SYMBOL.join(input_list)  # 用空符号分隔各输入
    
    # 确定起始状态和接受状态
    # 起始状态通常是第一个状态或名为 q1/halt 的状态
    state_names = list(result.state_ids.keys())
    start_state = "q1" if "q1" in state_names else state_names[0] if state_names else "q1"
    
    # 接受状态通常是 halt, accept, h 等
    accept_states = {"halt", "H", "h", "accept", "ACCEPT"}
    for state in state_names:
        if state.lower() in {"halt", "h", "accept"}:
            accept_states.add(state)
    
    # 创建并运行UTM
    utm = UniversalTuringMachine(
        machine_encoding=result.encoding,
        input_string=input_string,
        state_ids=result.state_ids,
        symbol_ids=result.symbol_ids,
        start_state=start_state,
        accept_states=accept_states
    )
    
    return utm.run(mode=mode, interval=interval, max_steps=max_steps)


def run_utm_from_encoding(
    encoding_result,
    input_string: str,
    mode: str = "interactive",
    interval: float = 0.5,
    max_steps: int = 10000
) -> bool:
    """
    从编码结果运行UTM
    
    Args:
        encoding_result: EncodingResult 对象
        input_string: 输入字符串
        mode: 运行模式
        interval: 时间间隔
        max_steps: 最大步数
    
    Returns:
        是否被接受
    """
    state_names = list(encoding_result.state_ids.keys())
    start_state = "q1" if "q1" in state_names else state_names[0] if state_names else "q1"
    
    accept_states = {"halt", "H", "h", "accept", "ACCEPT"}
    for state in state_names:
        if state.lower() in {"halt", "h", "accept"}:
            accept_states.add(state)
    
    utm = UniversalTuringMachine(
        machine_encoding=encoding_result.encoding,
        input_string=input_string,
        state_ids=encoding_result.state_ids,
        symbol_ids=encoding_result.symbol_ids,
        start_state=start_state,
        accept_states=accept_states
    )
    
    return utm.run(mode=mode, interval=interval, max_steps=max_steps)