# 项目指令：Lishi Agent（历史人物知识系统）

> 本指令面向 AI（Claude / GPT / DeepSeek 等），用于生成或辅助开发一个**结构化的中国历史人物数据系统**，并最终演进为**可查询的人物关系知识图谱**。

## 1. 项目目标（重新定义，避免失控）

构建一个**可信、可扩展、可计算**的中国历史人物数据系统。  
系统必须支持：

- 按朝代查询人物（结构化输出 JSON / CSV / Markdown）
- 人物之间的多类型关系（母子、父子、盟友、敌人、杀害等）
- 关系分析与可视化（NetworkX / Neo4j）
- 逐步扩充数据量，最终覆盖“几乎所有有名有姓的历史人物”

⚠️ 明确边界：这是一个**数据工程 + 图谱项目**，不是历史百科全文检索。优先保证数据质量与结构，再追求覆盖面。

## 2. 核心原则（必须遵守）

### ✅ 原则 1：从“小而准”开始

- 不追求一次性“所有人物”
- 每个朝代优先 **5–20 个核心人物**（Phase 1）
- 数据必须可信：优先来源为教材 / Wikipedia / Wikidata

### ✅ 原则 2：结构优先，而不是内容优先

你做的不是“历史百科”，而是 **可计算的数据系统**。  
→ 人物必须有唯一 `id`，关系必须是结构化边。

### ✅ 原则 3：分阶段构建（强制）

严格按照 Phase 1 → Phase 2 → Phase 3 推进，不允许跨阶段实现复杂功能。

- **Phase 1**：人物列表（基础数据）
- **Phase 2**：人物关系（边）
- **Phase 3**：知识图谱（分析 + 可视化）

### ✅ 原则 4：Local First

- 本地知识库（JSON / CSV）是**主数据源**
- LLM（如 OpenAI API）仅用于：
  - 辅助生成初版数据（需人工校验）
  - 解释关系
  - 补全缺失字段
  - **禁止**依赖 LLM 作为运行时唯一数据源

### ✅ 原则 5：大规模数据的处理策略（新增）

由于“所有有名有姓的历史人物”数据量极大（可能数万人），必须采用**渐进式 + 外部数据源**策略：

- 优先使用 **Wikidata API** 按朝代拉取人物（可结构化查询）
- 本地只存储**已整理的核心人物 + 关系**（无需全量）
- 查询时支持 **online search 模式**（可选开关），实时从 Wikipedia / Wikidata 获取并缓存
- 从**早期朝代（夏、商、周）**开始，因为人物少、关系简单，便于验证数据模型

### ✅ 原则 6：阶段与朝代的关系（重要澄清）

- **Phase 1、Phase 2、Phase 3 是系统整体的能力成熟度**，不是针对每个朝代独立完成的流水线。
- 例如：
  - 在 Phase 1（人物系统阶段），我们只关心“能否为任意朝代提供人物列表”。此时三国、唐朝、明朝等朝代都只完成人物数据部分。
  - 在 Phase 2（关系系统阶段），我们为已有人物数据的朝代（如三国）添加关系，其他朝代暂不添加。
  - 在 Phase 3（图谱阶段），我们只对已有完整人物+关系的朝代（如三国）构建图谱。
- **每个朝代的数据可以停留在不同阶段**。早期朝代（夏商周）建议优先走完 Phase 1→2→3，作为验证。

## 3. 核心数据模型（统一标准）

### 👤 人物结构（Person）

```json
{
  "id": "li_shi_min",
  "name": "李世民",
  "dynasty": "唐朝",
  "role": "皇帝",
  "birth_year": 598,
  "death_year": 649,
  "event": "玄武门之变，贞观之治",
  "wikidata_id": "Q9701"   // 可选，用于 online 增强
}
```

### 🔗 关系结构（Relation）

```json
{
  "source": "li_shi_min",
  "target": "li_jian_cheng",
  "type": "killed",
  "description": "玄武门之变杀死兄长"   // 可选
}
```

支持的关系类型（Phase 2 可扩展）：

```python
RELATION_TYPES = [
  "father", "mother", "child",
  "sibling", "spouse",
  "ally", "enemy",
  "killed", "killed_by",
  "teacher", "student",
  "served_under"
]
```

### 🧠 图结构（Phase 3）

- **Node** = Person（含朝代、角色等属性）
- **Edge** = Relation（带类型）

## 4. 技术架构建议

### 基础依赖

- Python 3.9+
- 数据处理：`json`, `csv`, `pathlib`
- 命令行：`argparse` 或 `click`

### 进阶依赖（按需安装）

