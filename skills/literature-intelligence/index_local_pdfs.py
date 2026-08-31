#!/usr/bin/env python3
"""Incrementally index metadata and text from one or more local PDF roots."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Workspace config.json.")
    parser.add_argument("--root", action="append", default=[], help="PDF root; repeatable.")
    parser.add_argument("--index-dir", help="Index directory; overrides config.")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Pages to extract per PDF; 0 extracts all pages.",
    )
    parser.add_argument("--no-managed-root", action="store_true")
    return parser.parse_args()


def load_config(path: str | None) -> dict[str, Any]:
    if not path:
        candidate = Path(".literature-intelligence/config.json")
        if not candidate.exists():
            return {}
        path = str(candidate)
    config_path = Path(path).expanduser().resolve()
    return json.loads(config_path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_doi(raw: str | None) -> str | None:
    if not raw:
        return None
    value = raw.strip().rstrip(".,;:)]}").lower()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value, flags=re.I)
    return value if DOI_RE.fullmatch(value) else None


def first_doi(text: str) -> str | None:
    match = DOI_RE.search(text)
    return normalize_doi(match.group(0)) if match else None


def classify_source(title: str, path: Path, first_text: str) -> str:
    haystack = f"{title} {path.name} {first_text[:5000]}".lower()
    if any(term in haystack for term in ("doctoral dissertation", "phd thesis", "博士学位论文")):
        return "phd_dissertation"
    if any(term in haystack for term in ("master thesis", "master's thesis", "硕士学位论文")):
        return "master_thesis"
    if any(term in haystack for term in ("technical report", "project report", "技术报告", "项目报告")):
        return "technical_report"
    if "preprint" in haystack:
        return "preprint"
    return "unknown"


def extract_with_pypdf(path: Path, max_pages: int) -> tuple[dict[str, Any], str]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    metadata = reader.metadata or {}
    page_total = len(reader.pages)
    take = page_total if max_pages <= 0 else min(page_total, max_pages)
    chunks: list[str] = []
    for idx in range(take):
        try:
            text = reader.pages[idx].extract_text() or ""
        except Exception as exc:  # preserve partial extraction
            text = f"[PAGE_EXTRACTION_ERROR: {type(exc).__name__}: {exc}]"
        chunks.append(f"\n\f\n=== PAGE {idx + 1} ===\n{text}")
    return (
        {
            "title": str(metadata.get("/Title") or "").strip(),
            "authors": str(metadata.get("/Author") or "").strip(),
            "subject": str(metadata.get("/Subject") or "").strip(),
            "keywords": str(metadata.get("/Keywords") or "").strip(),
            "creation_date": str(metadata.get("/CreationDate") or "").strip(),
            "pages": page_total,
            "pages_extracted": take,
            "extractor": "pypdf",
        },
        "".join(chunks),
    )


def extract_with_pdftotext(path: Path, max_pages: int) -> tuple[dict[str, Any], str]:
    executable = shutil.which("pdftotext")
    if not executable:
        raise RuntimeError("Neither pypdf nor pdftotext is available")
    command = [executable, "-layout"]
    if max_pages > 0:
        command += ["-f", "1", "-l", str(max_pages)]
    command += [str(path), "-"]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return (
        {
            "title": "",
            "authors": "",
            "subject": "",
            "keywords": "",
            "creation_date": "",
            "pages": None,
            "pages_extracted": max_pages or None,
            "extractor": "pdftotext",
        },
        completed.stdout,
    )


def extract_pdf(path: Path, max_pages: int) -> tuple[dict[str, Any], str]:
    try:
        return extract_with_pypdf(path, max_pages)
    except ImportError:
        return extract_with_pdftotext(path, max_pages)


def read_existing(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    result: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entry = json.loads(line)
            result[entry["path"]] = entry
    return result


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(text)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    roots = [Path(value).expanduser().resolve() for value in args.root]
    if not roots:
        roots = [Path(value).expanduser().resolve() for value in config.get("pdf_roots", [])]
    if not args.no_managed_root and config.get("managed_download_root"):
        managed = Path(config["managed_download_root"]).expanduser().resolve()
        if managed not in roots:
            roots.append(managed)
    if not roots:
        raise SystemExit("No PDF roots supplied. Use --root or a workspace config.")

    missing = [str(root) for root in roots if not root.exists()]
    roots = [root for root in roots if root.exists() and root.is_dir()]
    if not roots:
        raise SystemExit(f"No readable PDF roots. Missing or invalid: {missing}")

    index_dir = Path(
        args.index_dir or config.get("index_dir") or ".literature-intelligence"
    ).expanduser().resolve()
    text_dir = index_dir / "texts"
    catalog_path = index_dir / "catalog.jsonl"
    previous = read_existing(catalog_path)

    pdfs: list[Path] = []
    for root in roots:
        pdfs.extend(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf")
    pdfs = sorted(set(pdfs), key=lambda path: str(path).casefold())

    entries: list[dict[str, Any]] = []
    reused = extracted = failed = 0
    for path in pdfs:
        stat = path.stat()
        key = str(path)
        old = previous.get(key)
        if (
            old
            and old.get("size_bytes") == stat.st_size
            and old.get("mtime_ns") == stat.st_mtime_ns
            and old.get("extraction_max_pages") == args.max_pages
            and old.get("text_file")
            and Path(old["text_file"]).exists()
        ):
            entries.append(old)
            reused += 1
            continue

        entry: dict[str, Any] = {
            "path": key,
            "file_name": path.name,
            "source_origin": "local",
            "journal_tier": "not_applicable",
            "size_bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "extraction_max_pages": args.max_pages,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            file_hash = sha256_file(path)
            metadata, text = extract_pdf(path, args.max_pages)
            doi = first_doi(" ".join((metadata.get("subject", ""), text[:50000])))
            title = metadata.get("title") or path.stem
            year_match = YEAR_RE.search(
                " ".join((metadata.get("creation_date", ""), text[:10000], path.name))
            )
            text_path = text_dir / f"{file_hash}.txt"
            atomic_write_text(text_path, text)
            entry.update(metadata)
            entry.update(
                {
                    "sha256": file_hash,
                    "paper_id": f"doi:{doi}" if doi else f"sha256:{file_hash}",
                    "doi": doi,
                    "title": title,
                    "year": int(year_match.group(0)) if year_match else None,
                    "source_type": classify_source(title, path, text),
                    "text_file": str(text_path),
                    "status": "indexed",
                    "error": None,
                }
            )
            extracted += 1
        except Exception as exc:
            entry.update(
                {
                    "paper_id": f"path:{key}",
                    "title": path.stem,
                    "source_type": "unknown",
                    "status": "extraction_failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            failed += 1
        entries.append(entry)

    seen: dict[str, str] = {}
    for entry in entries:
        identities = []
        if entry.get("doi"):
            identities.append(f"doi:{entry['doi']}")
        if entry.get("sha256"):
            identities.append(f"sha256:{entry['sha256']}")
        duplicate_of = next((seen[item] for item in identities if item in seen), None)
        entry["duplicate_of"] = duplicate_of
        if not duplicate_of:
            for item in identities:
                seen[item] = entry["paper_id"]

    lines = "".join(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n" for entry in entries)
    atomic_write_text(catalog_path, lines)
    report = {
        "catalog": str(catalog_path),
        "roots": [str(root) for root in roots],
        "missing_roots": missing,
        "pdfs_found": len(pdfs),
        "reused": reused,
        "extracted": extracted,
        "failed": failed,
        "removed_since_previous_scan": len(set(previous) - {str(path) for path in pdfs}),
    }
    atomic_write_text(
        index_dir / "scan_report.json",
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())

