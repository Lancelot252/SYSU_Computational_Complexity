# Lab2: NP完全性归约

本项目为中山大学计算复杂性课程第二次编程作业，实现3SAT到节点覆盖(Vertex Cover)和独立集(Independent Set)的归约算法。

## 项目结构

```
lab2/
├── src/                # 源代码
│   ├── models/         # 数据模型
│   │   ├── formula.py  # CNF公式模型
│   │   └── graph.py    # 图结构模型
│   ├── parsers/        # 解析器
│   │   └── cnf_parser.py   # CNF解析器
│   ├── reductions/     # 归约算法
│   │   ├── vertex_cover.py     # 3SAT到Vertex Cover归约
│   │   └── independent_set.py  # 3SAT到Independent Set归约
│   └── utils/          # 工具模块
│       └── visualization.py    # 可视化工具
├── tests/              # 测试用例
└── docs/               # 文档
```

## 快速开始

```bash
pip install networkx matplotlib
python -m pytest tests/
```

## 功能模块

本项目实现了以下NP完全性归约：
- **任务1**: 3SAT → 节点覆盖 (Vertex Cover)
- **任务2**: 3SAT → 独立集 (Independent Set)

通过这些归约，我们证明了节点覆盖问题和独立集问题都是NP完全的。

## 使用方法

```python
from src.parsers import parse_cnf_string
from src.reductions import reduce_3sat_to_vertex_cover, reduce_3sat_to_independent_set

formula = parse_cnf_string("(x ∨ y ∨ ¬z) ∧ (¬x ∨ ¬y ∨ z)")

# 任务1: 3SAT → 节点覆盖
graph, k = reduce_3sat_to_vertex_cover(formula)

# 任务2: 3SAT → 独立集
graph, n = reduce_3sat_to_independent_set(formula)
```

## 作者
- 刘昊
