#!/usr/bin/env python3
"""Walk every cached page and emit an inventory of <file> embeds.

Each entry: page_id, slug, target_path (where the page lives in docs/),
source_url (the inner http(s) URL after decoding the file:// envelope),
filename (the original Chinese name), is_signed (bool), local_path
(where the downloaded file should land on disk), local_rel (the path
to use in the markdown link, relative to the doc file).

Subcommands:
  inventory               Print a JSON inventory to stdout (or write to
                          .notion-cache/files.json with --write).
  download-unsigned       Download every entry whose URL is not signed,
                          updating .notion-cache/files.json with status.
  download-signed <id>    For one page id, re-extract its file URLs from
                          the (just-refreshed) raw JSON and download them.
                          Caller is responsible for refreshing the raw
                          file before invoking this command.
  refresh-raw <id> <path> Replace the raw JSON for a page in place. Use
                          when a fresh notion-fetch result has been
                          captured to a tmp file.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / ".notion-cache"
MANIFEST = CACHE / "manifest.json"
FILES_INVENTORY = CACHE / "files.json"


SIGNED_HOST = "prod-files-secure"
UNSIGNED_HOST = "secure.notion-static.com"


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text[:max_len].rstrip("-")) or "file"


def guess_ext(filename: str, url: str) -> str:
    for src in (filename, url.split("?", 1)[0]):
        for ext in (".pdf", ".pptx", ".ppt", ".mp4", ".mov", ".zip", ".docx", ".doc", ".xlsx"):
            if src.lower().endswith(ext):
                return ext
    return ".bin"


def parse_inner(envelope_url: str) -> dict | None:
    """Decode a file://%7B...%7D Notion envelope.

    Returns a dict with keys:
      source: the raw S3 URL (often forbidden directly)
      filename: the last URL path segment, URL-decoded
      download_url: a notion.so/signed/... URL that 302s to a fresh
                    signed file.notion.so URL we CAN download
    """
    if not envelope_url.startswith("file://"):
        return None
    body = urllib.parse.unquote(envelope_url[7:])
    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        return None
    src = obj.get("source", "")
    if not src.startswith("http"):
        return None
    perm = obj.get("permissionRecord", {})
    table = perm.get("table", "block")
    block_id = perm.get("id", "")
    space_id = perm.get("spaceId", "")
    path = urllib.parse.urlparse(src).path
    raw = path.rsplit("/", 1)[-1]
    filename = urllib.parse.unquote(raw)
    # Build the notion.so/signed/ resolver URL.
    encoded_src = urllib.parse.quote(src, safe="")
    download_url = (
        f"https://www.notion.so/signed/{encoded_src}"
        f"?table={table}&id={block_id}&spaceId={space_id}"
    )
    return {
        "source": src,
        "filename": filename,
        "download_url": download_url,
    }


def extract_for_page(raw_path: Path, manifest_page: dict) -> list[dict]:
    """Return a list of file-embed dicts for the given cached page."""
    if not raw_path.exists():
        return []
    obj = json.loads(raw_path.read_text(encoding="utf-8"))
    if isinstance(obj, list):
        body = json.loads(obj[0]["text"])["text"]
    else:
        body = obj["text"]

    target_path = manifest_page.get("target_path", "")
    slug = manifest_page.get("slug", "")
    target_dir = Path(target_path).parent if target_path else Path("docs")
    asset_dir_rel = Path("assets") / slug
    asset_dir_abs = REPO / target_dir / asset_dir_rel

    entries: list[dict] = []
    seen_filenames: dict[str, int] = {}

    for m in re.finditer(r'<(?:file|video|audio)\s+src="(file://[^"]+)"\s*/?>', body):
        decoded = parse_inner(m.group(1))
        if not decoded:
            continue
        src_url = decoded["source"]
        filename = decoded["filename"]
        download_url = decoded["download_url"]

        ext = guess_ext(filename, src_url)
        # Strip extension to slugify the stem only; re-attach.
        stem = filename
        for e in (".pdf", ".pptx", ".ppt", ".mp4", ".mov", ".zip", ".docx", ".doc", ".xlsx"):
            if stem.lower().endswith(e):
                stem = stem[: -len(e)]
                break
        ascii_slug = slugify(stem) or "file"
        # Disambiguate identical slugs within one page.
        seen_filenames[ascii_slug] = seen_filenames.get(ascii_slug, 0) + 1
        if seen_filenames[ascii_slug] > 1:
            ascii_slug = f"{ascii_slug}-{seen_filenames[ascii_slug]}"
        local_basename = f"{ascii_slug}{ext}"

        local_abs = asset_dir_abs / local_basename
        local_rel = "./" + str(asset_dir_rel / local_basename)

        entries.append(
            {
                "page_id": manifest_page["id"],
                "doc_path": target_path,
                "slug": slug,
                "filename_zh": filename,
                "source_url": src_url,
                "download_url": download_url,
                "is_signed": SIGNED_HOST in src_url,
                "local_abs": str(local_abs.relative_to(REPO)),
                "local_rel": local_rel,
                "downloaded": False,
            }
        )
    return entries


def cmd_inventory(write: bool = False) -> None:
    m = json.load(MANIFEST.open("r", encoding="utf-8"))
    inventory: list[dict] = []
    for pid, page in m["pages"].items():
        if page.get("fetch_status") != "ok":
            continue
        raw = REPO / page.get("raw_path", "")
        inventory.extend(extract_for_page(raw, page))
    out = {
        "by_page": {},
        "totals": {"all": len(inventory), "signed": 0, "unsigned": 0},
    }
    for e in inventory:
        out["by_page"].setdefault(e["page_id"], []).append(e)
        if e["is_signed"]:
            out["totals"]["signed"] += 1
        else:
            out["totals"]["unsigned"] += 1

    text = json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True)
    if write:
        FILES_INVENTORY.write_text(text, encoding="utf-8")
        print(f"wrote {FILES_INVENTORY.relative_to(REPO)}: {out['totals']}")
    else:
        print(text)


def _save_inventory(out: dict) -> None:
    FILES_INVENTORY.write_text(
        json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _load_inventory() -> dict:
    return json.load(FILES_INVENTORY.open("r", encoding="utf-8"))


def _curl(url: str, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["curl", "-fsSL", "--max-time", "120", "-o", str(dst), url],
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def cmd_download_all() -> None:
    """Download every entry in the inventory using the notion.so/signed/
    resolver URL (which 302s to a fresh file.notion.so signed URL).

    Works for both 'secure.notion-static.com' and 'prod-files-secure'
    sources because both go through the same resolver."""
    out = _load_inventory()
    ok = fail = skipped = 0
    for pid, entries in out["by_page"].items():
        for e in entries:
            if e.get("downloaded"):
                skipped += 1
                continue
            dst = REPO / e["local_abs"]
            if dst.exists():
                e["downloaded"] = True
                skipped += 1
                continue
            url = e.get("download_url") or e["source_url"]
            if _curl(url, dst):
                e["downloaded"] = True
                ok += 1
            else:
                fail += 1
    _save_inventory(out)
    print(f"downloads: ok={ok} skipped={skipped} fail={fail}")


def cmd_refresh_raw(page_id: str, src_path: str) -> None:
    src = Path(src_path)
    obj = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(obj, list):
        obj = [{"type": "text", "text": json.dumps(obj, ensure_ascii=False)}]
    dst = CACHE / "raw" / f"{page_id}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    print(f"refreshed {dst.relative_to(REPO)}")


def cmd_download_signed(page_id: str) -> None:
    """Re-extract file URLs for one page from its (just-refreshed) raw JSON
    and download. Useful when a fresh signed URL has been captured."""
    m = json.load(MANIFEST.open("r", encoding="utf-8"))
    page = m["pages"].get(page_id)
    if not page:
        sys.exit(f"unknown page id: {page_id}")
    raw = REPO / page.get("raw_path", "")
    fresh_entries = extract_for_page(raw, page)
    inv = _load_inventory()
    by_page = inv["by_page"]
    # Replace the page's entries with the fresh URLs but preserve any
    # already-downloaded flags by matching on filename_zh.
    old_by_name = {e["filename_zh"]: e for e in by_page.get(page_id, [])}
    for e in fresh_entries:
        prior = old_by_name.get(e["filename_zh"])
        if prior and prior.get("downloaded"):
            e["downloaded"] = True
    by_page[page_id] = fresh_entries
    inv["totals"] = {
        "all": sum(len(v) for v in by_page.values()),
        "signed": sum(1 for v in by_page.values() for e in v if e["is_signed"]),
        "unsigned": sum(1 for v in by_page.values() for e in v if not e["is_signed"]),
    }
    ok = fail = 0
    for e in fresh_entries:
        if e.get("downloaded"):
            continue
        dst = REPO / e["local_abs"]
        if dst.exists():
            e["downloaded"] = True
            continue
        if _curl(e["source_url"], dst):
            e["downloaded"] = True
            ok += 1
        else:
            fail += 1
    _save_inventory(inv)
    print(f"{page_id}: downloaded ok={ok} fail={fail}")


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd = argv[1]
    rest = argv[2:]
    if cmd == "inventory":
        cmd_inventory(write="--write" in rest)
    elif cmd == "download-all":
        cmd_download_all()
    elif cmd == "refresh-raw":
        cmd_refresh_raw(*rest)
    elif cmd == "download-signed":
        cmd_download_signed(*rest)
    else:
        sys.exit(f"unknown subcommand: {cmd}\n{__doc__}")


if __name__ == "__main__":
    main(sys.argv)
