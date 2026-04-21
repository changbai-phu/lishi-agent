"""Storage module for loading and saving figures data."""

import json
from pathlib import Path
from typing import List, Dict, Optional

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOCAL_FIGURES_FILE = DATA_DIR / "local_figures.json"
LOCAL_RELATIONS_FILE = DATA_DIR / "local_relations.json"


def load_figures() -> List[Dict]:
    """Load all figures from local_figures.json.
    
    Returns:
        List of figure dictionaries.
    """
    if not LOCAL_FIGURES_FILE.exists():
        return []
    
    with open(LOCAL_FIGURES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_figures(figures: List[Dict]) -> None:
    """Save figures to local_figures.json.
    
    Args:
        figures: List of figure dictionaries to save.
    """
    with open(LOCAL_FIGURES_FILE, "w", encoding="utf-8") as f:
        json.dump(figures, f, ensure_ascii=False, indent=2)


def get_figures_by_dynasty(dynasty: str) -> List[Dict]:
    """Get figures filtered by dynasty.
    
    Args:
        dynasty: The dynasty name to filter by.
    
    Returns:
        List of figure dictionaries matching the dynasty.
    """
    figures = load_figures()
    return [f for f in figures if f.get("dynasty") == dynasty]


def load_relations() -> List[Dict]:
    """Load all relations from local_relations.json.
    
    Returns:
        List of relation dictionaries.
    """
    if not LOCAL_RELATIONS_FILE.exists():
        return []
    
    with open(LOCAL_RELATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_relations(person_id: str) -> List[Dict]:
    """Get all relations for a person (as source or target).
    
    Args:
        person_id: The figure ID to get relations for.
    
    Returns:
        List of relation dictionaries where the person is source or target.
    """
    relations = load_relations()
    return [r for r in relations if r.get("source") == person_id or r.get("target") == person_id]


def get_person_by_id(person_id: str) -> Optional[Dict]:
    """Get a person by their ID or Chinese name.
    
    Args:
        person_id: The figure ID (e.g., "liu_bei") or Chinese name (e.g., "刘备") to search for.
    
    Returns:
        Figure dictionary if found, None otherwise.
    """
    figures = load_figures()
    for f in figures:
        if f.get("id") == person_id or f.get("name") == person_id:
            return f
    return None
