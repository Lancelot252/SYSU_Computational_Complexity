# lab2 - NP完全性归约项目

计算复杂性课程第二次编程作业：3SAT到节点覆盖和独立集的归约实现。

## 项目概述

本项目实现了以下NP完全性归约：
- **任务1**: 3SAT → 节点覆盖 (Vertex Cover)
- **任务2**: 3SAT → 独立集 (Independent Set)

通过这些归约，我们证明了节点覆盖问题和独立集问题都是NP完全的。

## 目录结构

```
lab2/
├── README.md                    # 项目说明文档
├── main.py                      # 主程序入口
├── src/                         # 源代码目录
│   ├── __init__.py
│   ├── models/                  # 公共数据结构模块
│   │   ├── __init__.py
│   │   ├── formula.py           # 3SAT公式数据结构
│   │   └── graph.py             # 图数据结构
│   ├── parsers/                 # 解析器模块
│   │   ├── __init__.py
│   │   └── cnf_parser.py        # CNF公式解析器（支持多种格式）
│   ├── reductions/              # 归约算法模块
│   │   ├── __init__.py
│   │   ├── vertex_cover.py      # 任务1接口
│   │   └── independent_set.py   # 任务2接口
│   └── utils/                   # 工具模块
│       ├── __init__.py
│       └── visualization.py     # 可视化工具
├── test/                        # txt测试用例文件
│   ├── task1_course_example.txt # 任务1课件例子
│   ├── task1_custom_example.txt # 任务1自设计例子
│   ├── task2_course_example.txt # 任务2课件例子
│   └ task2_custom_example.txt   # 任务2自设计例子
├── tests/                       # Python测试用例
│   ├── __init__.py
│   ├── test_formula.py          # Formula测试
│   ├── test_graph.py            # Graph测试
│   └── test_cases.py            # 预定义测试用例
├── output/                      # 输出图片目录
│   └── .gitkeep                 # 保持目录在git中被跟踪
└── docs/
    ├── API.md                   # 接口说明文档
    ├── report.tex               # 实验报告框架
    └── figs/                    # 报告图片目录
```

## 安装依赖

```bash
pip install networkx matplotlib
```

## 使用方法

### 1. 运行主程序

```bash
python src/main.py --task 1 --input test/task1_course_example.txt
python src/main.py --task 2 --input test/task2_course_example.txt
python src/main.py --all
```

### 2. 解析3SAT公式

```python
from src.parsers import parse_txt_file, parse_cnf_string, parse_dimacs

# txt格式（本次作业规定格式）
formula = parse_txt_file("test/task1_course_example.txt")

# 数学符号格式
formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")

# 编程格式
formula = parse_cnf_string("(x|y|~z)&(~x|~y|z)")

# DIMACS格式文件
formula = parse_dimacs("input.cnf")
```

### 3. txt文件格式说明

本次作业规定的txt文件格式：
- 每一行表示一个子句
- 每一行包含恰好3个文字，以空格分隔
- 正文字直接写变量名，例如 `x`
- 负文字在变量名前加 `-`，例如 `-x` 表示 `¬x`

示例文件内容：
```
x y z 
-x -y -z 
x -y z 
-x y -z
```

对应公式：`(x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z) ∧ (x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)`

### 4. 使用数据结构

```python
from src.models import Literal, Clause, Formula3SAT, Graph

# 创建文字
lit = Literal('x', False)    # x
lit_neg = Literal('x', True)  # ¬x

# 创建子句
clause = Clause([Literal('x'), Literal('y'), Literal('z', True)])

# 创建图
graph = Graph()
node1 = graph.add_node("C1:x")
node2 = graph.add_node("C1:¬x")
graph.add_edge(node1, node2)
```

### 5. 执行归约

```python
from src.reductions import reduce_3sat_to_vertex_cover, reduce_3sat_to_independent_set
from src.parsers import parse_txt_file

formula = parse_txt_file("test/task1_course_example.txt")

# 任务1: 3SAT → 节点覆盖
graph, k = reduce_3sat_to_vertex_cover(formula)

# 任务2: 3SAT → 独立集
graph, n = reduce_3sat_to_independent_set(formula)
```

### 6. 可视化输出

```python
from src.utils import draw_reduction_graph_spec, draw_graph

# 按规格说明要求绘制归约结果
draw_reduction_graph_spec(
    formula_str=str(formula),
    graph=graph,
    k_or_n=k,
    problem_type="Vertex Cover",
    output_path="output/result.png"
)

# 基本绘图
draw_graph(graph, "output.png", "归约结果")
```

