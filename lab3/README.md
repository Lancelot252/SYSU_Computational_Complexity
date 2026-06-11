# lab3 - 近似算法实现

计算复杂性课程第三次编程作业：MAX-3SAT 随机近似算法与 METRIC-TSP 2-近似算法。

## 项目概述

本项目实现了两个近似算法：

- **任务1**: MAX-3SAT 随机近似算法（Las Vegas 风格）—— 不断随机生成变量赋值，直到找到满足至少 ⌈7/8·m⌉ 个子句的赋值
- **任务2**: METRIC-TSP 2-近似算法 —— 基于最小生成树与 DFS 遍历的近似算法

## 目录结构

```
lab3/
├── src/                           # 源代码目录
│   ├── __init__.py
│   ├── main.py                    # 主程序入口（CLI）
│   ├── max3sat/                   # MAX-3SAT 模块
│   │   ├── __init__.py
│   │   ├── models.py              # 数据结构（Literal, Clause, Formula）
│   │   ├── parser.py              # 公式解析与随机生成
│   │   └── solver.py              # 随机近似算法求解器
│   ├── metric_tsp/                # METRIC-TSP 模块
│   │   ├── __init__.py
│   │   ├── models.py              # 数据结构（City, Edge, WeightedGraph）
│   │   ├── graph.py               # 带权完全图构造
│   │   ├── mst.py                 # Kruskal 最小生成树
│   │   ├── dfs.py                 # DFS 遍历
│   │   └── solver.py              # 2-近似算法 + 暴力最优解
│   └── utils/
│       ├── __init__.py
│       └── timer.py               # 计时工具
├── test/                          # 测试用例目录
│   ├── max3sat/
│   │   ├── fixed.txt              # 固定测试用例
│   │   └── random_config.txt      # 随机生成配置
│   └── metric_tsp/
│       └── sample.txt             # 课件示例
├── output/                        # 输出目录
│   ├── max3sat/
│   └── metric_tsp/
├── docs/                          # 实验报告
│   └── report.pdf
├── requirements.txt               # 依赖说明
└── README.md                      # 本文件
```

## 安装依赖

本项目仅使用 Python 标准库，无需安装额外依赖：

```bash
# 如需运行单元测试（可选）
pip install pytest
```

## 运行 MAX-3SAT 测试

```bash
# 运行固定测试用例
python src/main.py --task 1 --input test/max3sat/fixed.txt

# 运行随机生成测试用例
python src/main.py --task 1 --input test/max3sat/random_config.txt --mode random
```

## 运行 METRIC-TSP 测试

```bash
# 运行课件示例
python src/main.py --task 2 --input test/metric_tsp/sample.txt
```

## 运行所有测试

```bash
python src/main.py --all
```
