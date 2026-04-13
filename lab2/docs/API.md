# API 接口文档

本文档详细说明了lab2项目中所有类和函数的接口定义。

## 目录

1. [数据模型 (models)](#数据模型-models)
   - [Literal](#literal)
   - [Clause](#clause)
   - [Formula3SAT](#formula3sat)
   - [Graph](#graph)
2. [解析器 (parsers)](#解析器-parsers)
   - [parse_cnf_string](#parse_cnf_string)
   - [parse_dimacs](#parse_dimacs)
3. [归约算法 (reductions)](#归约算法-reductions)
   - [任务1: 3SAT到节点覆盖](#任务1-3sat到节点覆盖)
   - [任务2: 3SAT到独立集](#任务2-3sat到独立集)
4. [可视化工具 (utils)](#可视化工具-utils)
5. [测试用例 (tests)](#测试用例-tests)

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

#### 示例

```python
graph = Graph()

# 添加节点
node1 = graph.add_node("x")
node2 = graph.add_node("¬x")
node3 = graph.add_node("y")

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

### parse_cnf_string

解析CNF格式字符串。

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

## 归约算法 (reductions)

### 任务1: 3SAT到节点覆盖

#### reduce_3sat_to_vertex_cover

将3SAT公式归约为节点覆盖问题。

```python
from src.reductions import reduce_3sat_to_vertex_cover
from src.models import Formula3SAT

formula = Formula3SAT.from_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
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
2. 对于每对互为否定的文字，在对应的节点之间添加边
3. 计算覆盖大小k = 子句数 + 变量数

**正确性保证**: 公式可满足 ⟺ G有大小为k的节点覆盖

---

### 任务2: 3SAT到独立集

#### reduce_3sat_to_independent_set

将3SAT公式归约为独立集问题。

```python
from src.reductions import reduce_3sat_to_independent_set
from src.models import Formula3SAT

formula = Formula3SAT.from_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")
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
2. 对于每对互为否定的文字，在对应的节点之间添加边
3. 计算独立集大小n = 子句数

**正确性保证**: 公式可满足 ⟺ G有大小为n的独立集

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
from src.models import Graph

graph = Graph()
# ... 添加节点和边 ...

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

### create_comparison_plot

创建对比图，同时显示原图、顶点覆盖和独立集。

```python
from src.utils import create_comparison_plot

create_comparison_plot(graph, vertex_cover={0, 1}, 
                       independent_set={2, 3}, 
                       output_path="comparison.png")
```

---

## 测试用例 (tests)

### 预定义测试用例

```python
from tests.test_cases import (
    COURSE_EXAMPLE,           # 课件例子
    CUSTOM_EXAMPLE,           # 自定义5+子句例子
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
- 创建项目框架
- 实现数据结构（Literal, Clause, Formula3SAT, Graph）
- 实现CNF解析器
- 定义归约接口
- 实现可视化工具
- 编写测试用例和文档

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
from src.models import Formula3SAT, Graph
from src.parsers import parse_cnf_string
from src.reductions import reduce_3sat_to_vertex_cover, reduce_3sat_to_independent_set
from src.utils import draw_graph_with_vertex_cover, draw_graph_with_independent_set

# 2. 解析公式
formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")

# 3. 执行归约（需要人员B和C实现）
# graph_vc, k = reduce_3sat_to_vertex_cover(formula)
# graph_is, n = reduce_3sat_to_independent_set(formula)

# 4. 可视化结果
# draw_graph_with_vertex_cover(graph_vc, cover_set, "vertex_cover.png")
# draw_graph_with_independent_set(graph_is, ind_set, "independent_set.png")
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