#!/usr/bin/env python3
"""Build a single translation-briefs JSON from the manifest.

Each entry is a self-contained brief a translator can use:
  - source_path:   relative path to the cleaned Chinese markdown
  - target_path:   relative path the English markdown should be written to
  - title_en:      English title to use as the H1 heading
  - char_count:    rough size, helpful for batching
  - image_map:     {s3_url -> relative path to use in the translation}
  - link_map:      {notion_url_or_id -> relative_path | null}
                   relative_path is what the link should point to.
                   null means "unmapped — rewriter will mark (Notion) later".

Also emits a global link_map keyed on bare 32-char id for the rewriter.
"""
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / ".notion-cache" / "manifest.json"
OUT = REPO / ".notion-cache" / "briefs.json"


def main() -> None:
    m = json.load(MANIFEST.open("r", encoding="utf-8"))
    pages = m["pages"]

    # global id -> (target_path, title_en) for any ok page
    id_to_target = {
        pid: (p["target_path"], p.get("title_en", ""))
        for pid, p in pages.items()
        if p.get("fetch_status") == "ok" and p.get("target_path")
    }

    briefs = {}
    for pid, p in pages.items():
        if p.get("fetch_status") != "ok":
            continue
        target = p["target_path"]
        target_dir = Path(target).parent

        # Image map: s3 url -> path relative to the target file
        image_map = {}
        for img in p.get("images", []):
            if not img.get("downloaded"):
                continue
            final = Path(img["final_path"])
            try:
                rel = os.path.relpath(REPO / final, REPO / target_dir)
            except ValueError:
                rel = str(final)
            if not rel.startswith("."):
                rel = "./" + rel
            image_map[img["src_url"]] = rel

        # Link map: only ids the page references AND we have target paths for.
        link_map = {}
        for cid in p.get("child_page_ids", []):
            if cid not in id_to_target:
                continue
            ctarget, ctitle = id_to_target[cid]
            try:
                rel = os.path.relpath(REPO / ctarget, REPO / target_dir)
            except ValueError:
                rel = ctarget
            if not rel.startswith("."):
                rel = "./" + rel
            link_map[cid] = {"path": rel, "title_en": ctitle}

        briefs[pid] = {
            "id": pid,
            "title_zh": p.get("title_zh", ""),
            "title_en": p.get("title_en", ""),
            "source_path": p.get("md_zh_path", "").replace("md-zh", "md-clean"),
            "target_path": target,
            "char_count": p.get("char_count", 0),
            "image_map": image_map,
            "link_map": link_map,
        }

    # Global rewriter map (used in pass 2 to catch any leftover bare URLs)
    global_link_map = {pid: t for pid, (t, _) in id_to_target.items()}

    json.dump(
        {"pages": briefs, "global_link_map": global_link_map},
        OUT.open("w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    print(f"Wrote {OUT.relative_to(REPO)} with {len(briefs)} briefs.")


if __name__ == "__main__":
    main()