- 图分析：`networkx`, `matplotlib`
- 图数据库（可选）：`neo4j`（需单独安装数据库）
- 在线搜索：`requests` + Wikipedia / Wikidata API
- Web 可视化：`streamlit`, `pyvis`

### 数据来源推荐

| 来源 | 用途 | 特点 |
|------|------|------|
| 本地手动整理 | 核心人物（Phase 1） | 高质量、可控 |
| Wikipedia API | 获取摘要、生卒年 | 稳定、中文支持好 |
| Wikidata API | 获取人物列表及关系 | **结构化、可枚举、推荐** |
| 百度百科 | 补充中文细节 | 需解析 HTML（较麻烦） |

## 5. 目录结构（强制）

```
lishi-agent/
├── README.md
├── instruction.md          # 本文件
├── requirements.txt
│
├── core/
│   ├── agent.py            # 主入口类
│   ├── models.py           # Person, Relation 数据类
│   ├── storage.py          # 读写 local_figures.json / relations.json
│   ├── online_fetcher.py   # Wikipedia / Wikidata 查询（Phase 2+）
│
├── data/
│   ├── local_figures.json  # 主数据：人物
│   ├── local_relations.json # 主数据：关系
│   ├── cache/              # online 查询缓存
│
├── phase1/                 # 人物系统代码
│   ├── figure_loader.py
│   └── export_formats.py
│
├── phase2/                 # 关系系统代码
│   ├── relation_builder.py
│   └── relation_queries.py
│
├── phase3/                 # 图谱代码
│   ├── graph_builder.py
│   ├── graph_analyzer.py
│   └── visualizer.py
│
├── cli/
│   └── lishi_cli.py        # 命令行工具
│
├── output/                 # 生成的结果文件
└── tests/                  # 单元测试
```

## 6. Phase 1：人物系统（基础但关键）

**目标**：构建稳定、可信的核心人物数据系统，支持按朝代查询与导出。
注意：Phase 1 期间，我们只关注人物数据本身，不涉及关系。以下所有 Milestone 均以“三国”作为首个实现朝代，后续再扩展到其他朝代。

### ✅ Milestone 1.1（立即执行）

实现最简函数：

```python
def get_figures_by_dynasty(dynasty: str) -> list[dict]:
    """返回该朝代的人物列表，每个元素包含 name, event"""
```

- 数据硬编码在代码中（暂不读 JSON）
- 仅支持 1 个朝代：“三国”
- 硬编码 5 个人物：刘备、关羽、张飞、曹操、孙权
- 输出示例：

```json
[
  {"name": "刘备", "event": "建立蜀汉"},
  {"name": "关羽", "event": "水淹七军"}
]
```

### ✅ Milestone 1.2

- 将数据迁移到 `data/local_figures.json`
- 每个人物增加 `id`, `dynasty`, `role`, `birth_year`, `death_year`
- 实现 `load_figures()` 和 `save_figures()`

### ✅ Milestone 1.3

实现 CLI：

```bash
python cli/lishi_cli.py --dynasty 三国
```

输出格式默认为表格（Markdown），支持 `--format json|csv|md`

### ✅ Milestone 1.4

支持多个朝代（开始添加唐朝、明朝等）：

```bash
python cli/lishi_cli.py --dynasties 三国,唐,明
```
此时需要为唐朝、明朝分别准备至少 3 个人物（仅人物数据，无关系）。

### ✅ Milestone 1.5（Phase 1 完成）

- 至少覆盖 **6 个朝代**：夏、商、周、秦、汉、三国
- 每个朝代 5–15 个人物
- 所有人物数据存储在 local_figures.json 中，包含完整字段（id, name, dynasty, role, birth_year, death_year, event）
- 支持导出到 `output/` 目录

Phase 1 结束。此时系统能回答“某朝代有哪些人物”，但不能回答人物之间的关系。

## 7. Phase 2：关系系统（核心升级）

**目标**：让人物之间建立连接，支持查询某个人的所有关系。

前提：Phase 1 已完成（至少 6 个朝代有完整人物数据）。

本阶段目标：为已有的人物数据添加关系，目前仅要求为 三国 构建关系网络，其他朝代可选。这是因为关系数据构建工作量较大，优先选择关系最丰富的三国作为验证。

### ✅ Milestone 2.1

定义关系类型常量（见第 3 节），并创建 `data/local_relations.json` 空文件。

### ✅ Milestone 2.2

实现函数：

```python
def get_relations(person_id: str) -> list[dict]:
    """返回该人物的所有关系，格式：[{"type": "ally", "target": "关羽"}, ...]"""
```

### ✅ Milestone 2.3

