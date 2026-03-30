# Project 1

## 项目结构

```text
src/
  main.py
  cli/
  core/
  modules/
test/
  *.json
docs/
README.md
```

- `src/main.py`：统一命令行入口。
- `src/cli/`：命令行参数解析、交互式样例选择与输出控制。
- `src/core/`：共享基础能力，包括 JSON 读取、样例发现、错误处理和统一数据模型。
- `src/modules/`：各功能模块实现，目前只完成图灵机编码模块，并为多带图灵机、通用图灵机预留扩展位。
- `test/`：共享测试样例库，只存放 JSON 文件。同一份样例将被编码模块、多带图灵机模块和通用图灵机模块复用。

## 当前已实现功能

当前程序已实现：

- 共享测试样例自动发现
- 图灵机编码模块
- 统一 CLI 入口
- `multitape` 和 `utm` 的命令预留位
- 默认启动后循环显示主菜单，直到手动选择退出

当前尚未实现：

- 多带图灵机模拟
- 通用图灵机模拟

## 共享样例格式

测试样例采用统一 JSON 结构：

```json
{
  "<state-name>": {
    "<read-symbol>": {
      "write": "<write-symbol>",
      "move": "<right|left|stay>",
      "nextState": "<next-state-name>"
    }
  },
  "input": ["<input-string-1>", "<input-string-2>"]
}
```

说明：

- 除 `input` 外，其余顶层键均视为状态名。
- `input` 字段用于保存共享测试输入，编码模块会自动忽略该字段。
- 后续多带图灵机和通用图灵机模块将直接复用同一份样例定义与 `input` 数据。

## 编码规则

图灵机编码模块采用如下规则：

- 状态名若形如 `qN`，则状态编号为 `N`；其他状态名按字典序分配未使用的正整数编号。
- 符号编号固定为：`0 -> 1`，`1 -> 2`，空白符 `" " -> 3`；其他符号按字典序从 `4` 开始编号。
- 方向编号固定为：`left -> 1`，`right -> 2`，`stay -> 3`。
- 单条转移 `(q_i, X_j) -> (q_k, X_l, D_m)` 编码为 `0^i 1 0^j 1 0^k 1 0^l 1 0^m`。
- 所有转移在编号后按 `(当前状态, 读取符号, 下一状态, 写入符号, 移动方向)` 排序，并使用 `11` 连接成整台图灵机的编码结果。

## 命令行使用方法

列出全部共享样例：

```bash
python src/main.py list
```

直接启动并进入循环菜单：

```bash
python src/main.py
```

对指定样例执行编码：

```bash
python src/main.py encode --sample sample_tm.json
```

不指定样例时进入交互式选择：

```bash
python src/main.py encode
```

输出编码明细：

```bash
python src/main.py encode --sample sample_tm.json --details
```

预留命令：

```bash
python src/main.py multitape
python src/main.py utm
```