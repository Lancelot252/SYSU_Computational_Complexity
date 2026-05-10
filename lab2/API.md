# API 接口文档

本文档详细说明了lab2项目中所有类和函数的接口定义。

## 目录

1. [数据模型 (models)](#数据模型-models)
   - [Literal](#literal)
   - [Clause](#clause)
   - [Formula3SAT](#formula3sat)
   - [Graph](#graph)
2. [解析器 (parsers)](#解析器-parsers)
   - [parse_txt_file](#parse_txt_file)
   - [parse_txt_string](#parse_txt_string)
   - [parse_cnf_string](#parse_cnf_string)
   - [parse_dimacs](#parse_dimacs)
   - [parse_dimacs_string](#parse_dimacs_string)
3. [归约算法 (reductions)](#归约算法-reductions)
   - [任务1: 3SAT到节点覆盖](#任务1-3sat到节点覆盖)
   - [任务2: 3SAT到独立集](#任务2-3sat到独立集)
4. [可视化工具 (utils)](#可视化工具-utils)
5. [主程序 (main.py)](#主程序-mainpy)
6. [测试用例 (tests)](#测试用例-tests)

---

## 数据模型 (models)

### Literal

文字类，表示一个布尔变量或其否定形式。

```python
from src.models import Literal

# 创建正文字
lit_pos = Literal('x', False)  # 表示 x

# 创建负文字
lit_neg = Literal('x', True)   # 表示 ¬x
```

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `variable` | `str` | 变量名，如 'x', 'y', 'z' |
| `negated` | `bool` | 是否取反，True 表示取反 |

#### 方法

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `__str__()` | `str` | 返回字符串表示，如 "x" 或 "¬x" |
| `__repr__()` | `str` | 返回正式表示，如 "Literal('x', False)" |
| `__eq__(other)` | `bool` | 判断两个文字是否相等 |
| `__hash__()` | `int` | 返回哈希值，可用于集合和字典 |
| `negate()` | `Literal` | 返回取反的文字 |

#### 示例

```python
lit = Literal('x', False)
print(lit)          # 输出: x
print(lit.negate()) # 输出: ¬x

# 文字可以放入集合
literals = {Literal('x', False), Literal('y', True)}
```

---

### Clause

子句类，表示3个文字的析取（OR）。

```python
from src.models import Literal, Clause

# 创建子句 (x ∨ y ∨ ¬z)
clause = Clause([
    Literal('x', False),
    Literal('y', False),
    Literal('z', True)
])
```

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `literals` | `List[Literal]` | 包含3个文字的列表 |

#### 方法

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `__str__()` | `str` | 返回字符串表示，如 "(x ∨ y ∨ ¬z)" |
| `__iter__()` | `Iterator[Literal]` | 支持迭代遍历文字 |
| `__len__()` | `int` | 返回文字数量（总是3） |
| `get_variables()` | `Set[str]` | 返回子句中所有变量名 |

#### 示例

```python
clause = Clause([
    Literal('x', False),
    Literal('y', False),
    Literal('z', True)
])

print(clause)  # 输出: (x ∨ y ∨ ¬z)

# 遍历子句中的文字
for lit in clause:
    print(lit)

# 获取变量集合
variables = clause.get_variables()  # {'x', 'y', 'z'}
```

---

### Formula3SAT

3SAT公式类，表示多个子句的合取（AND）。

```python
from src.models import Literal, Clause, Formula3SAT

# 创建公式 (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)
formula = Formula3SAT([
    Clause([Literal('x', False), Literal('y', False), Literal('z', True)]),
    Clause([Literal('x', True), Literal('y', True), Literal('z', False)])
])
```

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `clauses` | `List[Clause]` | 子句列表 |
| `variables` | `Set[str]` | 所有变量集合 |

#### 方法

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `__str__()` | `str` | 返回字符串表示 |
| `__iter__()` | `Iterator[Clause]` | 支持迭代遍历子句 |
| `__len__()` | `int` | 返回子句数量 |
| `get_clause_count()` | `int` | 获取子句数量 |
| `get_variable_count()` | `int` | 获取变量数量 |
| `get_clauses()` | `List[Clause]` | 获取所有子句 |
| `get_variables()` | `Set[str]` | 获取所有变量 |
| `from_string(s)` | `Formula3SAT` | 从字符串解析（类方法） |

#### 示例

```python
# 从字符串创建公式
formula = Formula3SAT.from_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")

print(formula)  # 输出: (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)
print(f"子句数: {len(formula)}")  # 输出: 子句数: 2
print(f"变量数: {formula.get_variable_count()}")  # 输出: 变量数: 3

# 遍历公式中的子句
for clause in formula:
    print(clause)
```

---

### Graph

无向图类，用于表示归约后的图结构。

```python
from src.models import Graph

graph = Graph()
```

#### 方法

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `add_node(label)` | `int` | 添加节点，返回节点ID |
| `add_edge(u, v)` | `None` | 添加无向边 |
| `remove_node(node_id)` | `None` | 移除节点及其关联边 |
| `remove_edge(u, v)` | `None` | 移除边 |
| `nodes()` | `List[int]` | 获取所有节点ID |
| `edges()` | `List[Tuple[int, int]]` | 获取所有边 |
| `node_count()` | `int` | 获取节点数量 |
| `edge_count()` | `int` | 获取边数量 |
| `get_label(node_id)` | `str` | 获取节点标签 |
| `set_label(node_id, label)` | `None` | 设置节点标签 |
| `neighbors(node_id)` | `Set[int]` | 获取节点的邻居 |
| `degree(node_id)` | `int` | 获取节点的度数 |
| `has_edge(u, v)` | `bool` | 检查边是否存在 |
| `has_node(node_id)` | `bool` | 检查节点是否存在 |
| `copy()` | `Graph` | 创建图的深拷贝 |
| `to_networkx()` | `nx.Graph` | 转换为networkx图 |
| `is_vertex_cover(vertices)` | `bool` | 检查是否是顶点覆盖 |
| `is_independent_set(vertices)` | `bool` | 检查是否是独立集 |
| `get_node_labels()` | `Dict[int, str]` | 获取所有节点标签 |
| `get_adjacency_dict()` | `Dict[int, Set[int]]` | 获取邻接表 |

#### 示例

```python
graph = Graph()

# 添加节点
node1 = graph.add_node("C1:x")
node2 = graph.add_node("C1:¬x")
node3 = graph.add_node("C2:y")

# 添加边
graph.add_edge(node1, node2)
graph.add_edge(node1, node3)

print(f"节点数: {graph.node_count()}")  # 输出: 3
print(f"边数: {graph.edge_count()}")    # 输出: 2

# 检查顶点覆盖
cover = {node1}
print(graph.is_vertex_cover(cover))  # 输出: True

# 检查独立集
ind_set = {node2, node3}
print(graph.is_independent_set(ind_set))  # 输出: True
```

---

## 解析器 (parsers)

### parse_txt_file

解析txt格式的3SAT公式文件（本次作业规定的输入格式）。

```python
from src.parsers import parse_txt_file

formula = parse_txt_file("test/task1_course_example.txt")
```

#### txt文件格式说明

本次作业规定的格式：
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

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `file_path` | `str` | txt文件路径 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `Formula3SAT` | 解析后的公式对象 |

#### 异常

| 异常 | 说明 |
|------|------|
| `FileNotFoundError` | 文件不存在 |
| `ValueError` | 文件格式无效或子句不包含恰好3个文字 |

#### 示例

```python
# 解析txt文件
formula = parse_txt_file("test/task1_course_example.txt")
print(formula)
# 输出: (x ∨ y ∨ z) ∧ (¬x ∨ ¬y ∨ ¬z) ∧ (x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)

print(f"子句数: {len(formula)}")  # 输出: 4
print(f"变量: {formula.get_variables()}")  # 输出: {'x', 'y', 'z'}
```

---

### parse_txt_string

解析txt格式的3SAT公式字符串。

```python
from src.parsers import parse_txt_string

formula = parse_txt_string("x y z\n-x -y -z\nx -y z")
```

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `s` | `str` | txt格式的公式字符串 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `Formula3SAT` | 解析后的公式对象 |

---

### parse_cnf_string

解析CNF格式字符串，支持多种格式。

```python
from src.parsers import parse_cnf_string

formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
```

#### 支持的格式

1. **数学符号格式**: `(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)`
2. **编程格式**: `(x|y|~z)&(~x|~y|z)`
3. **简化格式**: `(x+y+!z)*(!x+!y+z)`

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `s` | `str` | CNF公式字符串 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `Formula3SAT` | 解析后的公式对象 |

#### 示例

```python
# 数学符号格式
formula1 = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")

# 编程格式
formula2 = parse_cnf_string("(x|y|~z)&(~x|~y|z)")

# 简化格式
formula3 = parse_cnf_string("(x+y+!z)*(!x+!y+z)")
```

---

### parse_dimacs

解析DIMACS CNF格式文件。

```python
from src.parsers import parse_dimacs

formula = parse_dimacs("input.cnf")
```

#### DIMACS格式说明

```
c 这是注释
p cnf 3 2    # 3个变量，2个子句
1 -2 3 0     # 子句1: x1 ∨ ¬x2 ∨ x3
-1 -2 3 0    # 子句2: ¬x1 ∨ ¬x2 ∨ x3
```

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `file_path` | `str` | DIMACS CNF文件路径 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `Formula3SAT` | 解析后的公式对象 |

---

### parse_dimacs_string

解析DIMACS CNF格式字符串。

```python
from src.parsers import parse_dimacs_string

dimacs_str = "c 注释\np cnf 3 2\n1 -2 3 0\n-1 -2 3 0"
formula = parse_dimacs_string(dimacs_str)
```

---

## 归约算法 (reductions)

### 任务1: 3SAT到节点覆盖

#### reduce_3sat_to_vertex_cover

将3SAT公式归约为节点覆盖问题。

```python
from src.reductions import reduce_3sat_to_vertex_cover
from src.parsers import parse_txt_file

formula = parse_txt_file("test/task1_course_example.txt")
graph, k = reduce_3sat_to_vertex_cover(formula)
```

**⚠️ 此函数需要由人员B实现！**

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `formula` | `Formula3SAT` | 3SAT公式 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `Tuple[Graph, int]` | 图G和覆盖大小k |

#### 归约原理

1. 对于每个子句，创建一个三角形（3个节点，每个节点代表一个文字）
2. 同一个子句内的3个节点两两相连
3. 对任意两个互补文字（例如 x 与 -x）对应的节点添加边
4. 覆盖大小 k = 2m（m为子句数）

**正确性保证**: 公式可满足 ⟺ G存在大小不超过k的节点覆盖

---

#### verify_vertex_cover_reduction

验证归约的正确性。

**⚠️ 此函数需要由人员B实现！**

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `formula` | `Formula3SAT` | 原始公式 |
| `graph` | `Graph` | 归约后的图 |
| `k` | `int` | 覆盖大小 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `bool` | 归约是否正确 |

---

#### extract_satisfying_assignment

从节点覆盖解中提取满足赋值。

**⚠️ 此函数需要由人员B实现！**

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `formula` | `Formula3SAT` | 原始公式 |
| `graph` | `Graph` | 归约后的图 |
| `vertex_cover` | `set` | 节点覆盖集合 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `dict` | 变量名到布尔值的映射 |

---

### 任务2: 3SAT到独立集

#### reduce_3sat_to_independent_set

将3SAT公式归约为独立集问题。

```python
from src.reductions import reduce_3sat_to_independent_set
from src.parsers import parse_txt_file

formula = parse_txt_file("test/task2_course_example.txt")
graph, n = reduce_3sat_to_independent_set(formula)
```

**⚠️ 此函数需要由人员C实现！**

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `formula` | `Formula3SAT` | 3SAT公式 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `Tuple[Graph, int]` | 图G和独立集大小n |

#### 归约原理

1. 对于每个子句，创建一个三角形（3个节点，每个节点代表一个文字）
2. 同一个子句内的3个节点两两相连
3. 对任意两个互补文字（例如 x 与 -x）对应的节点添加边
4. 独立集大小 n = m（m为子句数）

**正确性保证**: 公式可满足 ⟺ G存在大小至少为n的独立集

---

#### verify_independent_set_reduction

验证归约的正确性。

**⚠️ 此函数需要由人员C实现！**

---

#### extract_satisfying_assignment

从独立集解中提取满足赋值。

**⚠️ 此函数需要由人员C实现！**

---

### 辅助函数

#### vertex_cover_to_independent_set

将节点覆盖问题转换为独立集问题。

```python
from src.reductions import vertex_cover_to_independent_set

graph, n = vertex_cover_to_independent_set(graph, k)
# n = graph.node_count() - k
```

#### independent_set_to_vertex_cover

将独立集问题转换为节点覆盖问题。

```python
from src.reductions import independent_set_to_vertex_cover

graph, k = independent_set_to_vertex_cover(graph, n)
# k = graph.node_count() - n
```

---

## 可视化工具 (utils)

### draw_graph

绘制图并保存或显示。

```python
from src.utils import draw_graph

draw_graph(graph, "output.png", "示例图")
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `graph` | `Graph` | 必需 | 要绘制的图 |
| `output_path` | `str` | `None` | 输出文件路径，None则显示 |
| `title` | `str` | `None` | 图标题 |
| `figsize` | `tuple` | `(10, 8)` | 图形大小 |

---

### draw_graph_with_highlight

绘制图并高亮特定节点。

```python
from src.utils import draw_graph_with_highlight

draw_graph_with_highlight(graph, {0, 1}, "output.png", "高亮图")
```

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `graph` | `Graph` | 必需 | 要绘制的图 |
| `highlight_nodes` | `Set[int]` | 必需 | 要高亮的节点 |
| `output_path` | `str` | `None` | 输出文件路径 |
| `title` | `str` | `None` | 图标题 |
| `highlight_color` | `str` | `'red'` | 高亮颜色 |
| `figsize` | `tuple` | `(10, 8)` | 图形大小 |

---

### draw_graph_with_vertex_cover

绘制图并显示顶点覆盖（绿色高亮）。

```python
from src.utils import draw_graph_with_vertex_cover

draw_graph_with_vertex_cover(graph, cover_set, "vc.png", "顶点覆盖")
```

---

### draw_graph_with_independent_set

绘制图并显示独立集（橙色高亮）。

```python
from src.utils import draw_graph_with_independent_set

draw_graph_with_independent_set(graph, ind_set, "is.png", "独立集")
```

---

### draw_reduction_graph_spec

按照规格说明要求绘制归约结果图。

```python
from src.utils import draw_reduction_graph_spec

draw_reduction_graph_spec(
    formula_str=str(formula),
    graph=graph,
    k_or_n=k,
    problem_type="Vertex Cover",
    output_path="output/result.png"
)
```

**满足规格说明要求**：
1. 完整图结构：展示全部节点和全部边
2. 圆形节点：节点绘制为圆形，标签包含子句编号和文字（如 C2:¬x）
3. 边清晰可见：使用不同线型区分子句内部边和互补文字之间的边
4. 问题文本描述：展示输入公式和所规约问题的文本

#### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `formula_str` | `str` | 必需 | 原始公式字符串 |
| `graph` | `Graph` | 必需 | 归约后的图 |
| `k_or_n` | `int` | 必需 | 覆盖大小或独立集大小 |
| `problem_type` | `str` | 必需 | "Vertex Cover" 或 "Independent Set" |
| `clause_edges` | `list` | `None` | 子句内部边列表 |
| `conflict_edges` | `list` | `None` | 互补文字边列表 |
| `output_path` | `str` | `None` | 输出文件路径 |
| `figsize` | `tuple` | `(12, 8)` | 图形大小 |

---

### format_node_label

格式化节点标签，符合规格说明要求。

```python
from src.utils import format_node_label

label = format_node_label(1, "x")   # 返回 "C1:x"
label = format_node_label(2, "¬x")  # 返回 "C2:¬x"
```

#### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `clause_index` | `int` | 子句编号（从1开始） |
| `literal_str` | `str` | 文字字符串 |

#### 返回值

| 类型 | 说明 |
|------|------|
| `str` | 格式化的标签 |

---

### create_comparison_plot

创建对比图，同时显示原图、顶点覆盖和独立集。

```python
from src.utils import create_comparison_plot

create_comparison_plot(graph, vertex_cover={0, 1}, 
                       independent_set={2, 3}, 
                       output_path="comparison.png")
```

---

## 主程序 (main.py)

### 命令行使用

```bash
# 运行任务1（点覆盖）
python main.py --task 1 --input test/task1_course_example.txt

# 运行任务2（独立集）
python main.py --task 2 --input test/task2_course_example.txt

# 运行所有测试用例
python main.py --all

# 仅测试解析器
python main.py --test-parser test/task1_course_example.txt

# 指定输出目录
python main.py --task 1 --input test/task1_course_example.txt --output-dir output
```

### 命令行参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `--task` | `int` | 运行指定任务 (1: 点覆盖, 2: 独立集) |
| `--input` | `str` | 输入txt文件路径 |
| `--all` | `flag` | 运行所有测试用例 |
| `--test-parser` | `str` | 仅测试解析器 |
| `--output-dir` | `str` | 输出图片目录（默认: output） |

---

## 测试用例 (tests)

### txt测试文件

| 文件名 | 任务 | 说明 |
|--------|------|------|
| `test/task1_course_example.txt` | 任务1 | 课件例子，4个子句 |
| `test/task1_custom_example.txt` | 任务1 | 自设计例子，6个子句 |
| `test/task2_course_example.txt` | 任务2 | 课件例子，3个子句 |
| `test/task2_custom_example.txt` | 任务2 | 自设计例子，6个子句 |

### Python测试用例

```python
from tests.test_cases import (
    COURSE_EXAMPLE,           # 课件例子字符串
    CUSTOM_EXAMPLE,           # 自定义5+子句例子字符串
    get_course_example,       # 获取课件例子Formula3SAT对象
    get_custom_example,       # 获取自定义例子Formula3SAT对象
    get_all_test_cases,       # 获取所有测试用例
    run_basic_tests           # 运行基本测试
)
```

#### 示例

```python
# 获取课件例子
formula = get_course_example()
print(formula)  # (x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z) ∧ (¬x ∨ y ∨ ¬z)

# 获取所有测试用例
for name, formula in get_all_test_cases():
    print(f"{name}: {formula}")

# 运行基本测试
run_basic_tests()
```

---

## 人员分工说明

### 人员A（已完成）
- 创建项目框架和目录结构
- 实现数据结构（Literal, Clause, Formula3SAT, Graph）
- 实现CNF解析器（支持多种格式）
- 实现txt文件解析器（规格说明要求的格式）
- 定义归约接口
- 实现可视化工具（符合规格说明要求）
- 创建主程序入口 main.py
- 创建txt测试用例文件
- 编写测试用例和文档
- 创建实验报告框架

### 人员B（待实现）
需要实现以下函数：
- `reduce_3sat_to_vertex_cover(formula)` - 3SAT到节点覆盖的归约
- `verify_vertex_cover_reduction(formula, graph, k)` - 验证归约正确性
- `extract_satisfying_assignment(formula, graph, vertex_cover)` - 从覆盖提取满足赋值

文件位置: `src/reductions/vertex_cover.py`

### 人员C（待实现）
需要实现以下函数：
- `reduce_3sat_to_independent_set(formula)` - 3SAT到独立集的归约
- `verify_independent_set_reduction(formula, graph, n)` - 验证归约正确性
- `extract_satisfying_assignment(formula, graph, independent_set)` - 从独立集提取满足赋值

文件位置: `src/reductions/independent_set.py`

---

## 使用示例

### 完整工作流程

```python
# 1. 导入模块
from src.parsers import parse_txt_file
from src.reductions import reduce_3sat_to_vertex_cover, reduce_3sat_to_independent_set
from src.utils import draw_reduction_graph_spec

# 2. 解析公式
formula = parse_txt_file("test/task1_course_example.txt")
print(f"公式: {formula}")

# 3. 执行归约（需要人员B和C实现）
# graph_vc, k = reduce_3sat_to_vertex_cover(formula)
# graph_is, n = reduce_3sat_to_independent_set(formula)

# 4. 可视化结果
# draw_reduction_graph_spec(str(formula), graph_vc, k, "Vertex Cover", "output/vc.png")
# draw_reduction_graph_spec(str(formula), graph_is, n, "Independent Set", "output/is.png")
```

---

## 依赖库

- Python 3.8+
- networkx（可视化）
- matplotlib（可视化）

安装依赖：
```bash
pip install networkx matplotlib
```

---

## 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/test_formula.py
python tests/test_graph.py
python tests/test_cases.py

# 测试解析器
python main.py --test-parser test/task1_course_example.txt