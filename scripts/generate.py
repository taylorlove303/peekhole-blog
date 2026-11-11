#!/usr/bin/env python3
"""Rebuild index.html, posts.json, sitemap.xml, latest.js, and homepage-snippet.html
from posts-data.json. Post HTML files in posts/ are left alone."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://blog.peekhole.com"
PEEKHOLE = "https://peekhole.com"
MAX_WIDGET_POSTS = 5


def load_posts() -> list[dict]:
    data = json.loads((ROOT / "posts-data.json").read_text())
    if not isinstance(data, list):
        raise SystemExit("posts-data.json must be a JSON array")
    required = ("title", "slug", "date", "description", "target_phrase")
    for i, post in enumerate(data):
        missing = [k for k in required if not post.get(k)]
        if missing:
            raise SystemExit(f"posts-data.json item {i} missing: {', '.join(missing)}")
        html = ROOT / "posts" / f"{post['slug']}.html"
        if not html.is_file():
            raise SystemExit(f"Missing post file: {html}")
        post["url"] = f"{SITE}/posts/{post['slug']}.html"
        if not post.get("date_display"):
            post["date_display"] = format_date(post["date"])
        if not post.get("kicker"):
            post["kicker"] = "GTA 6 news"
    # Newest first; keep file order for the same date.
    data.sort(key=lambda p: p["date"], reverse=True)
    return data


def format_date(iso: str) -> str:
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %-d, %Y")


def write(path: Path, content: str) -> None:
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content)
    print(f"wrote {path.relative_to(ROOT)}")


def make_posts_json(posts: list[dict]) -> str:
    out = []
    for p in posts:
        out.append(
            {
                "title": p["title"],
                "slug": p["slug"],
                "url": p["url"],
                "date": p["date"],
                "description": p["description"],
                "target_phrase": p["target_phrase"],
            }
        )
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def make_sitemap(posts: list[dict]) -> str:
    today = max((p["date"] for p in posts), default=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    urls = [
        (f"{SITE}/", today, "daily", "1.0"),
    ]
    for p in posts:
        urls.append((p["url"], p["date"], "weekly", "0.8"))
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod, freq, pri in urls:
        parts.append("  <url>")
        parts.append(f"    <loc>{escape(loc, quote=True)}</loc>")
        parts.append(f"    <lastmod>{lastmod}</lastmod>")
        parts.append(f"    <changefreq>{freq}</changefreq>")
        parts.append(f"    <priority>{pri}</priority>")
        parts.append("  </url>")
    parts.append("</urlset>")
    parts.append("")
    return "\n".join(parts)


def make_index(posts: list[dict]) -> str:
    cards = []
    for p in posts:
        cards.append(
            f'''      <article class="ph-card" id="{escape(p["slug"], quote=True)}">
        <p class="ph-kicker">{escape(p.get("kicker") or "GTA 6 news")}</p>
        <h2><a href="posts/{escape(p["slug"], quote=True)}.html">{escape(p["title"])}</a></h2>
        <p class="ph-date"><time datetime="{escape(p["date"], quote=True)}">{escape(p["date_display"])}</time></p>
        <p>{escape(p["description"])}</p>
        <p><a class="ph-readmore" href="posts/{escape(p["slug"], quote=True)}.html">Read the full post</a></p>
      </article>'''
        )
    cards_html = "\n".join(cards) if cards else "      <p>No posts yet.</p>"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Peekhole GTA 6 News | Peak Hole Briefings</title>
  <meta name="description" content="Daily Peekhole GTA 6 news from Taylor Love 303. Pre-loads, official updates, and neon Vice City briefings before the November 19 launch.">
  <link rel="canonical" href="{SITE}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Peekhole GTA 6 News | Peak Hole Briefings">
  <meta property="og:description" content="Daily Peekhole GTA 6 news from Taylor Love 303. Official updates and neon Vice City briefings.">
  <meta property="og:url" content="{SITE}/">
  <meta property="og:site_name" content="Peekhole">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Peekhole GTA 6 News | Peak Hole Briefings">
  <meta name="twitter:description" content="Daily Peekhole GTA 6 news from Taylor Love 303. Official updates and neon Vice City briefings.">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <div class="ph-page">
    <header class="ph-site-header">
      <a class="ph-brand" href="index.html">Peekhole</a>
      <nav class="ph-nav">
        <a href="index.html">Blog home</a>
        <a href="{PEEKHOLE}">Peekhole.com</a>
      </nav>
    </header>
    <main class="ph-blog">
      <header class="ph-blog-header">
        <h2 class="ph-section-title">GTA 6 news from the neon side</h2>
        <p>Short, original Peekhole briefings on Grand Theft Auto VI. Back to <a href="{PEEKHOLE}">peekhole.com</a> any time.</p>
      </header>
{cards_html}
    </main>
    <footer class="ph-site-footer">
      <p>A neon Vice City news desk from <a href="{PEEKHOLE}">Peekhole</a> and Taylor Love 303. Independent coverage — not affiliated with Rockstar Games.</p>
    </footer>
  </div>
</body>
</html>
'''


WIDGET_CSS = """
#peekhole-latest, #peekhole-latest * { box-sizing: border-box; }
#peekhole-latest {
  --ph-bg: #080414;
  --ph-card: #14081f;
  --ph-pink: #ff3cac;
  --ph-cyan: #00e8ff;
  --ph-text: #f6eef9;
  --ph-muted: #b9a8c8;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background:
    radial-gradient(800px 280px at 10% -20%, rgba(255, 60, 172, 0.18), transparent 55%),
    radial-gradient(700px 240px at 110% 0%, rgba(0, 232, 255, 0.12), transparent 50%),
    var(--ph-bg);
  color: var(--ph-text);
  padding: 0.85rem 0.75rem 0.95rem;
  width: 100%;
  max-width: 760px;
  margin: 0 auto;
  max-height: 860px;
  overflow-y: auto;
  -webkit-text-size-adjust: 100%;
}
#peekhole-latest .ph-w-header {
  margin: 0 0 0.75rem;
  padding-bottom: 0.55rem;
  border-bottom: 1px solid rgba(0, 232, 255, 0.25);
}
#peekhole-latest .ph-w-header a {
  font-size: 1rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #fff;
  text-decoration: none;
  text-shadow: 0 0 8px rgba(255, 60, 172, 0.9), 0 0 18px rgba(0, 232, 255, 0.35);
}
#peekhole-latest .ph-w-header p {
  margin: 0.3rem 0 0;
  color: var(--ph-muted);
  font-size: 0.85rem;
}
#peekhole-latest .ph-w-card {
  display: block;
  background: linear-gradient(180deg, rgba(255, 60, 172, 0.1), transparent 40%), var(--ph-card);
  border: 1px solid rgba(255, 60, 172, 0.38);
  border-radius: 14px;
  padding: 0.85rem 0.9rem;
  margin: 0 0 0.7rem;
  color: inherit;
  text-decoration: none;
  box-shadow: 0 0 20px rgba(255, 60, 172, 0.12);
}
#peekhole-latest .ph-w-card:hover,
#peekhole-latest .ph-w-card:focus {
  border-color: var(--ph-cyan);
}
#peekhole-latest .ph-w-card:focus-visible {
  outline: 2px solid var(--ph-cyan);
  outline-offset: 2px;
}
#peekhole-latest .ph-w-date {
  color: var(--ph-cyan);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 0.68rem;
  font-weight: 700;
  margin: 0 0 0.3rem;
}
#peekhole-latest .ph-w-card h3 {
  margin: 0 0 0.35rem;
  font-size: 1.02rem;
  line-height: 1.3;
  color: #fff;
  text-shadow: 0 0 8px rgba(255, 60, 172, 0.85);
}
#peekhole-latest .ph-w-card p {
  margin: 0;
  color: var(--ph-text);
  font-size: 0.9rem;
  line-height: 1.45;
}
#peekhole-latest .ph-w-foot {
  margin: 0.35rem 0 0;
  text-align: center;
}
#peekhole-latest .ph-w-foot a {
  color: var(--ph-cyan);
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-decoration: none;
}
#peekhole-latest .ph-w-foot a:hover,
#peekhole-latest .ph-w-foot a:focus {
  color: var(--ph-pink);
  text-decoration: underline;
}
#peekhole-latest .ph-w-msg {
  margin: 0.4rem 0;
  color: var(--ph-muted);
  font-size: 0.92rem;
}
""".strip()


def widget_cards_html(posts: list[dict], indent: str = "  ") -> str:
    chunks = []
    for p in posts[:MAX_WIDGET_POSTS]:
        chunks.append(
            f'''{indent}<a class="ph-w-card" href="{escape(p["url"], quote=True)}" target="_blank" rel="noopener">
{indent}  <div class="ph-w-date">{escape(p["date_display"])}</div>
{indent}  <h3>{escape(p["title"])}</h3>
{indent}  <p>{escape(p["description"])}</p>
{indent}</a>'''
        )
    return "\n".join(chunks)


def make_latest_js(posts: list[dict]) -> str:
    fallback = []
    for p in posts[:MAX_WIDGET_POSTS]:
        fallback.append(
            {
                "title": p["title"],
                "slug": p["slug"],
                "url": p["url"],
                "date": p["date"],
                "date_display": p["date_display"],
                "description": p["description"],
            }
        )
    fallback_json = json.dumps(fallback, indent=2, ensure_ascii=False)
    css_js = json.dumps(WIDGET_CSS)
    return f'''/* Peekhole latest-posts widget. Fetches {SITE}/posts.json and paints neon cards. */
(function () {{
  var ROOT = {json.dumps(SITE)};
  var FALLBACK_POSTS = {fallback_json};
  var STYLE_ID = "peekhole-latest-css";
  var CSS = {css_js};

  var mount = document.getElementById("peekhole-latest");
  if (!mount) return;

  function injectStyles() {{
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = CSS;
    document.head.appendChild(style);
  }}

  function formatDate(iso) {{
    if (!iso) return "";
    var d = new Date(iso + "T00:00:00");
    if (isNaN(d.getTime())) return iso;
    try {{
      return d.toLocaleDateString("en-US", {{ month: "long", day: "numeric", year: "numeric" }});
    }} catch (e) {{
      return iso;
    }}
  }}

  function esc(s) {{
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }}

  function render(posts) {{
    var list = Array.isArray(posts) ? posts.slice(0, 5) : [];
    var html = '<div class="ph-w-header">';
    html += '<a href="' + ROOT + '/" target="_blank" rel="noopener">Peekhole GTA 6 news</a>';
    html += "<p>Fresh briefings from the neon side of Vice City.</p></div>";
    if (!list.length) {{
      html += '<p class="ph-w-msg">Could not load posts right now.</p>';
      html += '<p class="ph-w-foot"><a href="' + ROOT + '/" target="_blank" rel="noopener">Open the Peekhole blog</a></p>';
      mount.innerHTML = html;
      return;
    }}
    for (var i = 0; i < list.length; i++) {{
      var p = list[i];
      var url = p.url || (ROOT + "/posts/" + p.slug + ".html");
      var when = p.date_display || formatDate(p.date);
      html += '<a class="ph-w-card" href="' + esc(url) + '" target="_blank" rel="noopener">';
      html += '<div class="ph-w-date">' + esc(when) + "</div>";
      html += "<h3>" + esc(p.title) + "</h3>";
      html += "<p>" + esc(p.description) + "</p>";
      html += "</a>";
    }}
    html += '<p class="ph-w-foot"><a href="' + ROOT + '/" target="_blank" rel="noopener">All Peekhole GTA 6 news</a></p>';
    mount.innerHTML = html;
  }}

  injectStyles();
  render(FALLBACK_POSTS);

  try {{
    fetch(ROOT + "/posts.json", {{ credentials: "omit" }})
      .then(function (res) {{
        if (!res.ok) throw new Error("status " + res.status);
        return res.json();
      }})
      .then(function (data) {{
        if (Array.isArray(data) && data.length) render(data);
      }})
      .catch(function () {{
        render(FALLBACK_POSTS);
      }});
  }} catch (e) {{
    render(FALLBACK_POSTS);
  }}
}})();
'''


def make_snippet(posts: list[dict]) -> str:
    cards = widget_cards_html(posts, indent="  ")
    return f'''<!--
  Peekhole latest-posts widget for the bottom of peekhole.com.
  Paste this entire file into a GoDaddy Website Builder HTML section.

  Recommended setting: set Forced Height to 820 pixels.
  (GoDaddy puts this code in a framed box. Auto-height often gets cut off.)

  Wait until blog.peekhole.com opens in a browser before pasting —
  that means the DNS step is finished.

  After this is pasted once, new daily posts show up on their own.
-->
<style>
{WIDGET_CSS}
</style>
<div id="peekhole-latest">
  <div class="ph-w-header">
    <a href="{SITE}/" target="_blank" rel="noopener">Peekhole GTA 6 news</a>
    <p>Fresh briefings from the neon side of Vice City.</p>
  </div>
{cards}
  <p class="ph-w-foot"><a href="{SITE}/" target="_blank" rel="noopener">All Peekhole GTA 6 news</a></p>
</div>
<script src="{SITE}/latest.js" defer></script>
'''


def main() -> None:
    posts = load_posts()
    write(ROOT / "posts.json", make_posts_json(posts))
    write(ROOT / "sitemap.xml", make_sitemap(posts))
    write(ROOT / "index.html", make_index(posts))
    write(ROOT / "latest.js", make_latest_js(posts))
    write(ROOT / "homepage-snippet.html", make_snippet(posts))
    print(f"ok: {len(posts)} post(s)")


if __name__ == "__main__":
    main()
