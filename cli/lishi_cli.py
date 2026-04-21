#!/usr/bin/env python3
"""Lishi Agent CLI - Command line interface for querying historical figures."""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.storage import get_figures_by_dynasty, load_figures, get_relations, get_person_by_id


def format_markdown_table(figures: list[dict]) -> str:
    """Format figures as a Markdown table.
    
    Args:
        figures: List of figure dictionaries.
    
    Returns:
        Markdown formatted table string.
    """
    if not figures:
        return "No figures found."
    
    # Build table header
    headers = list(figures[0].keys())
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    
    # Build table rows
    rows = []
    for f in figures:
        row = "| " + " | ".join(str(f.get(h, "")) for h in headers) + " |"
        rows.append(row)
    
    return "\n".join([header_line, separator] + rows)


def format_json(figures: list[dict]) -> str:
    """Format figures as JSON.
    
    Args:
        figures: List of figure dictionaries.
    
    Returns:
        JSON formatted string.
    """
    return json.dumps(figures, ensure_ascii=False, indent=2)


def format_csv(figures: list[dict]) -> str:
    """Format figures as CSV.
    
    Args:
        figures: List of figure dictionaries.
    
    Returns:
        CSV formatted string.
    """
    if not figures:
        return ""
    
    headers = list(figures[0].keys())
    header_line = ",".join(headers)
    
    rows = []
    for f in figures:
        row = ",".join(str(f.get(h, "")) for h in headers)
        rows.append(row)
    
    return "\n".join([header_line] + rows)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Lishi Agent - Query Chinese historical figures"
    )
    parser.add_argument(
        "--dynasty",
        type=str,
        help="Filter figures by dynasty (e.g., 三国, 唐朝)"
    )
    parser.add_argument(
        "--dynasties",
        type=str,
        help="Filter figures by multiple dynasties, comma-separated (e.g., 三国,唐朝,明)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["md", "json", "csv"],
        default="md",
        help="Output format (default: md)"
    )
    parser.add_argument(
        "--export",
        type=str,
        help="Export to output/ directory with specified filename"
    )
    parser.add_argument(
        "--person",
        type=str,
        help="Query person by ID to show their relations (e.g., liu_bei)"
    )
    parser.add_argument(
        "--relations",
        action="store_true",
        help="Show relations for the person specified with --person"
    )
    
    args = parser.parse_args()
    
    # Handle person relation queries
    if args.person and args.relations:
        person = get_person_by_id(args.person)
        if not person:
            print(f"Person '{args.person}' not found.")
            return
        
        print(f"## {person.get('name')} ({person.get('dynasty')}) - {person.get('role')}")
        print()
        
        relations = get_relations(args.person)
        if not relations:
            print("No relations found.")
            return
        
        # Group by relation type
        relation_types = {}
        for r in relations:
            rtype = r.get("type", "unknown")
            if rtype not in relation_types:
                relation_types[rtype] = []
            relation_types[rtype].append(r)
        
        # Display relations
        for rtype, rels in relation_types.items():
            print(f"### {rtype}")
            for r in rels:
                other_id = r.get("target") if r.get("source") == args.person else r.get("source")
                other_person = get_person_by_id(other_id)
                other_name = other_person.get("name") if other_person else other_id
                desc = r.get("description", "")
                print(f"- **{other_name}**: {desc}")
            print()
        return
    
    if args.dynasties:
        # Multiple dynasties (comma-separated)
        dynasty_list = [d.strip() for d in args.dynasties.split(",")]
        all_figures = []
        for dynasty in dynasty_list:
            all_figures.extend(get_figures_by_dynasty(dynasty))
        figures = all_figures
    elif args.dynasty:
        # Single dynasty
        figures = get_figures_by_dynasty(args.dynasty)
    else:
        # If no dynasty specified, show all figures
        figures = load_figures()
    
    # Format the output
    if args.format == "md":
        output = format_markdown_table(figures)
    elif args.format == "json":
        output = format_json(figures)
    elif args.format == "csv":
        output = format_csv(figures)
    
    # Print to console
    print(output)
    
    # Export to file if requested
    if args.export:
        project_root = Path(__file__).parent.parent
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / args.export
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n[Exported to {output_file}]")


if __name__ == "__main__":
    main()