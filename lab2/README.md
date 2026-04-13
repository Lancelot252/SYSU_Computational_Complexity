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
├── src/                         # 源代码目录
│   ├── __init__.py
│   ├── models/                  # 公共数据结构模块
│   │   ├── __init__.py
│   │   ├── formula.py           # 3SAT公式数据结构
│   │   └── graph.py             # 图数据结构
│   ├── parsers/                 # 解析器模块
│   │   ├── __init__.py
│   │   └── cnf_parser.py        # CNF公式解析器
│   ├── reductions/              # 归约算法模块
│   │   ├── __init__.py
│   │   ├── vertex_cover.py      # 任务1接口
│   │   └── independent_set.py   # 任务2接口
│   └── utils/                   # 工具模块
│       ├── __init__.py
│       └── visualization.py     # 可视化工具
├── tests/                       # 测试用例
│   ├── __init__.py
│   ├── test_formula.py          # Formula测试
│   ├── test_graph.py            # Graph测试
│   └── test_cases.py            # 预定义测试用例
└── docs/
    └── API.md                    # 接口说明文档
```

## 安装依赖

```bash
pip install networkx matplotlib
```

## 使用方法

### 1. 解析3SAT公式

```python
from src.parsers import parse_cnf_string

# 数学符号格式
formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")

# 编程格式
formula = parse_cnf_string("(x|y|~z)&(~x|~y|z)")

# DIMACS格式文件
from src.parsers import parse_dimacs
formula = parse_dimacs("input.cnf")
```

### 2. 使用数据结构

```python
from src.models import Literal, Clause, Formula3SAT, Graph

# 创建文字
lit = Literal('x', False)    # x
lit_neg = Literal('x', True)  # ¬x

# 创建子句
clause = Clause([Literal('x'), Literal('y'), Literal('z', True)])

# 创建图
graph = Graph()
node1 = graph.add_node("x")
node2 = graph.add_node("¬x")
graph.add_edge(node1, node2)
```

### 3. 执行归约

```python
from src.reductions import reduce_3sat_to_vertex_cover, reduce_3sat_to_independent_set
from src.parsers import parse_cnf_string

formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")

# 任务1: 3SAT → 节点覆盖
graph, k = reduce_3sat_to_vertex_cover(formula)

# 任务2: 3SAT → 独立集
graph, n = reduce_3sat_to_independent_set(formula)
```

### 4. 可视化

```python
from src.utils import draw_graph, draw_graph_with_highlight

# 绘制图
draw_graph(graph, "output.png", "归约结果")

# 高亮显示特定节点
draw_graph_with_highlight(graph, {0, 1}, "highlight.png", "独立集")
```

### 5. 运行测试

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
- 实现CNF解析器
- 定义归约接口
- 编写测试用例
- 实现可视化工具
- 编写文档（README.md, API.md）

### 人员B（待实现）
需要实现以下函数（位于 `src/reductions/vertex_cover.py`）：

1. `reduce_3sat_to_vertex_cover(formula)` - 主归约函数
2. `verify_vertex_cover_reduction(formula, graph, k)` - 验证归约正确性
3. `extract_satisfying_assignment(formula, graph, vertex_cover)` - 从解提取赋值

**归约原理**:
- 对于每个子句，创建一个三角形（3个节点代表3个文字）
- 在互为否定的文字节点之间添加边
- 覆盖大小 k = 子句数 × 2 + 变量数

### 人员C（待实现）
需要实现以下函数（位于 `src/reductions/independent_set.py`）：

1. `reduce_3sat_to_independent_set(formula)` - 主归约函数
2. `verify_independent_set_reduction(formula, graph, n)` - 验证归约正确性
3. `extract_satisfying_assignment(formula, graph, independent_set)` - 从解提取赋值

**归约原理**:
- 对于每个子句，创建一个三角形（3个节点代表3个文字）
- 在互为否定的文字节点之间添加边
- 独立集大小 n = 子句数

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

## 测试用例

项目包含以下预定义测试用例：

| 名称 | 公式 | 子句数 | 变量数 |
|------|------|--------|--------|
| 课件例子 | (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z) | 3 | 3 |
| 自定义例子 | (x ∨ y ∨ ¬z) ∧ (¬x ∨ z ∨ w) ∧ ... | 6 | 5 |
| 简单可满足 | (x ∨ y ∨ z) | 1 | 3 |

## API文档

详细的API文档请参见 [`docs/API.md`](docs/API.md)。

## 注意事项

1. 所有代码使用Python 3.8+语法
2. 使用类型注解(type hints)
3. 遵循PEP 8代码风格
4. 归约函数目前抛出 `NotImplementedError`，需要人员B和C实现

## 许可证

本项目仅供教育目的使用。