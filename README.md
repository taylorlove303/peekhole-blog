# Peekhole blog

Static GitHub Pages site for daily GTA 6 news, published at [blog.peekhole.com](https://blog.peekhole.com). There is no build step and no GitHub Action. Pages serves the files on the `main` branch.

## Publish a day's posts

1. Add each new article as `posts/<slug>.html`. Give that page its own `<title>`, meta description, canonical URL (`https://blog.peekhole.com/posts/<slug>.html`), Open Graph tags, and JSON-LD `BlogPosting` block. Target one long-tail phrase in the title and description.
2. Add a matching entry at the **top** of `posts-data.json` (newest first) with: `title`, `slug`, `date` (`YYYY-MM-DD`), `date_display`, `description`, `target_phrase`, `kicker`, `keywords`, and `tags`.
3. From this folder, run:

```bash
./publish.sh
```

Or pass the post date so the commit message is exact:

```bash
./publish.sh 2026-11-12
```

`publish.sh` rebuilds `index.html`, `posts.json`, `sitemap.xml`, `latest.js`, and `homepage-snippet.html`, commits with the message `Daily posts YYYY-MM-DD`, and pushes to `main`. GitHub Pages updates on its own a minute or two later.

Use `./publish.sh --no-push` to commit without pushing.

Rotate long-tail phrases so the same one does not appear on back-to-back days: `peekhole GTA 6 OnlyFans`, `what is peekhole in GTA 6`, `peak hole GTA 6`, `GTA 6 peekhole poster`, `GTA 6 peekhole QR code`, `peekhole Jack of Hearts`. Keep posts original. Do not claim an in-game item exists unless a source says so.

## Brand call to action

Relevant posts end, after the editorial text and sources, with a clearly separate box:

```html
<aside class="ph-cta" aria-label="From Peekhole">
  <span class="ph-cta-label">From Peekhole</span>
  <p>Enjoyed exploring the after-hours side of Vice City? Discover the exclusive world of Peekhole.</p>
  <a class="ph-cta-btn" href="https://peekhole.com/">Visit Peekhole</a>
</aside>
```

Vary the wording to fit the article. Keep it tasteful and non-explicit, and never mix promotion into the article body.

## Homepage snippet

`homepage-snippet.html` is the one-time paste for a GoDaddy Website Builder HTML section at the bottom of peekhole.com. Wait until https://blog.peekhole.com opens in a browser, then paste the snippet and set **Forced Height** to **820** pixels. After that, daily posts appear on their own.

## Custom domain

In GoDaddy DNS, add a CNAME record: **Host** `blog`, **Points to** / **Value** `taylorlove303.github.io`. HTTPS on the custom domain starts working after that DNS record is in place.
