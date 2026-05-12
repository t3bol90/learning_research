#!/usr/bin/env python3
"""For every docs/*.md placeholder line of the form

    - English description (PDF, embedded in source) <!-- zh: filename -->
    - English description (video, embedded in source) <!-- zh: filename -->
    - English description (PPTX, embedded in source) <!-- zh: filename -->
    - English description (PDF/video, embedded in source) <!-- zh: filename -->
    - English description (embedded in source) <!-- zh: filename -->

look up the matching downloaded file in .notion-cache/files.json (by
filename_zh, scoped to the docs file's page id), rename the file under
docs/.../assets/<slug>/ to a clean ASCII name derived from the English
description, and rewrite the line to a real markdown link.

Files that have no matching docs placeholder are left where they are
(callers can clean up orphans afterwards).
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INVENTORY = REPO / ".notion-cache" / "files.json"

PLACEHOLDER_RE = re.compile(
    r"^(?P<indent>\s*-\s*)(?P<text>.+?)\s*\((?:[^)]*?)embedded in source\)\s*<!--\s*zh:\s*(?P<zh>.+?)\s*-->\s*$"
)

# Matches inline links like:
#   [Caption](https://prod-files-secure...mp4) (video, Notion)
#   [Caption](https://prod-files-secure...mp4) (Notion)
URL_LINK_RE = re.compile(
    r"\[(?P<text>[^\]]+)\]\((?P<url>https?://[^)]*amazonaws\.com[^)]*)\)\s*(?:\((?:[^)]*Notion[^)]*)\))?"
)


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text[:max_len].rstrip("-")) or "file"


def ext_from_filename(name: str) -> str:
    for ext in (".pdf", ".pptx", ".ppt", ".mp4", ".mov", ".epub", ".zip", ".docx", ".doc", ".xlsx"):
        if name.lower().endswith(ext):
            return ext
    return ".bin"


def doc_to_pageid(inv: dict) -> dict[str, str]:
    """Map docs/<...>.md absolute path -> page_id."""
    out = {}
    for pid, entries in inv["by_page"].items():
        if entries:
            out[entries[0]["doc_path"]] = pid
    return out


def main() -> None:
    inv = json.load(INVENTORY.open("r", encoding="utf-8"))
    page_for_doc = doc_to_pageid(inv)

    rewrites = 0
    misses = 0

    for docpath, pid in page_for_doc.items():
        doc = REPO / docpath
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        new_lines = []
        changed = False

        # Build a per-page name->entry map. Disambiguate when multiple
        # entries share the same filename_zh by giving each a "pop" index
        # so callers can claim them in order of appearance.
        entries_by_name: dict[str, list[dict]] = {}
        for e in inv["by_page"].get(pid, []):
            entries_by_name.setdefault(e["filename_zh"], []).append(e)

        # Track how many times we've already used each name in this doc.
        used_count: dict[str, int] = {}

        for line in text.splitlines():
            m = PLACEHOLDER_RE.match(line)
            if not m:
                new_lines.append(line)
                continue
            indent = m.group("indent")
            description = m.group("text").strip()
            zh = m.group("zh").strip()
            candidates = entries_by_name.get(zh, [])
            idx = used_count.get(zh, 0)
            if idx >= len(candidates):
                misses += 1
                new_lines.append(line)
                continue
            entry = candidates[idx]
            used_count[zh] = idx + 1

            ext = ext_from_filename(zh)
            slug = slugify(description) or slugify(Path(zh).stem) or "file"
            target_dir = (REPO / docpath).parent / "assets" / Path(docpath).stem
            target_name = f"{slug}{ext}"
            counter = 2
            target_path = target_dir / target_name
            while target_path.exists() and str(target_path.relative_to(REPO)) != entry["local_abs"]:
                target_name = f"{slug}-{counter}{ext}"
                target_path = target_dir / target_name
                counter += 1

            src_abs = REPO / entry["local_abs"]
            if src_abs.exists() and src_abs != target_path:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_abs), str(target_path))
                entry["local_abs"] = str(target_path.relative_to(REPO))
            elif not src_abs.exists() and not target_path.exists():
                misses += 1
                new_lines.append(line)
                continue

            link_target_dir = target_path.parent.relative_to((REPO / docpath).parent)
            rel_link = "./" + str(link_target_dir / target_name)
            new_lines.append(
                f"{indent}[{description}]({rel_link}) <!-- zh: {zh} -->"
            )
            rewrites += 1
            changed = True

        text = "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

        # Second pass: rewrite inline `[text](signed-S3-URL) (video, Notion)`
        # links to local paths when we have the file. Match by source_url
        # since these don't have a filename_zh marker.
        url_to_entry = {e["source_url"]: e for e in inv["by_page"].get(pid, [])}
        url_used: dict[str, int] = {}

        def url_repl(m: re.Match) -> str:
            nonlocal changed
            link_text = m.group("text").strip()
            url = m.group("url")
            entry = url_to_entry.get(url)
            if not entry:
                # Strip query string variants and try again
                bare = url.split("?", 1)[0]
                for k, v in url_to_entry.items():
                    if k.split("?", 1)[0] == bare:
                        entry = v
                        break
            if not entry:
                return m.group(0)
            ext = ext_from_filename(entry["filename_zh"])
            slug = slugify(link_text) or slugify(Path(entry["filename_zh"]).stem) or "file"
            # Ensure unique within the page's asset dir.
            target_dir = (REPO / docpath).parent / "assets" / Path(docpath).stem
            target_name = f"{slug}{ext}"
            counter = 2
            target_path = target_dir / target_name
            while target_path.exists() and str(target_path.relative_to(REPO)) != entry["local_abs"]:
                target_name = f"{slug}-{counter}{ext}"
                target_path = target_dir / target_name
                counter += 1
            src_abs = REPO / entry["local_abs"]
            if src_abs.exists() and src_abs != target_path:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_abs), str(target_path))
                entry["local_abs"] = str(target_path.relative_to(REPO))
            elif not src_abs.exists() and not target_path.exists():
                return m.group(0)
            link_target_dir = target_path.parent.relative_to((REPO / docpath).parent)
            rel_link = "./" + str(link_target_dir / target_name)
            changed = True
            nonlocal_count[0] += 1
            return f"[{link_text}]({rel_link})"

        nonlocal_count = [0]
        text = URL_LINK_RE.sub(url_repl, text)

        if changed:
            doc.write_text(text, encoding="utf-8")
            rewrites += nonlocal_count[0]

    json.dump(inv, INVENTORY.open("w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
    print(f"rewritten {rewrites} placeholder lines (misses: {misses})")


if __name__ == "__main__":
    main()
