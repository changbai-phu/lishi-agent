# Lishi Agent (历史人物知识系统)

AI Agent that organizes famous historical figures and their key events from Chinese dynasties, evolving into a queryable knowledge graph.

## Project Overview

Lishi Agent is a structured Chinese historical figures data system that supports:
- Querying figures by dynasty (JSON / CSV / Markdown output)
- Multi-type relationships between figures (family, ally, enemy, etc.)
- Relationship analysis and visualization (NetworkX / Neo4j)
- Gradual expansion to cover "almost all famous historical figures"

## Core Principles

1. **Start Small & Accurate**: Begin with 5-20 core figures per dynasty
2. **Structure First**: Not an encyclopedia, but a computable data system
3. **Phase-based Development**: Phase 1 → Phase 2 → Phase 3
4. **Local First**: Local JSON/CSV as primary data source
5. **Progressive Data**: Use Wikidata API for large-scale data

## Current Status: Phase 1 Complete

### Supported Dynasties (10)

| Dynasty | Figures |
|---------|---------|
| 夏 (Xia) | 大禹、启、桀 |
| 商 (Shang) | 汤、盘庚 |
| 周 (Zhou) | 周文王、周武王 |
| 春秋 (Spring & Autumn) | 孔子、孙武、范蠡 |
| 战国 (Warring States) | 白起、廉颇、蔺相如 |
| 秦 (Qin) | 秦始皇、李斯 |
| 汉 (Han) | 刘邦、汉武帝、张骞、司马迁 |
| 三国 (Three Kingdoms) | 刘备、关羽、张飞、曹操、孙权 |
| 唐朝 (Tang) | 李世民、武则天、李白 |
| 明朝 (Ming) | 朱元璋、朱棣、王阳明 |

**Total: 31 figures**

## Installation

```bash
# No external dependencies required for Phase 1
# Optional: for future phases
pip install networkx matplotlib pyvis streamlit
```

## Usage

### Query by Dynasty
```bash
# Single dynasty
python cli/lishi_cli.py --dynasty 三国

# Multiple dynasties
python cli/lishi_cli.py --dynasties 三国,唐朝,明
```

### Output Formats
```bash
# Markdown table (default)
python cli/lishi_cli.py --dynasty 三国

# JSON
python cli/lishi_cli.py --dynasty 三国 --format json

# CSV
python cli/lishi_cli.py --dynasty 三国 --format csv
```

### Export to File
```bash
python cli/lishi_cli.py --dynasties 夏,商,周 --export ancient_figures.md
```

## Project Structure

```
lishi-agent/
├── README.md
├── instructions.md          # Project instructions
├── requirements.txt         # Dependencies
│
├── core/
│   └── storage.py           # Data loading/saving (load_figures, get_figures_by_dynasty)
│
├── phase1/                  # Phase 1: Figure system
│   └── figure_loader.py
│
├── phase2/                  # Phase 2: Relation system (planned)
│
├── phase3/                  # Phase 3: Knowledge graph (planned)
│
├── cli/
│   └── lishi_cli.py         # Command line interface
│
├── data/
│   ├── local_figures.json   # Figure data
│   ├── local_relations.json # Relation data (Phase 2)
│   └── cache/               # Online query cache
│
├── output/                  # Exported files
└── tests/                   # Unit tests
```

## Data Model

### Figure (Person)
```json
{
  "id": "liu_bei",
  "name": "刘备",
  "dynasty": "三国",
  "role": "皇帝",
  "birth_year": 161,
  "death_year": 223,
  "event": "建立蜀汉"
}
```

### Relation (Phase 2+)
```json
{
  "source": "liu_bei",
  "target": "guan_yu",
  "type": "ally",
  "description": "桃园三结义"
}
```

## Roadmap

### Phase 1: Figure System ✅ Complete
- [x] Query figures by dynasty
- [x] Multiple output formats (JSON, CSV, Markdown)
- [x] Export to file
- [x] Support 10 dynasties

### Phase 2: Relation System (In Progress)
- [ ] Define relation types
- [ ] Build Three Kingdoms relations
- [ ] Query person relations via CLI
- [ ] Visualize relationship graph

### Phase 3: Knowledge Graph
- [ ] Import to NetworkX
- [ ] Graph analysis (centrality, paths)
- [ ] Interactive HTML visualization
- [ ] Streamlit web UI

## License