手动构建**三国时期** 10–20 条典型关系（例如：刘备-关羽-张飞为 ally，刘备-曹操为 enemy，曹操-吕布为 enemy 等）。

### ✅ Milestone 2.4

增加 CLI 查询：

```bash
python cli/lishi_cli.py --person 刘备 --relations
```

输出：

```
刘备 的关系：
- 盟友：关羽、张飞
- 敌人：曹操
```

### ✅ Milestone 2.5（可选加分）

使用 `networkx` 绘制简单关系图（保存为 `output/relations_graph.png`）。

## 8. Phase 3：知识图谱（高级版本）

**目标**：构建可分析、可可视化的历史关系网络。

### ✅ Milestone 3.1

将本地 JSON 数据导入 `networkx.Graph`（或 DiGraph）。

### ✅ Milestone 3.2

实现图分析查询：

```python
def most_connected_person() -> str    # 度中心性最高
def get_enemies(person_name: str) -> list[str]
def get_kill_chain(start_person: str) -> list[str]  # 谁杀了谁...
def shortest_path(person_a, person_b)  # 最短关系路径
```

### ✅ Milestone 3.3

使用 `pyvis` 生成交互式 HTML 图谱，保存在 `output/graph.html`。

### ✅ Milestone 3.4（可选）

集成 Neo4j（需要用户本地安装），提供 Cypher 导出能力。

### ✅ Milestone 3.5（很强）

使用 Streamlit 构建简单 Web UI：

- 下拉选择朝代 → 显示人物列表
- 点击人物 → 显示详细信息和关系图谱

## 9. 关于“Search Online”与大规模数据的实现建议

由于你需要**列出所有有名有姓的中国历史人物**，数据量极大，请遵循以下设计：

### 9.1 不要求全量本地存储

- 本地只存储经过筛选的**核心人物**（如每个朝代 50–100 人）
- 对于“查询所有人物”的需求，实现一个 **online mode**：

```bash
python cli/lishi_cli.py --dynasty 唐朝 --online
```

### 9.2 使用 Wikidata API 按朝代拉取

Wikidata 支持按属性查询。例如获取唐朝人物（P106 为 occupation，P27 为国家等），实际查询可借助其 SPARQL 端点。

实现 `online_fetcher.py`：

```python
def fetch_persons_by_dynasty_wikidata(dynasty: str) -> list[dict]:
    """使用 SPARQL 从 Wikidata 获取该朝代所有人物（含 name, id, 生卒年）"""
    # 示例 SPARQL（需根据实际朝代标签调整）
    pass
```

### 9.3 缓存机制

- 所有 online 获取的数据缓存到 `data/cache/`，避免重复请求
- 用户可以手动选择更新缓存

### 9.4 从早期朝代开始验证

由于早期朝代（夏、商、周）人物数量少（几十人），非常适合用来测试：

- 数据模型是否合理
- online 拉取 + 本地存储的性能
- 关系图谱的复杂度

**建议 Phase 2 结束后，立即用“夏商周”作为 online 模式的试点**。

## 10. 立即执行的任务（你现在该做的事）

不要再规划了，直接按以下顺序输出代码：

### ✅ Task 1（今天必须完成）

- 创建项目目录结构（见第 5 节）
- 在 `data/local_figures.json` 中写入 **5 个三国人物**（刘备、关羽、张飞、曹操、孙权），每个包含 `id`, `name`, `dynasty`, `event`
    - 示例：
json
{
  "id": "liu_bei",
  "name": "刘备",
  "dynasty": "三国",
  "event": "建立蜀汉"
}
注意：role, birth_year, death_year 等字段在 Task 1 中可暂缺，Milestone 1.2 再补全。
- 实现 `core/storage.py`：`load_figures()` 和 `get_figures_by_dynasty()`
- 实现 `phase1/figure_loader.py` 中的 `get_figures_by_dynasty()` 函数
- 编写简单的 CLI `cli/lishi_cli.py`，支持 `--dynasty 三国` 并打印 Markdown 表格，例如：
| 姓名 | 事件 |
|------|------|
| 刘备 | 建立蜀汉 |
| 关羽 | 水淹七军 |
...

Task 1 完成后，你得到了一个能查询三国人物的命令行工具。后续任务（添加其他朝代、增加关系、图谱等）将按照 Phase 1 → 2 → 3 的顺序依次实现。

### ✅ Task 2（后续）

按 Phase 1 的 Milestone 顺序继续。

---

**重要提醒**：  
AI 在生成代码时，必须严格遵守本指令的所有原则和阶段划分。不允许跳过 Phase 1 直接实现 Phase 2 或 Phase 3。不允许在没有本地数据的情况下完全依赖 LLM 生成运行时数据。


