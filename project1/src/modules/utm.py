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

DIRECTION_IDS = {"left": 1, "right": 2, "stay": 3}
DIRECTION_NAMES = {1: "left", 2: "right", 3: "stay"}


TAPE_SEPARATOR = "-" * 40


class UniversalTuringMachine:
    
    def __init__(
        self,
        machine_encoding: str,
        input_string: str,
        state_ids: Dict[str, int],
        symbol_ids: Dict[str, int],
        start_state: str = "q1",
        accept_states: Optional[set] = None
    ):
        self.machine_encoding = machine_encoding
        self.input_string = input_string
        self.state_ids = state_ids
        self.symbol_ids = symbol_ids
        self.start_state = start_state
        self.accept_states = accept_states or set()
        
        self.transitions = self._parse_transitions(machine_encoding)
        
        self.tapes: List[Tape] = [Tape() for _ in range(3)]
        
        self.state = UTMState(stage="initial")
        self.simulated_state_id = state_ids.get(start_state, 1)  
        
        self.symbol_representation_length = self._calculate_representation_length()
    
    def _calculate_representation_length(self) -> int:
        max_state_id = max(self.state_ids.values()) if self.state_ids else 1
        max_symbol_id = max(self.symbol_ids.values()) if self.symbol_ids else 3
        return max(max_state_id, max_symbol_id)
    
    def _parse_transitions(self, encoding: str) -> List[UTMTransition]:
        transitions = []
        
        transition_parts = encoding.split("11")
        
        for part in transition_parts:
            if not part:
                continue
            
            components = part.split("1")
            
            if len(components) != 5:
                continue  
            
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
                continue  
        
        return transitions
    
    def _unary_encode(self, number: int) -> str:
        return "0" * number
    
    def initialize_tapes(self):
        # Tape1: M111w
        tape1_content = self.machine_encoding + "111" + self.input_string
        self.tapes[0].content = list(tape1_content)
        self.tapes[0].head_position = 0
        
        # Tape2: 初始化为输入 w
        tape2_content = self._encode_input_for_tape2(self.input_string)
        self.tapes[1].content = list(tape2_content) if tape2_content else [BLANK_SYMBOL]
        self.tapes[1].head_position = 0
        
        # Tape3: 存储起始状态
        start_state_encoding = self._unary_encode(self.simulated_state_id)
        self.tapes[2].content = list(start_state_encoding) if start_state_encoding else [BLANK_SYMBOL]
        self.tapes[2].head_position = 0
    
    def _encode_input_for_tape2(self, input_string: str) -> str:
        encoded_parts = []
        for char in input_string:
            symbol_id = self.symbol_ids.get(char, 3) 
            encoded_parts.append(self._unary_encode(symbol_id))
        return "1".join(encoded_parts)
    
    def _decode_symbol_from_tape2(self) -> int:
        count = 0
        pos = self.tapes[1].head_position
        
        while pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "0":
            count += 1
            pos += 1
        
        return count if count > 0 else 3  # 默认为空符号ID
    
    def _find_matching_transition(self, state_id: int, symbol_id: int) -> Optional[UTMTransition]:
        for transition in self.transitions:
            if transition.current_state_id == state_id and transition.read_symbol_id == symbol_id:
                return transition
        return None
    
    def _execute_transition(self, transition: UTMTransition):
        self._clear_symbol_on_tape2()
        
        new_symbol_encoding = self._unary_encode(transition.write_symbol_id)
        for char in new_symbol_encoding:
            self.tapes[1].write(char)
            self.tapes[1].move("right")
        
        direction = DIRECTION_NAMES.get(transition.move_id, "stay")
        if direction == "left":
            # 向左移动：需要回退到前一个符号的开始位置
            self._move_tape2_left()
        elif direction == "right":
            # 向右移动：需要定位到下一个符号
            self._skip_separator_on_tape2()
        
        self.tapes[2].content = list(self._unary_encode(transition.next_state_id))
        self.tapes[2].head_position = 0
        self.simulated_state_id = transition.next_state_id
    
    def _clear_symbol_on_tape2(self):
        while self.tapes[1].head_position < len(self.tapes[1].content):
            if self.tapes[1].content[self.tapes[1].head_position] == "0":
                self.tapes[1].content[self.tapes[1].head_position] = BLANK_SYMBOL
                self.tapes[1].head_position += 1
            else:
                break
        self.tapes[1].head_position = 0
    
    def _move_tape2_left(self):
        pos = self.tapes[1].head_position
        
        while pos > 0 and self.tapes[1].content[pos - 1] == BLANK_SYMBOL:
            pos -= 1
        
        if pos > 0 and self.tapes[1].content[pos - 1] == "1":
            pos -= 1  
        
        while pos > 0 and self.tapes[1].content[pos - 1] == "0":
            pos -= 1
        
        self.tapes[1].head_position = pos
    
    def _move_tape2_right(self):
        pos = self.tapes[1].head_position
        
        while pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "0":
            pos += 1
        
        if pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "1":
            pos += 1
        
        self.tapes[1].head_position = pos
    
    def _skip_separator_on_tape2(self):
        pos = self.tapes[1].head_position
        if pos < len(self.tapes[1].content) and self.tapes[1].content[pos] == "1":
            self.tapes[1].head_position += 1
    
    def print_stage(self, stage_name: str):
        description = STAGE_DESCRIPTIONS.get(stage_name, "")
        print(f"当前阶段说明：{description}")
    
    def print_tapes(self, show_head_marker: bool = True):
        tape_names = ["Tape1 (M111w)", "Tape2 (模拟磁带)", "Tape3 (状态)"]
        
        for i, tape in enumerate(self.tapes):
            content, head_pos = tape.get_display_content(padding=5)
            
            if show_head_marker:
                display = content[:head_pos] + "*" + content[head_pos:]
                print(f"{tape_names[i]}: {display}")
            else:
                print(f"{tape_names[i]}: {content}")
            
            if i < 2:
                print(TAPE_SEPARATOR)
    
    def print_status(self):
        print("=" * 60)
        print(f"UTM 步数：{self.state.step_count}")
        print(f"被模拟图灵机状态ID：{self.simulated_state_id}")
        self.print_tapes()
        self.print_stage(self.state.stage)
        print("=" * 60)
    
    def step(self) -> bool:
        if self.state.halted:
            return False
        
        current_symbol_id = self._decode_symbol_from_tape2()
        
        self.state.stage = "search_move"
        transition = self._find_matching_transition(self.simulated_state_id, current_symbol_id)
        
        if transition is None:
            self.state.stage = "no_match"
            self.state.halted = True
            return False
        
        self.state.stage = "execute_move"
        self._execute_transition(transition)
        self.state.step_count += 1
    
        state_name = self._get_state_name_by_id(self.simulated_state_id)
        if state_name in self.accept_states:
            self.state.stage = "accept"
            self.state.accepted = True
            self.state.halted = True
        
        return True
    
    def _get_state_name_by_id(self, state_id: int) -> Optional[str]:
        for name, id_ in self.state_ids.items():
            if id_ == state_id:
                return name
        return None
    
    def run(self, mode: str = "interactive", interval: float = 0.5, max_steps: int = 10000):
        self.state.stage = "step2"
        print("\n" + "=" * 60)
        print("UTM 初始化")
        print("=" * 60)
        self.print_stage("step2")
        print(f"符号表示长度：{self.symbol_representation_length} 个UTM符号")
        print()
        
        self.state.stage = "step3"
        self.print_stage("step3")
        self.initialize_tapes()
        print()
        
        print("=" * 60)
        print("初始状态")
        print("=" * 60)
        self.print_status()
        print()
        
        while not self.state.halted and self.state.step_count < max_steps:
            if mode == "interactive": # 默认为交互式
                input("按 Enter 键继续下一步...")
            else:
                time.sleep(interval)
            
            success = self.step()
            self.print_status()
            print()
            
            if not success:
                break
        
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

    result = encode_machine_file(json_path)
    
    if details:
        print("编码结果：")
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        print()
    
    machine_definition = load_json_object(json_path)
    input_list = machine_definition.get("input", [])
    input_string = BLANK_SYMBOL.join(input_list)  
    
   
    state_names = list(result.state_ids.keys())
    start_state = "q1" if "q1" in state_names else state_names[0] if state_names else "q1"
    
    accept_states = {"halt", "H", "h", "accept", "ACCEPT"}
    for state in state_names:
        if state.lower() in {"halt", "h", "accept"}:
            accept_states.add(state)
    
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