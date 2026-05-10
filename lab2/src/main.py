"""
3SAT归约程序主入口

本程序实现3SAT到点覆盖(Vertex Cover)和独立集(Independent Set)的归约。
按照规格说明要求，从txt文件读取3SAT公式，执行归约并输出图片。

使用方法:
    python src/main.py --task 1 --input test/task1_course_example.txt
    python src/main.py --task 2 --input test/task2_course_example.txt
    python src/main.py --all  # 运行所有测试用例
    
注意：请从项目根目录运行此脚本
"""

import argparse
import os
import sys
from pathlib import Path

# 确保从项目根目录运行
# 获取脚本所在目录 (src目录)
script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
project_root = os.path.dirname(script_dir)

# 将项目根目录添加到路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.parsers import parse_txt_file
from src.models import Formula3SAT
from src.utils import draw_reduction_graph_spec, format_node_label


def run_task1(input_file: str, output_dir: str = "output") -> None:
    """
    运行任务1：3SAT到点覆盖的归约
    
    Args:
        input_file: 输入txt文件路径
        output_dir: 输出图片目录
    """
    print(f"\n{'='*60}")
    print(f"任务1：3SAT → 点覆盖 (Vertex Cover)")
    print(f"{'='*60}")
    
    # 解析输入文件
    print(f"\n读取输入文件: {input_file}")
    formula = parse_txt_file(input_file)
    print(f"解析成功！")
    print(f"  公式: {formula}")
    print(f"  子句数量: {len(formula)}")
    print(f"  变量数量: {formula.get_variable_count()}")
    print(f"  变量集合: {formula.get_variables()}")
    
    # 执行归约
    print(f"\n执行归约...")
    try:
        from src.reductions import reduce_3sat_to_vertex_cover
        graph, k = reduce_3sat_to_vertex_cover(formula)
        print(f"归约完成！")
        print(f"  图节点数: {graph.node_count()}")
        print(f"  图边数: {graph.edge_count()}")
        print(f"  点覆盖大小 k = {k}")
        
        # 生成输出图片
        output_filename = Path(input_file).stem + "_vertex_cover.png"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\n生成输出图片: {output_path}")
        
        # 获取公式字符串
        formula_str = str(formula)
        
        # 绘制归约结果图
        draw_reduction_graph_spec(
            formula_str=formula_str,
            graph=graph,
            k_or_n=k,
            problem_type="Vertex Cover",
            output_path=output_path
        )
        
        print(f"图片已保存！")
        print(f"\n问题：在上图中是否存在大小不超过 k = {k} 的点覆盖？")
        
    except NotImplementedError:
        print(f"⚠️  归约函数尚未实现！")
        print(f"   请在 src/reductions/vertex_cover.py 中实现 reduce_3sat_to_vertex_cover 函数")
        print(f"\n   当前已完成的准备工作：")
        print(f"   - 输入文件解析成功")
        print(f"   - 公式结构验证通过")
        print(f"   - 等待归约算法实现...")


def run_task2(input_file: str, output_dir: str = "output") -> None:
    """
    运行任务2：3SAT到独立集的归约
    
    Args:
        input_file: 输入txt文件路径
        output_dir: 输出图片目录
    """
    print(f"\n{'='*60}")
    print(f"任务2：3SAT → 独立集 (Independent Set)")
    print(f"{'='*60}")
    
    # 解析输入文件
    print(f"\n读取输入文件: {input_file}")
    formula = parse_txt_file(input_file)
    print(f"解析成功！")
    print(f"  公式: {formula}")
    print(f"  子句数量: {len(formula)}")
    print(f"  变量数量: {formula.get_variable_count()}")
    print(f"  变量集合: {formula.get_variables()}")
    
    # 执行归约
    print(f"\n执行归约...")
    try:
        from src.reductions import reduce_3sat_to_independent_set
        graph, n = reduce_3sat_to_independent_set(formula)
        print(f"归约完成！")
        print(f"  图节点数: {graph.node_count()}")
        print(f"  图边数: {graph.edge_count()}")
        print(f"  独立集大小 n = {n}")
        
        # 生成输出图片
        output_filename = Path(input_file).stem + "_independent_set.png"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\n生成输出图片: {output_path}")
        
        # 获取公式字符串
        formula_str = str(formula)
        
        # 绘制归约结果图
        draw_reduction_graph_spec(
            formula_str=formula_str,
            graph=graph,
            k_or_n=n,
            problem_type="Independent Set",
            output_path=output_path
        )
        
        print(f"图片已保存！")
        print(f"\n问题：在上图中是否存在大小至少为 n = {n} 的独立集？")
        
    except NotImplementedError:
        print(f"⚠️  归约函数尚未实现！")
        print(f"   请在 src/reductions/independent_set.py 中实现 reduce_3sat_to_independent_set 函数")
        print(f"\n   当前已完成的准备工作：")
        print(f"   - 输入文件解析成功")
        print(f"   - 公式结构验证通过")
        print(f"   - 等待归约算法实现...")


