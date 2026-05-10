# Lab1: 通用图灵机 (UTM)

本项目为中山大学计算复杂性课程第一次编程作业，实现多带图灵机的编码和通用图灵机模拟器。

## 项目结构

```
lab1/
├── src/                # 源代码
│   ├── main.py         # 程序入口
│   ├── cli/            # 命令行接口
│   ├── core/           # 核心模块
│   └── modules/        # 功能模块
│       ├── encoding.py     # 图灵机编码
│       ├── multitape.py    # 多带图灵机
│       └── utm.py          # 通用图灵机
├── test/               # 测试用例
├── docs/               # 文档
└── 实验报告/            # LaTeX实验报告
```

## 快速开始

```bash
cd src
python main.py --help
```

## 功能模块

### 图灵机编码模块
将JSON定义的图灵机转换为二进制编码。

### 多带图灵机模块
模拟多带图灵机运行。

### 通用图灵机模块
实现通用图灵机模拟器。

## 使用方法

```bash
# 运行图灵机编码
python main.py encode --input test/sample_tm.json

# 运行多带图灵机
python main.py run --input test/sample_tm.json

# 运行通用图灵机
python main.py utm --input test/sample_tm.json
```

