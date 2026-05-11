#!/usr/bin/env python3
"""Copy every downloaded image from .notion-cache/images/<id>/ to its
final_path under docs/.../assets/."""
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / ".notion-cache" / "manifest.json"


def main() -> None:
    m = json.load(MANIFEST.open("r", encoding="utf-8"))
    copied = 0
    skipped = 0
    missing = 0
    for pid, p in m["pages"].items():
        if p.get("fetch_status") != "ok":
            continue
        for img in p.get("images", []):
            if not img.get("downloaded"):
                continue
            src = REPO / img["local_cache"]
            dst = REPO / img["final_path"]
            if not src.exists():
                print(f"MISSING source: {src}")
                missing += 1
                continue
            if dst.exists():
                skipped += 1
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
    print(f"copied={copied} skipped={skipped} missing={missing}")


if __name__ == "__main__":
    main()
