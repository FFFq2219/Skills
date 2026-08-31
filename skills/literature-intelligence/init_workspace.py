#!/usr/bin/env python3
"""Initialize a reusable literature-intelligence workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workspace",
        default=".literature-intelligence",
        help="Directory for the index, extracted text, logs, and configuration.",
    )
    parser.add_argument(
        "--pdf-root",
        action="append",
        default=[],
        help="PDF root to scan. Repeat for multiple roots.",
    )
    parser.add_argument(
        "--managed-download-root",
        help="Separate directory for PDFs downloaded by the skill.",
    )
    parser.add_argument("--project", default="default", help="Project label.")
    parser.add_argument("--force", action="store_true", help="Replace existing config.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    config_path = workspace / "config.json"
    if config_path.exists() and not args.force:
        raise SystemExit(f"Config exists: {config_path}. Use --force to replace it.")

    roots = [str(Path(root).expanduser().resolve()) for root in args.pdf_root]
    managed_root = (
        Path(args.managed_download_root).expanduser().resolve()
        if args.managed_download_root
        else workspace / "managed-pdfs"
    )

    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "texts").mkdir(exist_ok=True)
    (workspace / "logs").mkdir(exist_ok=True)
    managed_root.mkdir(parents=True, exist_ok=True)

    config = {
        "version": 1,
        "project": args.project,
        "pdf_roots": roots,
        "managed_download_root": str(managed_root),
        "index_dir": str(workspace),
        "online_quality_gate": {
            "default_include": ["S", "A", "B"],
            "local_pdfs_exempt": True,
            "allow_documented_method_exceptions": True,
        },
    }
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"config": str(config_path), **config}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

