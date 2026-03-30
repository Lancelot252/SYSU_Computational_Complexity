# 操作日志 - UTM模块实现

## 概述
本文档记录了成员C实现通用图灵机(UTM)模块的所有操作。

---

## 操作记录

### 2026-03-30

#### 1. 分析成员A的代码结构
- **文件**: `SYSU_Computational_Complexity-main/SYSU_Computational_Complexity-main/project1/src/modules/encoding.py`
- **发现**:
  - `encode_machine_file(path)` - 从JSON文件编码图灵机
  - `encode_machine_definition(machine_definition)` - 从字典编码图灵机
  - 返回 `EncodingResult` 对象，包含:
    - `encoding: str` - 二进制编码字符串
    - `state_ids: Dict[str, int]` - 状态名到ID的映射
    - `symbol_ids: Dict[str, int]` - 符号到ID的映射
    - `transitions: List[EncodedTransition]` - 编码后的转移列表
  - 编码格式: 每个转移用一进制编码，转移间用`11`分隔
  - 方向ID: `left=1, right=2, stay=3`

#### 2. 分析项目结构
- **已实现**: 编码模块 (`encoding.py`)
- **待实现**: 多带图灵机模块 (`multitape.py`), 通用图灵机模块 (`utm.py`)
- **CLI入口**: `app.py` 已预留 `utm` 命令

#### 3. 设计UTM模块架构
- 创建了详细的计划文档 `plans/utm_module_plan.md`
- 定义了UTM类的基本结构
- 规划了与多带图灵机模块的接口

#### 4. 扩展数据模型 (`core/models.py`)
- 添加了 `Tape` 类：模拟单条磁带，支持读写和移动操作
- 添加了 `MultiTapeTransition` 类：多带图灵机的转移规则
- 添加了 `UTMTransition` 类：UTM解析出的转移规则
- 添加了 `UTMState` 类：UTM运行状态

#### 5. 实现多带图灵机模块 (`modules/multitape.py`)
- 实现了 `MultiTapeTM` 类：
  - 支持多条磁带和多个磁头
  - 支持状态转移
  - 支持交互式和自动两种展示模式
  - 磁带显示格式：`_____ABC*ACB_____`（`*`表示磁头位置）
- 实现了 `run_multitape()` 便捷函数
- 实现了 `run_multitape_from_config()` 配置运行函数

#### 6. 实现通用图灵机模块 (`modules/utm.py`)
- 实现了 `UniversalTuringMachine` 类：
  - 三条磁带初始化：
    - Tape1: 存储 `M111w`
    - Tape2: 模拟被模拟图灵机的磁带
    - Tape3: 存储当前状态
  - 转移规则解析：从二进制编码解析转移规则
  - 主循环逻辑：搜索匹配转移、执行转移
  - 阶段说明打印：Step 2、Step 3、搜索转移、执行转移等
- 实现了 `run_utm()` 便捷函数
- 实现了 `run_utm_from_encoding()` 从编码结果运行函数

#### 7. 更新CLI入口 (`cli/app.py`)
- 添加了 `multitape` 命令：
  - `--config`: 配置文件路径
  - `--mode`: 运行模式（interactive/auto）
  - `--interval`: 时间间隔
- 添加了 `utm` 命令：
  - `--sample`: 测试样例
  - `--mode`: 运行模式
  - `--interval`: 时间间隔
  - `--details`: 输出详细信息
  - `--max-steps`: 最大步数限制
- 添加了默认多带图灵机演示配置

#### 8. 创建ADD图灵机测试用例 (`test/add_tm.json`)
- 实现了两数加法图灵机ADD的JSON定义
- 状态：q1-q7, halt
- 输入：["00", "000"]（代表2和3的一进制编码）

#### 9. 测试验证
- **编码模块测试**: 成功编码ADD图灵机，输出21个转移规则
- **UTM模块测试**: 成功运行6步后接受
- **多带图灵机测试**: 成功运行演示配置

---

## 文件变更记录

| 文件 | 操作 | 说明 |
|------|------|------|
| `plans/utm_module_plan.md` | 创建 | UTM模块设计计划 |
| `OPERATION_LOG.md` | 创建 | 本操作日志 |
| `src/core/models.py` | 修改 | 扩展数据模型（Tape、UTMTransition等） |
| `src/modules/multitape.py` | 修改 | 实现多带图灵机模块 |
| `src/modules/utm.py` | 修改 | 实现通用图灵机模块 |
| `src/cli/app.py` | 修改 | CLI入口更新（添加multitape和utm命令） |
| `test/add_tm.json` | 创建 | ADD图灵机测试用例 |

---

## 技术决策记录

### UTM磁带设计
根据作业要求，UTM需要三条磁带：
- **Tape1**: 存储 `M111w`，其中M是被模拟图灵机的编码，w是输入
- **Tape2**: 模拟被模拟图灵机的磁带（符号用一进制表示）
- **Tape3**: 存储当前状态（状态ID的一进制表示）

### 编码解析策略
- 从Tape1解析转移规则：用`11`分隔各转移，用`1`分隔转移内部各部分
- 使用状态ID和符号ID进行匹配
- 方向编码: 1=left, 2=right, 3=stay

### 展示模式
- **交互式**: 每步等待用户按Enter继续
- **自动**: 每步等待固定时间间隔

---

## 接口规范

### 与编码模块的接口
```python
from modules.encoding import encode_machine_file
result = encode_machine_file("test/sample_tm.json")
M = result.encoding  # 图灵机编码
state_ids = result.state_ids  # 状态映射
symbol_ids = result.symbol_ids  # 符号映射
```

### 与多带图灵机模块的接口
```python
from modules.multitape import MultiTapeTM, run_multitape

# 创建多带图灵机
tm = MultiTapeTM(num_tapes=2, initial_state="q1", accept_states={"halt"})
tm.set_tape(0, "0101")  # 设置磁带内容
tm.add_transition(...)  # 添加转移规则
tm.run(mode="interactive")  # 运行
```

### UTM运行接口
```python
from modules.utm import run_utm

# 运行UTM
result = run_utm(
    json_path="test/add_tm.json",
    mode="auto",
    interval=0.5,
    max_steps=10000,
    details=True
)
```

---

## 测试结果

### 编码模块测试
```
编码结果：21个转移规则
状态映射：q1=1, q2=2, q3=3, q4=4, q5=5, q6=6, q7=7, halt=8
符号映射：0=1, 1=2, 空符号=3
```

### UTM模块测试
```
运行结果：接受 (ACCEPTED)
总步数：6步
阶段：Step2 -> Step3 -> 搜索转移 -> 执行转移 -> Accept
```

### 多带图灵机测试
```
运行结果：接受 (ACCEPTED)
总步数：7步
```

---

## 待完成任务
- [x] 完成UTM核心逻辑实现
- [x] 完成多带图灵机模块实现
- [x] 更新CLI入口
- [x] 创建ADD测试用例
- [x] 整体测试
- [ ] 编写实验报告（UTM模块部分）
- [ ] 创建README文件