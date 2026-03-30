import re
from pathlib import Path
from typing import Any, Dict, List, Union

from core.errors import ValidationError
from core.json_utils import load_json_object
from core.models import EncodedTransition, EncodingResult, Transition

BLANK_SYMBOL = " "
BLANK_ALIASES = {"", " ", "blank"}
STATE_NAME_PATTERN = re.compile(r"^q([1-9]\d*)$")
DIRECTION_IDS = {"left": 1, "right": 2, "stay": 3}


def encode_machine_file(path: Union[str, Path]) -> EncodingResult:
    machine_definition = load_json_object(path)
    return encode_machine_definition(machine_definition)


def encode_machine_definition(machine_definition: Dict[str, Any]) -> EncodingResult:
    transitions = extract_transitions(machine_definition)
    state_ids = build_state_ids(transitions)
    symbol_ids = build_symbol_ids(transitions)

    ordered_transitions = sorted(
        transitions,
        key=lambda transition: (
            state_ids[transition.current_state],
            symbol_ids[transition.read_symbol],
            state_ids[transition.next_state],
            symbol_ids[transition.write_symbol],
            DIRECTION_IDS[transition.move],
        ),
    )

    encoded_transitions = [
        EncodedTransition(
            current_state=transition.current_state,
            read_symbol=transition.read_symbol,
            write_symbol=transition.write_symbol,
            move=transition.move,
            next_state=transition.next_state,
            encoding=encode_transition(transition, state_ids, symbol_ids),
        )
        for transition in ordered_transitions
    ]

    return EncodingResult(
        encoding="11".join(item.encoding for item in encoded_transitions),
        state_ids=dict(sorted(state_ids.items(), key=lambda item: item[1])),
        symbol_ids=dict(sorted(symbol_ids.items(), key=lambda item: item[1])),
        transitions=encoded_transitions,
    )


def extract_transitions(machine_definition: Dict[str, Any]) -> List[Transition]:
    transitions: List[Transition] = []

    for state_name, state_body in machine_definition.items():
        if state_name == "input":
            continue

        if not isinstance(state_name, str):
            raise ValidationError("状态名必须是字符串。")
        if not isinstance(state_body, dict):
            raise ValidationError(f"状态 {state_name!r} 的定义必须是对象。")

        for read_symbol, action in state_body.items():
            if not isinstance(read_symbol, str):
                raise ValidationError(f"状态 {state_name!r} 的读取符号必须是字符串。")
            if not isinstance(action, dict):
                raise ValidationError(
                    f"状态 {state_name!r} 在符号 {read_symbol!r} 下的动作必须是对象。"
                )

            missing_keys = {"write", "move", "nextState"} - set(action)
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise ValidationError(
                    f"状态 {state_name!r} 在符号 {read_symbol!r} 下缺少字段: {missing}"
                )

            write_symbol = action["write"]
            move = action["move"]
            next_state = action["nextState"]

            if not isinstance(write_symbol, str):
                raise ValidationError("字段 write 必须是字符串。")
            if not isinstance(move, str):
                raise ValidationError("字段 move 必须是字符串。")
            if not isinstance(next_state, str):
                raise ValidationError("字段 nextState 必须是字符串。")

            transitions.append(
                Transition(
                    current_state=state_name,
                    read_symbol=normalize_symbol(read_symbol),
                    write_symbol=normalize_symbol(write_symbol),
                    move=normalize_move(move),
                    next_state=next_state,
                )
            )

    if not transitions:
        raise ValidationError("JSON 中未找到任何状态转移定义。")

    return transitions


def normalize_symbol(symbol: str) -> str:
    if symbol in BLANK_ALIASES:
        return BLANK_SYMBOL
    return symbol


def normalize_move(move: str) -> str:
    lowered = move.strip().lower()
    if lowered in {"left", "l"}:
        return "left"
    if lowered in {"right", "r"}:
        return "right"
    if lowered in {"stay", "s"}:
        return "stay"
    raise ValidationError(f"不支持的移动方向: {move!r}")


def unary_encode(number: int) -> str:
    if number <= 0:
        raise ValidationError(f"用于编码的数字必须为正整数，收到 {number}。")
    return "0" * number


def build_state_ids(transitions: List[Transition]) -> Dict[str, int]:
    state_names = {
        transition.current_state for transition in transitions
    } | {transition.next_state for transition in transitions}

    state_ids: Dict[str, int] = {}
    used_ids: Dict[int, str] = {}

    for state_name in sorted(state_names):
        match = STATE_NAME_PATTERN.fullmatch(state_name)
        if not match:
            continue

        state_id = int(match.group(1))
        if state_id in used_ids and used_ids[state_id] != state_name:
            raise ValidationError(
                f"状态 {used_ids[state_id]!r} 和 {state_name!r} 映射到了同一个编号 {state_id}。"
            )
        state_ids[state_name] = state_id
        used_ids[state_id] = state_name

    next_available = 1
    for state_name in sorted(state_names):
        if state_name in state_ids:
            continue
        while next_available in used_ids:
            next_available += 1
        state_ids[state_name] = next_available
        used_ids[next_available] = state_name
        next_available += 1

    return state_ids


def build_symbol_ids(transitions: List[Transition]) -> Dict[str, int]:
    symbols = {
        transition.read_symbol for transition in transitions
    } | {transition.write_symbol for transition in transitions}

    symbol_ids: Dict[str, int] = {"0": 1, "1": 2, BLANK_SYMBOL: 3}
    next_available = 4

    for symbol in sorted(symbols):
        if symbol in symbol_ids:
            continue
        symbol_ids[symbol] = next_available
        next_available += 1

    return symbol_ids


def encode_transition(
    transition: Transition,
    state_ids: Dict[str, int],
    symbol_ids: Dict[str, int],
) -> str:
    parts = [
        unary_encode(state_ids[transition.current_state]),
        unary_encode(symbol_ids[transition.read_symbol]),
        unary_encode(state_ids[transition.next_state]),
        unary_encode(symbol_ids[transition.write_symbol]),
        unary_encode(DIRECTION_IDS[transition.move]),
    ]
    return "1".join(parts)