def run_all_tests(output_dir: str = "output") -> None:
    """
    运行所有测试用例
    
    Args:
        output_dir: 输出图片目录
    """
    print(f"\n{'='*60}")
    print(f"运行所有测试用例")
    print(f"{'='*60}")
    
    # 使用项目根目录下的test目录
    test_dir = os.path.join(project_root, "test")
    
    # 任务1测试用例
    task1_files = [
        "task1_course_example.txt",
        "task1_custom_example.txt"
    ]
    
    # 任务2测试用例
    task2_files = [
        "task2_course_example.txt",
        "task2_custom_example.txt"
    ]
    
    print(f"\n任务1测试用例：")
    for filename in task1_files:
        filepath = os.path.join(test_dir, filename)
        if os.path.exists(filepath):
            run_task1(filepath, output_dir)
        else:
            print(f"  ⚠️  文件不存在: {filepath}")
    
    print(f"\n任务2测试用例：")
    for filename in task2_files:
        filepath = os.path.join(test_dir, filename)
        if os.path.exists(filepath):
            run_task2(filepath, output_dir)
        else:
            print(f"  ⚠️  文件不存在: {filepath}")


def main():
    """
    主函数：解析命令行参数并执行相应任务
    """
    parser = argparse.ArgumentParser(
        description="3SAT归约程序：将3SAT归约到点覆盖和独立集",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python src/main.py --task 1 --input test/task1_course_example.txt
  python src/main.py --task 2 --input test/task2_course_example.txt
  python src/main.py --all
  python src/main.py --test-parser test/task1_course_example.txt
  
注意：请从项目根目录运行此脚本
        """
    )
    
    parser.add_argument(
        '--task', type=int, choices=[1, 2],
        help='运行指定任务 (1: 点覆盖, 2: 独立集)'
    )
    
    parser.add_argument(
        '--input', type=str,
        help='输入txt文件路径'
    )
    
    parser.add_argument(
        '--all', action='store_true',
        help='运行所有测试用例'
    )
    
    parser.add_argument(
        '--test-parser', type=str,
        help='仅测试解析器，不执行归约'
    )
    
    parser.add_argument(
        '--output-dir', type=str, default=os.path.join(project_root, 'output'),
        help='输出图片目录 (默认: output)'
    )
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # 根据参数执行相应操作
    if args.test_parser:
        # 仅测试解析器
        print(f"\n测试解析器: {args.test_parser}")
        formula = parse_txt_file(args.test_parser)
        print(f"解析成功！")
        print(f"  公式: {formula}")
        print(f"  子句数量: {len(formula)}")
        print(f"  变量: {formula.get_variables()}")
        
    elif args.all:
        # 运行所有测试
        run_all_tests(args.output_dir)
        
    elif args.task and args.input:
        # 运行指定任务
        if args.task == 1:
            run_task1(args.input, args.output_dir)
        else:
            run_task2(args.input, args.output_dir)
            
    else:
        # 无参数时显示帮助
        parser.print_help()
        print(f"\n提示：请使用 --task 和 --input 参数指定任务和输入文件")
        print(f"      或使用 --all 运行所有测试用例")


if __name__ == "__main__":
    main()