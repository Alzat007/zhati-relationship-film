#!/usr/bin/env python3
"""Search free stock-video sites for background clips.

Supported now:
  - Mixkit (no key; parses the search page JSON-LD)
  - Coverr (no key; parses the search page CDN links)
  - Pexels (optional PEXELS_API_KEY)
  - Pixabay (optional PIXABAY_API_KEY)

Usage:
  stock_search.py "rain window" --limit 6
  stock_search.py "hands coffee" --source mixkit --json
"""
import argparse
import html
import json
import os
import re
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36")


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def mixkit(query, limit):
    slug = re.sub(r"\s+", "-", query.strip().lower())
    url = f"https://mixkit.co/free-stock-video/{urllib.parse.quote(slug)}/"
    try:
        page = get(url)
    except Exception:
        url = f"https://mixkit.co/free-stock-video/discover/{urllib.parse.quote(query)}/"
        page = get(url)
    out = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', page, re.S):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        graph = data.get("@graph") if isinstance(data, dict) else data
        if not isinstance(graph, list):
            graph = [graph]
        for x in graph:
            if not isinstance(x, dict) or x.get("@type") != "VideoObject":
                continue
            content = x.get("contentUrl")
            if not content:
                continue
            out.append({
                "source": "Mixkit",
                "title": clean(x.get("name") or ""),
                "url": content,
                "page": url,
                "license": "Mixkit License — check mixkit.co/license",
                "thumb": x.get("thumbnailUrl") or "",
            })
            if len(out) >= limit:
                return out
    return out


def coverr(query, limit):
    url = f"https://coverr.co/s?q={urllib.parse.quote_plus(query)}"
    page = get(url)
    seen, out = set(), []
    for slug in re.findall(r'https://cdn\.coverr\.co/videos/([^"/]+)/1080p\.mp4', page):
        if slug in seen or "paywall" in slug or slug.startswith("coverr-temp"):
            continue
        seen.add(slug)
        title = re.sub(r"^coverr-", "", slug).replace("-", " ").strip()
        out.append({
            "source": "Coverr",
            "title": title,
            "url": f"https://cdn.coverr.co/videos/{slug}/1080p.mp4",
            "page": f"https://coverr.co/videos/{slug}",
            "license": "Coverr License — check coverr.co/license",
            "thumb": "",
        })
        if len(out) >= limit:
            break
    return out


def pexels(query, limit):
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        return []
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": query, "per_page": limit})
    req = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read().decode("utf-8", "replace"))
    out = []
    for v in data.get("videos", [])[:limit]:
        files = v.get("video_files", [])
        best = max(files, key=lambda f: (f.get("width") or 0) * (f.get("height") or 0)) if files else None
        if not best:
            continue
        out.append({
            "source": "Pexels",
            "title": clean(v.get("alt") or v.get("user", {}).get("name") or ""),
            "url": best.get("link", ""),
            "page": v.get("url", ""),
            "license": "Pexels License — check pexels.com/license",
            "thumb": v.get("image", ""),
        })
    return out


def pixabay(query, limit):
    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key:
        return []
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({
        "key": key, "q": query, "per_page": max(3, min(20, limit)), "safesearch": "true"})
    data = json.loads(get(url))
    out = []
    for v in data.get("hits", [])[:limit]:
        videos = v.get("videos", {})
        best = videos.get("large") or videos.get("medium") or videos.get("small")
        if not best:
            continue
        out.append({
            "source": "Pixabay",
            "title": clean(v.get("tags") or ""),
            "url": best.get("url", ""),
            "page": v.get("pageURL", ""),
            "license": "Pixabay Content License — check pixabay.com/service/license-summary",
            "thumb": "",
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument("--source", choices=["auto", "mixkit", "coverr", "pexels", "pixabay"], default="auto")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    out = []
    if args.source in ("auto", "mixkit"):
        try: out += mixkit(args.query, args.limit)
        except Exception as e: print(f"  [mixkit] {e}", file=__import__('sys').stderr)
    if args.source == "coverr":
        try: out += coverr(args.query, args.limit)
        except Exception as e: print(f"  [coverr] {e}", file=__import__('sys').stderr)
    if args.source in ("auto", "pexels"):
        try: out += pexels(args.query, args.limit)
        except Exception as e: print(f"  [pexels] {e}", file=__import__('sys').stderr)
    if args.source in ("auto", "pixabay"):
        try: out += pixabay(args.query, args.limit)
        except Exception as e: print(f"  [pixabay] {e}", file=__import__('sys').stderr)

    # de-dupe by url
    seen, uniq = set(), []
    for x in out:
        if x["url"] and x["url"] not in seen:
            seen.add(x["url"])
            uniq.append(x)
    uniq = uniq[:args.limit]

    if args.json:
        print(json.dumps(uniq, ensure_ascii=False, indent=2))
        return
    if not uniq:
        print("no results. Set PEXELS_API_KEY/PIXABAY_API_KEY, or try a shorter English query.")
        return
    for i, x in enumerate(uniq, 1):
        print(f"[{i}] {x['source']} · {x['title'][:70] or '(untitled)'}")
        print(f"    {x['url']}")
        print(f"    page: {x['page']}")
        print(f"    license: {x['license']}")
    print("\nNext: download + normalize one with scripts/fetch_stock.py, or approve a candidate first.")


if __name__ == "__main__":
    main()
