import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

from core.errors import AppError, NotImplementedFeatureError
from core.models import SampleInfo
from core.samples import discover_samples, resolve_sample
from modules.encoding import encode_machine_file
from modules.multitape import run_multitape, run_multitape_from_config
from modules.utm import run_utm, run_utm_from_encoding

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="统一图灵机程序入口。已实现：图灵机编码、多带图灵机、通用图灵机模块。"
    )
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="列出 test 目录下的共享 JSON 样例")
    list_parser.set_defaults(handler=handle_list)

    encode_parser = subparsers.add_parser("encode", help="对指定样例执行图灵机编码")
    encode_parser.add_argument(
        "--sample",
        help="样例文件名、相对路径或完整路径。未提供时进入交互选择。",
    )
    encode_parser.add_argument(
        "--details",
        action="store_true",
        help="输出状态映射、符号映射和逐转移编码明细。",
    )
    encode_parser.set_defaults(handler=handle_encode)

    multitape_parser = subparsers.add_parser("multitape", help="运行多带图灵机模拟器")
    multitape_parser.add_argument(
        "--config",
        help="多带图灵机配置文件路径（JSON格式）。",
    )
    multitape_parser.add_argument(
        "--mode",
        choices=["interactive", "auto"],
        default="interactive",
        help="运行模式：interactive（交互式）或 auto（自动）。",
    )
    multitape_parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="自动模式下的时间间隔（秒）。",
    )
    multitape_parser.set_defaults(handler=handle_multitape)

    utm_parser = subparsers.add_parser("utm", help="运行通用图灵机模拟器")
    utm_parser.add_argument(
        "--sample",
        help="样例文件名、相对路径或完整路径。未提供时进入交互选择。",
    )
    utm_parser.add_argument(
        "--mode",
        choices=["interactive", "auto"],
        default="interactive",
        help="运行模式：interactive（交互式）或 auto（自动）。",
    )
    utm_parser.add_argument(
        "--interval",
        type=float,
        default=0.5,
        help="自动模式下的时间间隔（秒）。",
    )
    utm_parser.add_argument(
        "--details",
        action="store_true",
        help="输出编码详细信息。",
    )
    utm_parser.add_argument(
        "--max-steps",
        type=int,
        default=10000,
        help="最大运行步数限制。",
    )
    utm_parser.set_defaults(handler=handle_utm)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        return run_interactive_menu()

    try:
        return args.handler(args)
    except AppError as error:
        print(f"错误: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n操作已取消。", file=sys.stderr)
        return 130


def handle_list(_args: argparse.Namespace) -> int:
    samples = discover_samples(PROJECT_ROOT)
    if not samples:
        print("test 目录下未发现任何 JSON 测试样例。")
        return 0

    print("可用测试样例:")
    for index, sample in enumerate(samples, start=1):
        print(f"{index}. {sample.name} ({sample.relative_path.as_posix()})")
    return 0


def handle_encode(args: argparse.Namespace) -> int:
    sample = resolve_sample(PROJECT_ROOT, args.sample) if args.sample else prompt_for_sample()
    result = encode_machine_file(sample.path)

    if args.details:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        return 0

    print(result.encoding)
    return 0


def handle_multitape(args: argparse.Namespace) -> int:
    """处理多带图灵机命令"""
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"错误: 配置文件 {args.config} 不存在。", file=sys.stderr)
            return 1
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"错误: 配置文件 JSON 格式无效: {e}", file=sys.stderr)
            return 1
    else:
        # 使用默认的多带图灵机演示配置
        print("未提供配置文件，使用默认演示配置。")
        config = get_default_multitape_demo_config()
    
    print("\n" + "=" * 60)
    print("多带图灵机模拟器")
    print("=" * 60)
    print(f"运行模式: {args.mode}")
    if args.mode == "auto":
        print(f"时间间隔: {args.interval} 秒")
    print()
    
    result = run_multitape_from_config(config, mode=args.mode, interval=args.interval)
    return 0 if result else 1


