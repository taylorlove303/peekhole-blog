/* Peekhole latest-posts widget. Fetches https://blog.peekhole.com/posts.json and paints neon cards. */
(function () {
  var ROOT = "https://blog.peekhole.com";
  var FALLBACK_POSTS = [
  {
    "title": "How Do You Go to Hell in GTA 6? | Peekhole",
    "slug": "how-do-you-go-to-hell-in-gta-6-peekhole",
    "url": "https://blog.peekhole.com/posts/how-do-you-go-to-hell-in-gta-6-peekhole.html",
    "date": "2026-11-24",
    "date_display": "November 24, 2026",
    "description": "How do you go to Hell in GTA 6? Find the Circles of Hell garage in north Port Gellhorn at night after Chapter 2 starts. Steps, boss tips and rewards."
  },
  {
    "title": "Does GTA 6 Have Websites? | Peekhole",
    "slug": "does-gta-6-have-websites-peekhole",
    "url": "https://blog.peekhole.com/posts/does-gta-6-have-websites-peekhole.html",
    "date": "2026-11-24",
    "date_display": "November 24, 2026",
    "description": "Does GTA 6 have websites? No. Rockstar dropped the fictional internet for phone apps and social feeds. Here's why, in Rockstar's own words."
  },
  {
    "title": "Who Plays Lucia in GTA 6? | Peekhole",
    "slug": "who-plays-lucia-in-gta-6-peekhole",
    "url": "https://blog.peekhole.com/posts/who-plays-lucia-in-gta-6-peekhole.html",
    "date": "2026-11-24",
    "date_display": "November 24, 2026",
    "description": "Who plays Lucia in GTA 6? Manni L. Perez, now up for Best Performance at The Game Awards. Plus who plays Jason, and other big cast names."
  },
  {
    "title": "What Is GTA 6 Update 01.002.002? | Peekhole",
    "slug": "what-is-gta-6-update-01-002-002-peekhole",
    "url": "https://blog.peekhole.com/posts/what-is-gta-6-update-01-002-002-peekhole.html",
    "date": "2026-11-23",
    "date_display": "November 23, 2026",
    "description": "What is GTA 6 update 01.002.002? It's the first patch since launch, out Nov 23 on PS5 and Xbox. Size, rollout waves, and why there are no notes."
  },
  {
    "title": "Can You Play Darts in GTA 6? | Peekhole",
    "slug": "can-you-play-darts-in-gta-6-peekhole",
    "url": "https://blog.peekhole.com/posts/can-you-play-darts-in-gta-6-peekhole.html",
    "date": "2026-11-23",
    "date_display": "November 23, 2026",
    "description": "Can you play darts in GTA 6? No. Rockstar cut darts and bowling. Pool, weightlifting and basketball made it in. Here's why, in Rockstar's words."
  }
];
  var STYLE_ID = "peekhole-latest-css";
  var CSS = "#peekhole-latest, #peekhole-latest * { box-sizing: border-box; }\n#peekhole-latest {\n  --ph-bg: #080414;\n  --ph-card: #14081f;\n  --ph-pink: #ff3cac;\n  --ph-cyan: #00e8ff;\n  --ph-text: #f6eef9;\n  --ph-muted: #b9a8c8;\n  font-family: \"Segoe UI\", Tahoma, Geneva, Verdana, sans-serif;\n  background:\n    radial-gradient(800px 280px at 10% -20%, rgba(255, 60, 172, 0.18), transparent 55%),\n    radial-gradient(700px 240px at 110% 0%, rgba(0, 232, 255, 0.12), transparent 50%),\n    var(--ph-bg);\n  color: var(--ph-text);\n  padding: 0.85rem 0.75rem 0.95rem;\n  width: 100%;\n  max-width: 760px;\n  margin: 0 auto;\n  max-height: 860px;\n  overflow-y: auto;\n  -webkit-text-size-adjust: 100%;\n}\n#peekhole-latest .ph-w-header {\n  margin: 0 0 0.75rem;\n  padding-bottom: 0.55rem;\n  border-bottom: 1px solid rgba(0, 232, 255, 0.25);\n}\n#peekhole-latest .ph-w-header a {\n  font-size: 1rem;\n  letter-spacing: 0.08em;\n  text-transform: uppercase;\n  color: #fff;\n  text-decoration: none;\n  text-shadow: 0 0 8px rgba(255, 60, 172, 0.9), 0 0 18px rgba(0, 232, 255, 0.35);\n}\n#peekhole-latest .ph-w-header p {\n  margin: 0.3rem 0 0;\n  color: var(--ph-muted);\n  font-size: 0.85rem;\n}\n#peekhole-latest .ph-w-card {\n  display: block;\n  background: linear-gradient(180deg, rgba(255, 60, 172, 0.1), transparent 40%), var(--ph-card);\n  border: 1px solid rgba(255, 60, 172, 0.38);\n  border-radius: 14px;\n  padding: 0.85rem 0.9rem;\n  margin: 0 0 0.7rem;\n  color: inherit;\n  text-decoration: none;\n  box-shadow: 0 0 20px rgba(255, 60, 172, 0.12);\n}\n#peekhole-latest .ph-w-card:hover,\n#peekhole-latest .ph-w-card:focus {\n  border-color: var(--ph-cyan);\n}\n#peekhole-latest .ph-w-card:focus-visible {\n  outline: 2px solid var(--ph-cyan);\n  outline-offset: 2px;\n}\n#peekhole-latest .ph-w-date {\n  color: var(--ph-cyan);\n  letter-spacing: 0.12em;\n  text-transform: uppercase;\n  font-size: 0.68rem;\n  font-weight: 700;\n  margin: 0 0 0.3rem;\n}\n#peekhole-latest .ph-w-card h3 {\n  margin: 0 0 0.35rem;\n  font-size: 1.02rem;\n  line-height: 1.3;\n  color: #fff;\n  text-shadow: 0 0 8px rgba(255, 60, 172, 0.85);\n}\n#peekhole-latest .ph-w-card p {\n  margin: 0;\n  color: var(--ph-text);\n  font-size: 0.9rem;\n  line-height: 1.45;\n}\n#peekhole-latest .ph-w-foot {\n  margin: 0.35rem 0 0;\n  text-align: center;\n}\n#peekhole-latest .ph-w-foot a {\n  color: var(--ph-cyan);\n  font-size: 0.85rem;\n  font-weight: 700;\n  letter-spacing: 0.04em;\n  text-transform: uppercase;\n  text-decoration: none;\n}\n#peekhole-latest .ph-w-foot a:hover,\n#peekhole-latest .ph-w-foot a:focus {\n  color: var(--ph-pink);\n  text-decoration: underline;\n}\n#peekhole-latest .ph-w-msg {\n  margin: 0.4rem 0;\n  color: var(--ph-muted);\n  font-size: 0.92rem;\n}";

  var mount = document.getElementById("peekhole-latest");
  if (!mount) return;

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = CSS;
    document.head.appendChild(style);
  }

  function formatDate(iso) {
    if (!iso) return "";
    var d = new Date(iso + "T00:00:00");
    if (isNaN(d.getTime())) return iso;
    try {
      return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
    } catch (e) {
      return iso;
    }
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function render(posts) {
    var list = Array.isArray(posts) ? posts.slice(0, 5) : [];
    var html = '<div class="ph-w-header">';
    html += '<a href="' + ROOT + '/" target="_blank" rel="noopener">Peekhole GTA 6 news</a>';
    html += "<p>Fresh briefings from the neon side of Vice City.</p></div>";
    if (!list.length) {
      html += '<p class="ph-w-msg">Could not load posts right now.</p>';
      html += '<p class="ph-w-foot"><a href="' + ROOT + '/" target="_blank" rel="noopener">Open the Peekhole blog</a></p>';
      mount.innerHTML = html;
      return;
    }
    for (var i = 0; i < list.length; i++) {
      var p = list[i];
      var url = p.url || (ROOT + "/posts/" + p.slug + ".html");
      var when = p.date_display || formatDate(p.date);
      html += '<a class="ph-w-card" href="' + esc(url) + '" target="_blank" rel="noopener">';
      html += '<div class="ph-w-date">' + esc(when) + "</div>";
      html += "<h3>" + esc(p.title) + "</h3>";
      html += "<p>" + esc(p.description) + "</p>";
      html += "</a>";
    }
    html += '<p class="ph-w-foot"><a href="' + ROOT + '/" target="_blank" rel="noopener">All Peekhole GTA 6 news</a></p>';
    mount.innerHTML = html;
  }

  injectStyles();
  render(FALLBACK_POSTS);

  try {
    fetch(ROOT + "/posts.json", { credentials: "omit" })
      .then(function (res) {
        if (!res.ok) throw new Error("status " + res.status);
        return res.json();
      })
      .then(function (data) {
        if (Array.isArray(data) && data.length) render(data);
      })
      .catch(function () {
        render(FALLBACK_POSTS);
      });
  } catch (e) {
    render(FALLBACK_POSTS);
  }
})();
