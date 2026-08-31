#!/usr/bin/env python3
"""Download a resolved, public open-access PDF and write provenance metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Direct lawful public PDF URL.")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--filename")
    parser.add_argument("--doi")
    parser.add_argument("--title")
    parser.add_argument("--journal")
    parser.add_argument("--year", type=int)
    parser.add_argument("--project", action="append", default=[])
    parser.add_argument("--topic", action="append", default=[])
    parser.add_argument("--access-route", default="open_access")
    parser.add_argument("--max-mib", type=int, default=100)
    return parser.parse_args()


def slug(value: str, limit: int = 120) -> str:
    value = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE).strip("._")
    return (value or "paper")[:limit]


def atomic_json(path: Path, payload: dict) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def main() -> int:
    args = parse_args()
    parsed = urllib.parse.urlparse(args.url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SystemExit("Only direct http/https public PDF URLs are accepted.")

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    base = args.filename
    if not base:
        identity = args.title or args.doi or Path(parsed.path).stem or "paper"
        base = "_".join(part for part in (str(args.year or ""), identity) if part)
    filename = slug(base)
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    request = urllib.request.Request(
        args.url,
        headers={"User-Agent": "literature-intelligence/1.0 lawful-open-access-retrieval"},
    )
    limit = args.max_mib * 1024 * 1024
    with urllib.request.urlopen(request, timeout=45) as response:
        final_url = response.geturl()
        content_type = response.headers.get_content_type()
        declared = response.headers.get("Content-Length")
        if declared and int(declared) > limit:
            raise SystemExit(f"PDF exceeds --max-mib ({args.max_mib} MiB).")
        with tempfile.NamedTemporaryFile("wb", dir=out_dir, delete=False) as handle:
            temporary = Path(handle.name)
            digest = hashlib.sha256()
            total = 0
            head = b""
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                if not head:
                    head = chunk[:1024]
                total += len(chunk)
                if total > limit:
                    handle.close()
                    temporary.unlink(missing_ok=True)
                    raise SystemExit(f"PDF exceeds --max-mib ({args.max_mib} MiB).")
                digest.update(chunk)
                handle.write(chunk)

    if b"%PDF-" not in head or total == 0:
        temporary.unlink(missing_ok=True)
        raise SystemExit(f"Downloaded content is not a PDF (content-type: {content_type}).")

    file_hash = digest.hexdigest()
    destination = out_dir / filename
    if destination.exists():
        existing_hash = hashlib.sha256(destination.read_bytes()).hexdigest()
        if existing_hash == file_hash:
            temporary.unlink(missing_ok=True)
        else:
            destination = destination.with_name(f"{destination.stem}__{file_hash[:10]}.pdf")
            temporary.replace(destination)
    else:
        temporary.replace(destination)

    metadata = {
        "title": args.title,
        "journal": args.journal,
        "year": args.year,
        "doi": args.doi.lower().strip() if args.doi else None,
        "source_url": args.url,
        "resolved_url": final_url,
        "access_route": args.access_route,
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "sha256": file_hash,
        "size_bytes": destination.stat().st_size,
        "local_pdf": str(destination),
        "project": args.project,
        "topic": args.topic,
        "status": "FULLTEXT_AVAILABLE",
    }
    metadata_path = destination.with_suffix(".metadata.json")
    atomic_json(metadata_path, metadata)
    print(json.dumps({"pdf": str(destination), "metadata": str(metadata_path), **metadata}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

