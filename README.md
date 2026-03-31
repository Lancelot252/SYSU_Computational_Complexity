# SYSU_Computational_Complexity

本项目为中山大学计算机学院2026年计算复杂性专业选修课的小组作业存储仓库。

## 项目结构

```
.
├── project1/               # 第一次编程作业
│   ├── src/                # 源代码
│   │   ├── main.py         # 程序入口
│   │   ├── cli/            # 命令行接口
│   │   ├── core/           # 核心模块
│   │   └── modules/        # 功能模块
│   ├── test/               # 测试用例
│   ├── docs/               # 实验报告
│   └── README.md           # 项目说明
├── 实验报告模板/            # LaTeX报告模板
├── 要求文档/                # 作业要求
└── README.md               # 本文件
```

## 快速开始

```bash
cd project1/src
python main.py --help
```

## 功能模块

- **图灵机编码模块**：将JSON定义的图灵机转换为二进制编码
- **多带图灵机模块**：模拟多带图灵机运行
- **通用图灵机模块**：实现通用图灵机模拟器

## 详细说明

请参阅 [project1/README.md](project1/README.md)