#!/usr/bin/env python3
"""Helper for the Notion -> Markdown migration.

Subcommands:
  init                       Create manifest from seed list.
  add-fetched <id> <path>    Record a fetched raw response, parse out
                             title/ancestors/images/sub-page links;
                             update manifest.
  next                       Print next page id to fetch (BFS pop), or
                             empty if queue drained.
  download-images <id>       curl every image for the page, update manifest.
  wrap-inline <src> <dst>    Wrap an inline MCP response (single JSON object)
                             into the array-of-text shape add-fetched expects.
  process-inline <id>        Read an inline JSON object from stdin, wrap it,
                             add to manifest, and download images. One-shot.
  list-ok                    Print every page id whose fetch_status==ok.
  list-needing-translation   Print every ok page id whose translation_status!=done.
  sanitise <id>              Strip Notion-specific markup, write
                             .notion-cache/md-clean/<id>.md (still in zh).
  rewrite-links <file>       Apply manifest link map to the given file.
  set-target <id> <path>     Set target_path for a page (used after slug decisions).
  set-translated <id>        Mark translation_status=done for a page.
  status                     Print queue / done counts and any failures.
  verify                     Run all checks (no CJK leakage, all relative
                             paths exist, image files present).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / ".notion-cache"
DOCS = REPO / "docs"
MANIFEST = CACHE / "manifest.json"

DEPTH_CAP = 2
PAGE_CAP = 150
WORKSPACE_ROOT_HINT = "pengsida"  # used for the workspace check

PAGE_ID_RE = re.compile(
    r"([0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12})",
    re.IGNORECASE,
)
NOTION_HOST_RE = re.compile(r"https?://[^\s)\"<>]*notion\.(?:so|site)[^\s)\"<>]*")
S3_URL_RE = re.compile(r"https?://[^\s)\"<>]*amazonaws\.com[^\s)\"<>]*")

# Banned vocabulary for the avoid-ai-writing post-check.
BANNED = re.compile(
    r"(?:—|\bdelve\b|\bleverage\b|\brobust\b|\bseamless\b|\becosystem\b|\bharness\b)",
    re.IGNORECASE,
)
CJK_RE = re.compile(r"[一-鿿㐀-䶿]")

# ---------- Seeds ----------

SEEDS = [
    ("1713fe292ff1808eb33be93ea2d79ad9", "Sebastian Starke 模板博士生", ["seed:README.md:18"]),
    ("b43507ef26d044bd888ac29f4736e116", "如何做 research project", ["seed:README.md:23"]),
    ("c13c7e52aab64c1a8e3576b97fcb9851", "如何练习写论文", ["seed:README.md:25"]),
    ("c1a22465a0fa4b15a12985223916048e", "论文写作模板", ["seed:README.md:26"]),
    ("74aef88b9187439fa4e301704f6eb49a", "高水平科研工作者的写作经验", ["seed:README.md:27"]),
    ("af99ce47103e4917b6a5bd1fd4b3c022", "怎么 rebuttal", ["seed:README.md:28"]),
    ("810f02670691444f8c94cc3d5b76dcbc", "怎么做学术报告 slides", ["seed:README.md:29"]),
    ("8911dcc5922b4442a80d4407926e65bf", "学习计划样例", ["seed:getting_started_in_research.md:19"]),
    ("59569d7b66954578b21bf1dc6ea35776", "常用工具与配置", ["seed:getting_started_in_research.md:25"]),
    ("a3fe9f17b8af46558cd1112627009c83", "第三阶段心理准备", ["seed:getting_started_in_research.md:31"]),
    ("da6ce171c13846b7a7ffaa7473ffa6ea", "如何培养想 idea 的能力", ["seed:getting_advanced_in_research.md:5"]),
    ("d192db870bc64436ae4a4a590b36772a", "如何有效地读论文", ["seed:getting_advanced_in_research.md:6"]),
    ("d697ef578d784c869d4f8314f0d617da", "每周 meet 的 ppt 展示", ["seed:getting_advanced_in_research.md:6"]),
    ("1aee6e718de6472f834d13da8f4ff097", "如何分析实验不 work 的原因", ["seed:getting_advanced_in_research.md:7"]),
    ("caf34717f4c046c69ee7e14ea953c46f", "怎么写实验记录", ["seed:getting_advanced_in_research.md:7"]),
    ("c278dab7e4764d61a92c1fd1ef3135b1", "怎么找论文", ["seed:changelog:3"]),
    ("1753fe292ff180948215cf82cd2b30ae", "Project 核心技术问题分析模板", ["seed:changelog:9"]),
    ("1d13fe292ff180de91afcb7f2eb57b69", "从面试问题反思科研", ["seed:changelog:12"]),
]

# ---------- Helpers ----------


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_manifest() -> dict:
    if not MANIFEST.exists():
        return {"version": 1, "started_at": now_iso(), "pages": {}}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_manifest(m: dict) -> None:
    m["last_updated_at"] = now_iso()
    CACHE.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="manifest.", suffix=".tmp", dir=str(CACHE))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False, indent=2, sort_keys=True)
        os.replace(tmp, MANIFEST)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def normalise_id(raw: str) -> str | None:
    m = PAGE_ID_RE.search(raw)
    if not m:
        return None
    nid = m.group(1).replace("-", "").lower()
    return nid if len(nid) == 32 else None


def canonical_url(page_id: str) -> str:
    return f"https://pengsida.notion.site/{page_id}"


def slugify(text: str, max_len: int = 50) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-+", "-", text)
    return (text[:max_len].rstrip("-")) or "page"


def parse_raw(raw_path: Path) -> dict:
    """Pull the inner page payload out of a Notion-MCP tool-result JSON file.

    The file is a JSON array of {type, text} elements; the text element is
    itself a JSON string with metadata/title/url/text fields. We unwrap.
    """
    outer = json.loads(raw_path.read_text(encoding="utf-8"))
    if not isinstance(outer, list) or not outer:
        raise ValueError(f"Unexpected raw shape in {raw_path}")
    inner_text = outer[0].get("text", "")
    try:
        inner = json.loads(inner_text)
    except json.JSONDecodeError:
        # Some responses might already be plain text.
        return {
            "title": "",
            "url": "",
            "text": inner_text,
            "ancestors": [],
        }
    return {
        "title": inner.get("title", ""),
        "url": inner.get("url", ""),
        "text": inner.get("text", ""),
        "ancestors": _extract_ancestors(inner.get("text", "")),
    }


def _extract_ancestors(body: str) -> list[str]:
    m = re.search(
        r"<ancestor-path>(.*?)</ancestor-path>", body, re.DOTALL,
    )
    if not m:
        return []
    inner = m.group(1)
    parts = re.findall(r"<ancestor[^>]*>(.*?)</ancestor>", inner, re.DOTALL)
    if parts:
        return [p.strip() for p in parts if p.strip()]
    crumbs = [c.strip() for c in inner.split("/") if c.strip()]
    return crumbs


def _extract_child_ids(body: str, self_id: str) -> list[str]:
    found = []
    seen = set()
    for url in NOTION_HOST_RE.findall(body):
        nid = normalise_id(url)
        if not nid or nid == self_id or nid in seen:
            continue
        seen.add(nid)
        found.append(nid)
    for m in re.finditer(r'<mention-page url="([^"]+)"', body):
        nid = normalise_id(m.group(1))
        if not nid or nid == self_id or nid in seen:
            continue
        seen.add(nid)
        found.append(nid)
    return found


def _extract_image_urls(body: str) -> list[str]:
    found = []
    seen = set()
    # Standard markdown image
    for m in re.finditer(r"!\[[^\]]*\]\((https?://[^)]+amazonaws\.com[^)]+)\)", body):
        u = m.group(1)
        if u not in seen:
            seen.add(u)
            found.append(u)
    # <file src="..."> for image files (heuristic: ends with image ext)
    for m in re.finditer(r'<file\s+src="(https?://[^"]+amazonaws\.com[^"]+)"', body):
        u = m.group(1)
        if u not in seen:
            seen.add(u)
            found.append(u)
    # Bare S3 URL inside <img src="...">
    for m in re.finditer(r'<img\s+[^>]*src="(https?://[^"]+amazonaws\.com[^"]+)"', body):
        u = m.group(1)
        if u not in seen:
            seen.add(u)
            found.append(u)
    return found


def ensure_seed_entries(m: dict) -> None:
    pages = m.setdefault("pages", {})
    for pid, title_zh, refs in SEEDS:
        if pid not in pages:
            pages[pid] = {
                "id": pid,
                "url_canonical": canonical_url(pid),
                "title_zh": title_zh,
                "title_en": "",
                "slug": "",
                "ancestor_path": [],
                "target_path": "",
                "depth": 0,
                "discovered_from": refs,
                "fetch_status": "queued",
                "fetch_error": None,
                "fetched_at": None,
                "raw_path": "",
                "md_zh_path": "",
                "char_count": 0,
                "child_page_ids": [],
                "images": [],
                "translation_status": "pending",
                "translated_at": None,
            }


# ---------- Subcommands ----------


def cmd_init() -> None:
    m = load_manifest()
    ensure_seed_entries(m)
    save_manifest(m)
    print(f"Initialised manifest with {len(m['pages'])} seed entries at {MANIFEST}")


def cmd_next() -> None:
    m = load_manifest()
    pages = m.get("pages", {})
    queued = [(p.get("depth", 0), pid) for pid, p in pages.items() if p.get("fetch_status") == "queued"]
    if not queued:
        return
    queued.sort(key=lambda x: (x[0], x[1]))
    print(queued[0][1])


def cmd_wrap_inline(src_path: str, dst_path: str) -> None:
    src = Path(src_path)
    dst = Path(dst_path)
    obj = json.loads(src.read_text(encoding="utf-8"))
    if isinstance(obj, list):
        # Already in the expected shape.
        dst.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    else:
        wrapped = [{"type": "text", "text": json.dumps(obj, ensure_ascii=False)}]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(wrapped, ensure_ascii=False), encoding="utf-8")
    print(f"wrapped {src} -> {dst}")


def cmd_process_inline(page_id: str) -> None:
    page_id = normalise_id(page_id) or page_id
    raw_text = sys.stdin.read()
    obj = json.loads(raw_text)
    if not isinstance(obj, list):
        wrapped = [{"type": "text", "text": json.dumps(obj, ensure_ascii=False)}]
    else:
        wrapped = obj
    raw_dest = CACHE / "raw" / f"{page_id}.json"
    raw_dest.parent.mkdir(parents=True, exist_ok=True)
    raw_dest.write_text(json.dumps(wrapped, ensure_ascii=False), encoding="utf-8")
    cmd_add_fetched(page_id, str(raw_dest))
    cmd_download_images(page_id)


def cmd_add_fetched(page_id: str, raw_path_str: str) -> None:
    page_id = normalise_id(page_id) or page_id
    raw_src = Path(raw_path_str)
    if not raw_src.exists():
        sys.exit(f"raw file not found: {raw_src}")

    m = load_manifest()
    pages = m.setdefault("pages", {})
    if page_id not in pages:
        pages[page_id] = {
            "id": page_id,
            "url_canonical": canonical_url(page_id),
            "title_zh": "",
            "title_en": "",
            "slug": "",
            "ancestor_path": [],
            "target_path": "",
            "depth": 0,
            "discovered_from": [],
            "fetch_status": "queued",
            "fetch_error": None,
            "fetched_at": None,
            "raw_path": "",
            "md_zh_path": "",
            "char_count": 0,
            "child_page_ids": [],
            "images": [],
            "translation_status": "pending",
            "translated_at": None,
        }
    page = pages[page_id]

    raw_dest = CACHE / "raw" / f"{page_id}.json"
    raw_dest.parent.mkdir(parents=True, exist_ok=True)
    if raw_src.resolve() != raw_dest.resolve():
        shutil.copy2(raw_src, raw_dest)

    parsed = parse_raw(raw_dest)
    body = parsed["text"]

    # Detect "private/inaccessible" responses.
    lowered = body.lower()
    if (
        "permission" in lowered and "denied" in lowered
    ) or "未对外公开" in body or "page not found" in lowered:
        page["fetch_status"] = "private"
        page["fetch_error"] = body[:300]
        page["fetched_at"] = now_iso()
        save_manifest(m)
        print(f"{page_id}: marked private")
        return

    md_dest = CACHE / "md-zh" / f"{page_id}.md"
    md_dest.parent.mkdir(parents=True, exist_ok=True)
    md_dest.write_text(body, encoding="utf-8")

    if parsed["title"] and not page["title_zh"]:
        page["title_zh"] = parsed["title"]

    page["fetch_status"] = "ok"
    page["fetched_at"] = now_iso()
    page["raw_path"] = str(raw_dest.relative_to(REPO))
    page["md_zh_path"] = str(md_dest.relative_to(REPO))
    page["char_count"] = len(body)
    page["ancestor_path"] = parsed["ancestors"]

    images = []
    for idx, src in enumerate(_extract_image_urls(body), start=1):
        ext = _guess_ext(src)
        local = CACHE / "images" / page_id / f"{idx:03d}{ext}"
        images.append(
            {
                "index": idx,
                "src_url": src,
                "local_cache": str(local.relative_to(REPO)),
                "final_path": "",
                "downloaded": False,
                "ext": ext,
            }
        )
    page["images"] = images

    children = _extract_child_ids(body, page_id)
    page["child_page_ids"] = children

    # Enqueue children if within caps and workspace.
    in_workspace = _is_in_workspace(parsed["ancestors"])
    next_depth = page.get("depth", 0) + 1
    total = len(pages)
    if in_workspace and next_depth <= DEPTH_CAP and total < PAGE_CAP:
        for cid in children:
            if total >= PAGE_CAP:
                break
            if cid in pages:
                continue
            pages[cid] = {
                "id": cid,
                "url_canonical": canonical_url(cid),
                "title_zh": "",
                "title_en": "",
                "slug": "",
                "ancestor_path": [],
                "target_path": "",
                "depth": next_depth,
                "discovered_from": [f"child-of:{page_id}"],
                "fetch_status": "queued",
                "fetch_error": None,
                "fetched_at": None,
                "raw_path": "",
                "md_zh_path": "",
                "char_count": 0,
                "child_page_ids": [],
                "images": [],
                "translation_status": "pending",
                "translated_at": None,
            }
            total += 1

    save_manifest(m)
    print(
        f"{page_id}: ok char_count={len(body)} images={len(images)} children={len(children)}"
    )


def _guess_ext(url: str) -> str:
    head = url.split("?", 1)[0].lower()
    for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
        if head.endswith(ext):
            return ext if ext != ".jpeg" else ".jpg"
    return ".bin"


def _is_in_workspace(ancestors: list[str]) -> bool:
    if not ancestors:
        return True  # be permissive when ancestor info absent
    joined = " ".join(ancestors).lower()
    return WORKSPACE_ROOT_HINT in joined or True  # default permissive


def cmd_download_images(page_id: str) -> None:
    page_id = normalise_id(page_id) or page_id
    m = load_manifest()
    pages = m.get("pages", {})
    if page_id not in pages:
        sys.exit(f"unknown page id: {page_id}")
    page = pages[page_id]
    failures = 0
    for img in page.get("images", []):
        if img.get("downloaded"):
            continue
        local = REPO / img["local_cache"]
        local.parent.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(
                [
                    "curl",
                    "-fsSL",
                    "--max-time",
                    "60",
                    "-o",
                    str(local),
                    img["src_url"],
                ],
                check=True,
            )
            img["downloaded"] = True
        except subprocess.CalledProcessError as e:
            failures += 1
            img["downloaded"] = False
            img["last_error"] = str(e)
    save_manifest(m)
    total = len(page.get("images", []))
    print(f"{page_id}: downloaded {total - failures}/{total} images")


def cmd_list_ok() -> None:
    m = load_manifest()
    for pid, p in m.get("pages", {}).items():
        if p.get("fetch_status") == "ok":
            print(pid)


def cmd_list_needing_translation() -> None:
    m = load_manifest()
    for pid, p in m.get("pages", {}).items():
        if p.get("fetch_status") == "ok" and p.get("translation_status") != "done":
            print(pid)


def cmd_status() -> None:
    m = load_manifest()
    pages = m.get("pages", {})
    counts = {"queued": 0, "ok": 0, "private": 0, "failed": 0}
    trans = {"pending": 0, "done": 0, "failed": 0}
    for p in pages.values():
        counts[p.get("fetch_status", "queued")] = counts.get(p.get("fetch_status", "queued"), 0) + 1
        trans[p.get("translation_status", "pending")] = trans.get(p.get("translation_status", "pending"), 0) + 1
    print(f"pages total: {len(pages)}")
    print(f"  fetch:       {counts}")
    print(f"  translation: {trans}")
    failed = [pid for pid, p in pages.items() if p.get("fetch_status") in ("failed", "private")]
    if failed:
        print("  failed/private ids:")
        for pid in failed:
            p = pages[pid]
            print(f"    {pid}  status={p.get('fetch_status')}  title={p.get('title_zh','')!r}")


def cmd_set_target(page_id: str, target: str) -> None:
    page_id = normalise_id(page_id) or page_id
    m = load_manifest()
    if page_id not in m.get("pages", {}):
        sys.exit(f"unknown page id: {page_id}")
    page = m["pages"][page_id]
    page["target_path"] = target
    if not page.get("slug"):
        # derive slug from final filename
        page["slug"] = Path(target).stem
    # Compute final image paths now that target is known.
    if page.get("images"):
        target_dir = Path(target).parent
        slug = page["slug"]
        for img in page["images"]:
            img["final_path"] = str(target_dir / "assets" / slug / f"{img['index']:03d}{img['ext']}")
    save_manifest(m)
    print(f"{page_id}: target={target}")


def cmd_set_translated(page_id: str) -> None:
    page_id = normalise_id(page_id) or page_id
    m = load_manifest()
    if page_id not in m.get("pages", {}):
        sys.exit(f"unknown page id: {page_id}")
    m["pages"][page_id]["translation_status"] = "done"
    m["pages"][page_id]["translated_at"] = now_iso()
    save_manifest(m)
    print(f"{page_id}: translation_status=done")


# ---------- Sanitiser ----------


_SAN_REPLACEMENTS = [
    (re.compile(r"<empty-block\s*/?>"), ""),
    (re.compile(r"<page-discussions[^>]*/?>"), ""),
    (re.compile(r"<notice[^>]*>.*?</notice>", re.DOTALL), ""),
    (re.compile(r"<span\s+color=\"[^\"]+\">(.*?)</span>", re.DOTALL), r"\1"),
    (re.compile(r"<callout\s+icon=\"[^\"]*\"\s+color=\"[^\"]*\">", re.DOTALL), "> "),
    (re.compile(r"<callout\s+icon=\"[^\"]*\">", re.DOTALL), "> "),
    (re.compile(r"</callout>"), ""),
    (re.compile(r"<colgroup>.*?</colgroup>", re.DOTALL), ""),
]


def cmd_sanitise(page_id: str) -> None:
    page_id = normalise_id(page_id) or page_id
    m = load_manifest()
    page = m.get("pages", {}).get(page_id)
    if not page:
        sys.exit(f"unknown page id: {page_id}")
    src = REPO / page.get("md_zh_path", "")
    if not src.exists():
        sys.exit(f"missing md-zh source: {src}")
    body = src.read_text(encoding="utf-8")
    # Strip the leading <page url=...><ancestor-path>...<properties>... wrappers
    # and the trailing </content></page>.
    body = re.sub(r'^Here is the result of "view".*?\n<page[^>]*>\n', "", body, count=1, flags=re.DOTALL)
    body = re.sub(r"<ancestor-path>.*?</ancestor-path>\s*", "", body, count=1, flags=re.DOTALL)
    body = re.sub(r"<properties>.*?</properties>\s*", "", body, count=1, flags=re.DOTALL)
    body = re.sub(r"^<content>\s*", "", body, count=1)
    body = re.sub(r"\s*</content>\s*</page>\s*$", "\n", body, count=1)
    for pat, repl in _SAN_REPLACEMENTS:
        body = pat.sub(repl, body)
    # Compact runs of blank lines.
    body = re.sub(r"\n{3,}", "\n\n", body)
    dest = CACHE / "md-clean" / f"{page_id}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(body, encoding="utf-8")
    print(f"{page_id}: sanitised -> {dest.relative_to(REPO)}  ({len(body)} chars)")


# ---------- Link rewriter ----------


def cmd_rewrite_links(file_path: str) -> None:
    f = Path(file_path)
    if not f.is_absolute():
        f = REPO / f
    if not f.exists():
        sys.exit(f"file not found: {f}")
    m = load_manifest()
    pages = m.get("pages", {})
    body = f.read_text(encoding="utf-8")
    file_dir = f.parent

    def repl_md(match: re.Match) -> str:
        text, url = match.group(1), match.group(2)
        nid = normalise_id(url) if "notion" in url else None
        if not nid:
            return match.group(0)
        page = pages.get(nid)
        if page and page.get("fetch_status") == "ok" and page.get("target_path"):
            target = REPO / page["target_path"]
            try:
                rel = os.path.relpath(target, file_dir)
            except ValueError:
                rel = page["target_path"]
            if not rel.startswith("."):
                rel = "./" + rel
            return f"[{text}]({rel})"
        # Untranslatable -> mark with (Notion)
        if not text.endswith("(Notion)"):
            text = f"{text} (Notion)"
        return f"[{text}]({url})"

    new_body = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", repl_md, body)

    def repl_bare(match: re.Match) -> str:
        url = match.group(0)
        nid = normalise_id(url)
        if not nid:
            return url
        page = pages.get(nid)
        if page and page.get("fetch_status") == "ok" and page.get("target_path"):
            target = REPO / page["target_path"]
            try:
                rel = os.path.relpath(target, file_dir)
            except ValueError:
                rel = page["target_path"]
            if not rel.startswith("."):
                rel = "./" + rel
            return rel
        return url

    new_body = re.sub(
        r"https?://[^\s,()<>\"]*notion\.(?:so|site)[^\s,()<>\"]*",
        repl_bare,
        new_body,
    )
    if new_body != body:
        f.write_text(new_body, encoding="utf-8")
        print(f"rewrote links in {f.relative_to(REPO)}")
    else:
        print(f"no changes for {f.relative_to(REPO)}")


# ---------- Verifier ----------


def cmd_verify() -> None:
    problems = []
    files = []
    for root in (DOCS, REPO):
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if ".notion-cache" in p.parts:
                continue
            files.append(p)
    files.append(REPO / "changelog")

    for f in files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        # Banned patterns - skip lines inside fenced code blocks (verbatim quotes)
        in_fence = False
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if BANNED.search(line):
                problems.append(f"{f.relative_to(REPO)}:{line_no}: banned pattern in: {line.strip()[:120]}")
        # Residual CJK
        for line_no, line in enumerate(text.splitlines(), start=1):
            if CJK_RE.search(line) and "<!-- zh:" not in line:
                problems.append(f"{f.relative_to(REPO)}:{line_no}: CJK residue: {line.strip()[:120]}")
        # Notion URLs without (Notion) marker
        for m in re.finditer(r"\[([^\]]+)\]\((https?://[^)]+notion\.(?:so|site)[^)]*)\)", text):
            if "(Notion)" not in m.group(1):
                problems.append(f"{f.relative_to(REPO)}: unmarked Notion URL: {m.group(2)}")
        # Internal markdown links
        for m in re.finditer(r"\[([^\]]+)\]\((?!https?:)([^)#]+)(?:#[^)]*)?\)", text):
            href = m.group(2)
            target = (f.parent / href).resolve()
            if not target.exists():
                problems.append(f"{f.relative_to(REPO)}: broken link -> {href}")
        # Image references
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
            href = m.group(1)
            if href.startswith("http"):
                continue
            target = (f.parent / href).resolve()
            if not target.exists():
                problems.append(f"{f.relative_to(REPO)}: missing image -> {href}")
    if problems:
        print(f"FOUND {len(problems)} ISSUES")
        for p in problems[:200]:
            print(" -", p)
        if len(problems) > 200:
            print(f"  ... ({len(problems) - 200} more)")
        sys.exit(1)
    print("OK: verification passed")


# ---------- Dispatch ----------


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, *rest = argv[1:]
    if cmd == "init":
        cmd_init()
    elif cmd == "next":
        cmd_next()
    elif cmd == "add-fetched":
        cmd_add_fetched(*rest)
    elif cmd == "wrap-inline":
        cmd_wrap_inline(*rest)
    elif cmd == "process-inline":
        cmd_process_inline(*rest)
    elif cmd == "download-images":
        cmd_download_images(*rest)
    elif cmd == "list-ok":
        cmd_list_ok()
    elif cmd == "list-needing-translation":
        cmd_list_needing_translation()
    elif cmd == "sanitise":
        cmd_sanitise(*rest)
    elif cmd == "rewrite-links":
        cmd_rewrite_links(*rest)
    elif cmd == "set-target":
        cmd_set_target(*rest)
    elif cmd == "set-translated":
        cmd_set_translated(*rest)
    elif cmd == "status":
        cmd_status()
    elif cmd == "verify":
        cmd_verify()
    else:
        sys.exit(f"unknown subcommand: {cmd}\n{__doc__}")


if __name__ == "__main__":
    main(sys.argv)
