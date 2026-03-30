# 计算复杂性第一次编程作业 - 图灵机模拟器

## 项目概述

本项目实现了图灵机编码、多带图灵机模拟器和通用图灵机模拟器，使用Python语言编写。

## 项目结构

```
project1/
├── src/                    # 源代码目录
│   ├── main.py             # 程序入口
│   ├── cli/                # 命令行接口
│   │   ├── __init__.py
│   │   └── app.py          # CLI应用
│   ├── core/               # 核心模块
│   │   ├── __init__.py
│   │   ├── models.py       # 数据模型定义
│   │   ├── errors.py       # 错误定义
│   │   ├── json_utils.py   # JSON工具
│   │   └── samples.py      # 样例管理
│   └── modules/            # 功能模块
│   │       ├── __init__.py
│   │       ├── encoding.py # 图灵机编码模块（成员A）
│   │       ├── multitape.py# 多带图灵机模块（成员B/C）
│   │       └── utm.py      # 通用图灵机模块（成员C）
├── test/                   # 测试用例目录
│   ├── sample_tm.json      # 示例图灵机
│   └── add_tm.json         # ADD加法图灵机
├── docs/                   # 实验报告目录
│   └── report.pdf          # 实验报告
└── README.md               # 本文件
```

## 功能模块

### 1. 图灵机编码模块

将定义图灵机的JSON文件转换为二进制编码。

**编码规则**：
- 每个转移规则编码格式：`状态ID(一进制) 1 符号ID(一进制) 1 下一状态ID(一进制) 1 写入符号ID(一进制) 1 方向ID(一进制)`
- 转移之间用 `11` 分隔
- 方向ID：`left=1, right=2, stay=3`
- 一进制编码：数字n用n个0表示

### 2. 多带图灵机模块

模拟多带图灵机的运行过程。

**功能**：
- 支持多条磁带和多个磁头
- 支持状态转移
- 支持交互式和自动两种展示模式
- 磁带显示格式：`_____ABC*ACB_____`（`*`表示磁头位置）

### 3. 通用图灵机模块

基于多带图灵机实现通用图灵机模拟器。

**三条磁带**：
- Tape1：存储 `M111w`（被模拟图灵机的编码和输入）
- Tape2：模拟被模拟图灵机的磁带
- Tape3：存储当前状态

**运行阶段**：
- Step 2：分析M确定符号表示长度
- Step 3：初始化磁带
- 搜索匹配转移
- 执行转移
- 接受/拒绝

## 使用方法

### 运行程序

```bash
cd project1/src
python main.py
```

### 命令列表

#### 1. 列出测试样例

```bash
python main.py list
```

#### 2. 图灵机编码

```bash
# 基本编码
python main.py encode --sample add_tm.json

# 详细输出
python main.py encode --sample add_tm.json --details
```

#### 3. 运行多带图灵机

```bash
# 交互式模式
python main.py multitape --mode interactive

# 自动模式
python main.py multitape --mode auto --interval 0.5

# 使用配置文件
python main.py multitape --config config.json --mode auto
```

#### 4. 运行通用图灵机

```bash
# 交互式模式
python main.py utm --sample add_tm.json --mode interactive

# 自动模式
python main.py utm --sample add_tm.json --mode auto --interval 0.1

# 详细输出
python main.py utm --sample add_tm.json --details --mode auto

# 设置最大步数
python main.py utm --sample add_tm.json --max-steps 1000
```

### 交互式菜单

不带参数运行程序会进入交互式菜单：

```bash
python main.py
```

菜单选项：
1. 列出 test 目录下的共享 JSON 样例
2. 对选定样例执行图灵机编码
3. 运行多带图灵机模拟器
4. 运行通用图灵机模拟器
5. 退出程序

## 测试用例

### ADD图灵机 (`test/add_tm.json`)

两数加法图灵机，计算两个一进制数的和。

**输入格式**：
```json
{
  "input": ["00", "000"]  // 代表 2 + 3
}
```

**预期结果**：磁带上留下 `00000`（代表5）

### 示例图灵机 (`test/sample_tm.json`)

一个简单的图灵机示例。

## JSON文件格式

```json
{
  "q1": {
    "0": {
      "write": "1",
      "move": "right",
      "nextState": "q2"
    },
    " ": {
      "write": " ",
      "move": "left",
      "nextState": "halt"
    }
  },
  "halt": {},
  "input": ["00", "000"]
}
```

**字段说明**：
- 状态名：如 `q1`, `q2`, `halt`
- 读取符号：触发转移的符号
- `write`：写入的符号
- `move`：移动方向（`left`, `right`, `stay`）
- `nextState`：下一状态
- `input`：输入字符串列表

## 运行示例

### 编码ADD图灵机

```
$ python main.py encode --sample add_tm.json --details

编码结果：
{
  "encoding": "010101010011010010100100...",
  "state_ids": {"q1": 1, "q2": 2, ..., "halt": 8},
  "symbol_ids": {"0": 1, "1": 2, " ": 3},
  "transitions": [21个转移规则]
}
```

### 运行UTM

```
$ python main.py utm --sample add_tm.json --mode auto

============================================================
UTM 初始化
============================================================
当前阶段说明：Step 2: The UTM examines M...

============================================================
初始状态
============================================================
Tape1 (M111w): _____{编码}11100 000_____
Tape2 (模拟磁带): _____00 000_____
Tape3 (状态): _____0_____

...

============================================================
运行结束
============================================================
结果：接受 (ACCEPTED)
总步数：6
```

## 依赖

- Python 3.8+
- 无需额外依赖库

## 分工说明

| 成员 | 主要职责 |
|------|----------|
| 成员A | 图灵机编码模块 + 测试用例构造 |
| 成员B | 多带图灵机模块 + 运行展示 |
| 成员C | 通用图灵机模块 + 整体集成 |

## 作者

- 成员A：编码模块
- 成员B：多带图灵机模块
- 成员C：UTM模块、整体集成

## 许可证

本项目仅用于教学目的。