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
6. **Chronological Order**: Figures stored by birth_year (earliest to latest)

## Current Status: Phase 1 Complete

### Supported Dynasties (18)

| Dynasty | Period | Figures |
|---------|--------|---------|
| 夏 (Xia) | ~2070-1600 BCE | 大禹、启、桀 |
| 商 (Shang) | ~1600-1046 BCE | 汤、盘庚 |
| 周 (Zhou) | 1046-256 BCE | 周文王、周武王 |
| 春秋 (Spring & Autumn) | 770-476 BCE | 孔子、孙武、范蠡 |
| 战国 (Warring States) | 475-221 BCE | 白起、廉颇、蔺相如 |
| 秦 (Qin) | 221-206 BCE | 李斯、秦始皇 |
| 汉 (Han) | 206 BCE-220 AD | 刘邦、张骞、司马迁、汉武帝 |
| 东汉 (Eastern Han) | 25-220 AD | 刘秀 |
| 三国 (Three Kingdoms) | 220-280 AD | 曹操、刘备、关羽、张飞、孙权、曹丕 |
| 晋朝 (Jin) | 265-420 AD | 司马炎 |
| 南北朝 (Southern & Northern) | 420-589 AD | 苻坚、萧道成、文帝、陶弘景 |
| 隋朝 (Sui) | 581-618 AD | 杨坚 |
| 唐朝 (Tang) | 618-907 AD | 李渊、李世民、武则天、李白 |
| 五代十国 (Five Dynasties) | 907-960 AD | 王覆 |
| 宋朝 (Song) | 960-1279 AD | 赵匡胤、苏轼、岳飞、文天祥 |
| 元朝 (Yuan) | 1271-1368 AD | 忽必烈、马可波罗 |
| 明朝 (Ming) | 1368-1644 AD | 朱元璋、朱棣、王阳明 |
| 清朝 (Qing) | 1644-1912 AD | 努尔哈赤、康熙帝、乾隆帝、曹雪芹、慈禧太后 |

**Total: 52 figures** (sorted chronologically by birth_year)

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
│   ├── local_figures.json   # Figure data (52 figures, 18 dynasties)
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

Data is sorted by birth_year (earliest to latest).

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
- [x] Support 18 dynasties
- [x] Chronological sorting (by birth_year)

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

MIT