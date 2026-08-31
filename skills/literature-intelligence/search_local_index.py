#!/usr/bin/env python3
"""Rank local indexed PDFs for exact and concept-expanded search terms."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Primary search phrase.")
    parser.add_argument("--term", action="append", default=[], help="Synonym or related term; repeatable.")
    parser.add_argument("--index-dir", default=".literature-intelligence")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--snippet-chars", type=int, default=360)
    return parser.parse_args()


def tokens(value: str) -> list[str]:
    parts = re.findall(r"[A-Za-z0-9_+.-]{2,}|[\u4e00-\u9fff]{2,}", value.lower())
    return list(dict.fromkeys(part for part in parts if len(part.strip(".-")) >= 2))


def load_catalog(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def best_snippet(text: str, terms: list[str], width: int) -> tuple[str, int | None]:
    lower = text.lower()
    positions = [lower.find(term) for term in terms if lower.find(term) >= 0]
    if not positions:
        return "", None
    center = min(positions)
    start = max(0, center - width // 3)
    end = min(len(text), start + width)
    snippet = re.sub(r"\s+", " ", text[start:end]).strip()
    marker_matches = list(re.finditer(r"=== PAGE (\d+) ===", text[:center]))
    page = int(marker_matches[-1].group(1)) if marker_matches else None
    return snippet, page


def main() -> int:
    args = parse_args()
    index_dir = Path(args.index_dir).expanduser().resolve()
    catalog_path = index_dir / "catalog.jsonl"
    if not catalog_path.exists():
        raise SystemExit(f"Catalog not found: {catalog_path}")
    search_terms = list(dict.fromkeys(tokens(args.query) + [term.lower() for term in args.term]))
    if not search_terms:
        raise SystemExit("No searchable terms.")

    ranked = []
    for entry in load_catalog(catalog_path):
        metadata = " ".join(
            str(entry.get(field) or "")
            for field in ("title", "authors", "keywords", "subject", "file_name", "path", "doi")
        ).lower()
        text = ""
        text_path = entry.get("text_file")
        if text_path and Path(text_path).exists():
            text = Path(text_path).read_text(encoding="utf-8", errors="replace")
        lower_text = text.lower()
        metadata_hits = sum(metadata.count(term) for term in search_terms)
        text_hits = sum(lower_text.count(term) for term in search_terms)
        matched_terms = [term for term in search_terms if term in metadata or term in lower_text]
        if not matched_terms:
            continue
        phrase_bonus = 8 if args.query.lower() in metadata or args.query.lower() in lower_text else 0
        coverage_bonus = 4 * len(matched_terms)
        score = 10 * min(metadata_hits, 10) + min(text_hits, 60) + phrase_bonus + coverage_bonus
        snippet, page = best_snippet(text, matched_terms, args.snippet_chars)
        ranked.append(
            {
                "score": score,
                "matched_terms": matched_terms,
                "title": entry.get("title"),
                "authors": entry.get("authors"),
                "year": entry.get("year"),
                "doi": entry.get("doi"),
                "source_type": entry.get("source_type"),
                "path": entry.get("path"),
                "page_hint": page,
                "snippet": snippet,
                "duplicate_of": entry.get("duplicate_of"),
            }
        )
    ranked.sort(key=lambda item: (-item["score"], str(item.get("title") or "")))
    output = {
        "query": args.query,
        "terms": search_terms,
        "matches": len(ranked),
        "results": ranked[: args.top],
        "note": (
            "Scores rank term relevance only, not study quality or evidence strength. "
            "Verify page hints and snippets in the original PDF before citation."
        ),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