### 7. 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行单个测试文件
python tests/test_formula.py
python tests/test_graph.py
python tests/test_cases.py
```

## 分工说明

### 人员A（已完成）
- 创建项目框架和目录结构
- 实现公共数据结构（`Literal`, `Clause`, `Formula3SAT`, `Graph`）
- 实现CNF解析器（支持多种格式）
- 实现txt文件解析器（规格说明要求的格式）
- 定义归约接口
- 编写测试用例
- 实现可视化工具（符合规格说明要求）
- 创建主程序入口 `main.py`
- 创建txt测试用例文件
- 编写文档（README.md, API.md）
- 创建实验报告框架

### 人员B（待实现）
需要实现以下函数（位于 `src/reductions/vertex_cover.py`）：

1. `reduce_3sat_to_vertex_cover(formula)` - 主归约函数
2. `verify_vertex_cover_reduction(formula, graph, k)` - 验证归约正确性
3. `extract_satisfying_assignment(formula, graph, vertex_cover)` - 从解提取赋值

**归约原理**:
- 对于每个子句，创建一个三角形（3个节点代表3个文字）
- 同一个子句内的3个节点两两相连
- 对任意两个互补文字（例如 x 与 -x）对应的节点添加边
- 覆盖大小 k = 2m（m为子句数）

**正确性**:
- φ 可满足 ⟺ G 存在大小不超过 k 的点覆盖

### 人员C（待实现）
需要实现以下函数（位于 `src/reductions/independent_set.py`）：

1. `reduce_3sat_to_independent_set(formula)` - 主归约函数
2. `verify_independent_set_reduction(formula, graph, n)` - 验证归约正确性
3. `extract_satisfying_assignment(formula, graph, independent_set)` - 从解提取赋值

**归约原理**:
- 对于每个子句，创建一个三角形（3个节点代表3个文字）
- 同一个子句内的3个节点两两相连
- 对任意两个互补文字（例如 x 与 -x）对应的节点添加边
- 独立集大小 n = m（m为子句数）

**正确性**:
- φ 可满足 ⟺ G 存在大小至少为 n 的独立集

## 归约正确性证明

### 3SAT → 节点覆盖
**定理**: 3SAT公式 φ 可满足 ⟺ 归约后的图 G 存在大小为 k 的节点覆盖

**证明要点**:
1. 如果 φ 可满足，取满足赋值中为真的文字对应的节点，加上每个子句中另外2个节点，构成大小为 k 的覆盖
2. 如果 G 存在大小为 k 的覆盖，从覆盖中选择满足赋值

### 3SAT → 独立集
**定理**: 3SAT公式 φ 可满足 ⟺ 归约后的图 G 存在大小为 n 的独立集

**证明要点**:
1. 如果 φ 可满足，取每个子句中为真的文字节点，构成大小为 n 的独立集
2. 如果 G 存在大小为 n 的独立集，独立集中的节点给出满足赋值

**运行测试**:
```bash
# 运行independent_set测试文件
python tests/test_independent_set.py
```
测试用例保存于：
`test\task2_course_example.txt`与`test\task2_custom_example.txt`中

图片输出保存于：
`output\independent_set_course_example.png`与`output\independent_set_custom_example.png`中

## 测试用例

### 任务1测试用例

| 文件名 | 公式 | 子句数 | 变量数 |
|--------|------|--------|--------|
| task1_course_example.txt | (x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z) ∧ (x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z) | 4 | 3 |
| task1_custom_example.txt | (x ∨ y ∨ ¬z) ∧ (¬x ∨ z ∨ w) ∧ ... | 6 | 5 |

### 任务2测试用例

| 文件名 | 公式 | 子句数 | 变量数 |
|--------|------|--------|--------|
| task2_course_example.txt | (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z) | 3 | 3 |
| task2_custom_example.txt |(x∨¬y∨z)∧(¬x∨y∨¬z)∧(y∨¬z∨w)∧(¬y∨z∨¬w)∧(x∨¬w∨¬z)| 5 | 5 |

## 输出图片规范

程序输出的图片满足以下要求：
1. **完整图结构**：展示归约后图的全部节点和全部边
2. **圆形节点**：节点绘制为圆形，带有清晰标签（如 `C2:¬x`）
3. **边清晰可见**：使用不同线型区分子句内部边和互补文字之间的边
4. **问题文本描述**：图片中展示输入3SAT公式和所规约问题的文本

## API文档

详细的API文档请参见 [`API.md`](API.md)。

## 注意事项

1. 所有代码使用Python 3.8+语法
2. 使用类型注解(type hints)
3. 遵循PEP 8代码风格
4. 归约函数目前抛出 `NotImplementedError`，需要人员B和C实现
5. 运行前请确保已安装 `networkx` 和 `matplotlib` 库

## 许可证

本项目仅供教育目的使用。