def handle_utm(args: argparse.Namespace) -> int:
    """处理通用图灵机命令"""
    sample = resolve_sample(PROJECT_ROOT, args.sample) if args.sample else prompt_for_sample()
    
    print("\n" + "=" * 60)
    print("通用图灵机模拟器 (UTM)")
    print("=" * 60)
    print(f"测试样例: {sample.name}")
    print(f"运行模式: {args.mode}")
    if args.mode == "auto":
        print(f"时间间隔: {args.interval} 秒")
    print(f"最大步数: {args.max_steps}")
    print()
    
    result = run_utm(
        json_path=sample.path,
        mode=args.mode,
        interval=args.interval,
        max_steps=args.max_steps,
        details=args.details
    )
    return 0 if result else 1


def get_default_multitape_demo_config() -> dict:
    """获取默认的多带图灵机演示配置"""
    return {
        "num_tapes": 2,
        "initial_state": "q1",
        "accept_states": ["halt"],
        "transitions": [
            {
                "state": "q1",
                "read": ("0", " "),
                "write": ("0", " "),
                "move": ("right", "stay"),
                "next_state": "q1"
            },
            {
                "state": "q1",
                "read": ("1", " "),
                "write": ("1", " "),
                "move": ("right", "stay"),
                "next_state": "q1"
            },
            {
                "state": "q1",
                "read": (" ", " "),
                "write": (" ", " "),
                "move": ("left", "stay"),
                "next_state": "q2"
            },
            {
                "state": "q2",
                "read": ("0", " "),
                "write": ("1", " "),
                "move": ("left", "stay"),
                "next_state": "halt"
            },
            {
                "state": "q2",
                "read": ("1", " "),
                "write": ("0", " "),
                "move": ("left", "stay"),
                "next_state": "q2"
            },
        ],
        "tape_contents": ["0101", ""]
    }


def prompt_for_sample() -> SampleInfo:
    samples = discover_samples(PROJECT_ROOT)
    if not samples:
        raise AppError("test 目录为空，无法选择测试样例。")

    print("请选择测试样例:")
    for index, sample in enumerate(samples, start=1):
        print(f"{index}. {sample.name} ({sample.relative_path.as_posix()})")

    while True:
        selected = input("请输入编号: ").strip()
        if not selected.isdigit():
            print("请输入有效的数字编号。")
            continue

        sample_index = int(selected)
        if 1 <= sample_index <= len(samples):
            return samples[sample_index - 1]

        print("编号超出范围，请重新输入。")


def run_interactive_menu() -> int:
    options = [
        ("list", "列出 test 目录下的共享 JSON 样例", handle_list),
        ("encode", "对选定样例执行图灵机编码", handle_encode),
        ("multitape", "运行多带图灵机模拟器", handle_multitape),
        ("utm", "运行通用图灵机模拟器", handle_utm),
        ("exit", "退出程序", None),
    ]

    while True:
        print("请选择功能:")
        for index, (_, description, _) in enumerate(options, start=1):
            print(f"{index}. {description}")

        try:
            selected = input("请输入编号: ").strip()
        except KeyboardInterrupt:
            print("\n请输入菜单中的「退出程序」选项结束程序。")
            continue

        if not selected.isdigit():
            print("请输入有效的数字编号。\n")
            continue

        option_index = int(selected)
        if not 1 <= option_index <= len(options):
            print("编号超出范围，请重新输入。\n")
            continue

        command, _, handler = options[option_index - 1]
        if command == "exit":
            print("已退出。")
            return 0

        args = argparse.Namespace(
            command=command,
            sample=None,
            details=False,
            mode="interactive",
            interval=0.5,
            config=None,
            max_steps=10000
        )
        try:
            handler(args)
        except AppError as error:
            print(f"错误: {error}")
        except KeyboardInterrupt:
            print("\n已取消当前操作，返回主菜单。")

        print("")