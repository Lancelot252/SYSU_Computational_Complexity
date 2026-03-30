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

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="统一图灵机程序入口。当前已实现图灵机编码模块。"
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

    multitape_parser = subparsers.add_parser("multitape", help="预留：多带图灵机模块")
    multitape_parser.set_defaults(handler=handle_multitape)

    utm_parser = subparsers.add_parser("utm", help="预留：通用图灵机模块")
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


def handle_multitape(_args: argparse.Namespace) -> int:
    raise NotImplementedFeatureError("多带图灵机模块尚未实现，当前仅预留统一 CLI 接口。")


def handle_utm(_args: argparse.Namespace) -> int:
    raise NotImplementedFeatureError("通用图灵机模块尚未实现，当前仅预留统一 CLI 接口。")


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
        ("multitape", "预留：多带图灵机模块", handle_multitape),
        ("utm", "预留：通用图灵机模块", handle_utm),
        ("exit", "退出程序", None),
    ]

    while True:
        print("请选择功能:")
        for index, (_, description, _) in enumerate(options, start=1):
            print(f"{index}. {description}")

        try:
            selected = input("请输入编号: ").strip()
        except KeyboardInterrupt:
            print("\n请输入菜单中的“退出程序”选项结束程序。")
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

        args = argparse.Namespace(command=command, sample=None, details=False)
        try:
            handler(args)
        except AppError as error:
            print(f"错误: {error}")
        except KeyboardInterrupt:
            print("\n已取消当前操作，返回主菜单。")

        print("")