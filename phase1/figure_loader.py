"""Figure loader module for Phase 1 - loads and queries figures by dynasty."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.storage import get_figures_by_dynasty, load_figures


def get_figures_by_dynasty(dynasty: str) -> list[dict]:
    """Return figures for a given dynasty.
    
    Args:
        dynasty: The dynasty name (e.g., "三国", "唐朝").
    
    Returns:
        List of figure dictionaries with name and event.
    """
    figures = get_figures_by_dynasty(dynasty)
    return [{"name": f.get("name"), "event": f.get("event")} for f in figures]


def get_all_figures() -> list[dict]:
    """Return all figures.
    
    Returns:
        List of all figure dictionaries.
    """
    return load_figures()


if __name__ == "__main__":
    # Test the module
    figures = get_figures_by_dynasty("三国")
    print(f"Found {len(figures)} figures from 三国:")
    for f in figures:
        print(f"  - {f['name']}: {f['event']}")