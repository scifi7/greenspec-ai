"""Look and feel for GreenSpec AI: green palette, CSS and small HTML builders.

Palette
  forest #123D2B  header band, headings
  fern   #2E7D4F  buttons, score bars
  moss   #5BA574  accents
  sage   #DCE8D5  tracks, soft panels
  mist   #F2F6EE  page background
  ink    #17301F  body text
  amber  #C99A2E  "Moderate" rating
  clay   #B5543A  "Poor" rating
"""
import html

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Public+Sans:wght@400;500;600&display=swap');

:root {
  --forest:#123D2B; --fern:#2E7D4F; --moss:#5BA574; --sage:#DCE8D5;
  --mist:#F2F6EE; --ink:#17301F; --line:#CFE0C8; --amber:#C99A2E; --clay:#B5543A;
}
.stApp { background: var(--mist); font-family: 'Public Sans', system-ui, sans-serif; color: var(--ink); }
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }
.block-container { max-width: 760px; padding-top: 1.5rem; padding-bottom: 4rem; }

/* Header band */
.gs-hero { background: var(--forest); border-radius: 18px; padding: 2rem 2rem 1.8rem; margin-bottom: 1.4rem; }
.gs-hero-title { font-family: 'Bricolage Grotesque', system-ui, sans-serif; font-weight: 700;
  font-size: 2.7rem; line-height: 1.05; letter-spacing: -0.02em; color: #EAF4E6; margin: 0; }
.gs-hero-sub { color: #B9D3BE; margin-top: .7rem; font-size: 1.05rem; max-width: 34rem; line-height: 1.45; }

/* Form */
[data-testid="stForm"] { background: #FFFFFF; border: 1px solid var(--line); border-radius: 14px; padding: 1.4rem; }
[data-testid="stForm"] label p { font-weight: 600; color: var(--forest); }
[data-testid="stFormSubmitButton"] button { background: var(--fern); color: #FFFFFF; border: 0;
  border-radius: 10px; padding: .6rem 1.5rem; font-weight: 600; }
[data-testid="stFormSubmitButton"] button:hover { background: var(--forest); color: #FFFFFF; }
[data-testid="stFormSubmitButton"] button:focus-visible { outline: 3px solid var(--moss); outline-offset: 2px; }

/* Section headings */
.gs-sec { font-family: 'Bricolage Grotesque', system-ui, sans-serif; font-weight: 600; font-size: 1.45rem;
  color: var(--forest); margin: 2.2rem 0 .8rem; padding-bottom: .4rem; border-bottom: 1px solid var(--line); }

/* Scorecard */
.gs-card { display: flex; gap: 2rem; align-items: center; flex-wrap: wrap; background: #FFFFFF;
  border: 1px solid var(--line); border-radius: 14px; padding: 1.5rem; }
.gs-ring { width: 172px; height: 172px; border-radius: 50%; flex: 0 0 auto; display: grid; place-items: center;
  background: conic-gradient(var(--c) calc(var(--p) * 1%), var(--sage) 0); }
.gs-ring-inner { width: 134px; height: 134px; border-radius: 50%; background: #FFFFFF;
  display: flex; flex-direction: column; align-items: center; justify-content: center; }
.gs-ring-num { font-family: 'Bricolage Grotesque', system-ui, sans-serif; font-weight: 700; font-size: 3rem; line-height: 1; color: var(--forest); }
.gs-ring-den { font-size: .8rem; color: #4D6A57; margin-top: .2rem; }
.gs-side { flex: 1 1 260px; min-width: 240px; }
.gs-prod { font-family: 'Bricolage Grotesque', system-ui, sans-serif; font-weight: 600; font-size: 1.35rem; color: var(--forest); margin: 0; }
.gs-meta { color: #4D6A57; font-size: .92rem; margin: .2rem 0 .8rem; }
.gs-badge { display: inline-block; font-weight: 600; font-size: .9rem; padding: .2rem .8rem; border-radius: 999px; margin-bottom: 1rem; }
.gs-good { background: #DCEFE0; color: #1F5C37; }
.gs-moderate { background: #F6EBC8; color: #6B4E0E; }
.gs-poor { background: #F4DAD2; color: #7A2E18; }

/* Bars */
.gs-bar { margin: .7rem 0; }
.gs-bar-top { display: flex; justify-content: space-between; font-size: .92rem; font-weight: 500; margin-bottom: .3rem; }
.gs-track { height: 12px; background: var(--sage); border-radius: 6px; overflow: hidden; }
.gs-fill { height: 100%; background: var(--fern); border-radius: 6px; }
.gs-note { color: #4D6A57; font-size: .85rem; margin-top: .8rem; }

/* Bordered containers (AI suggestions, regulations) */
[data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--line) !important; border-radius: 14px !important; background: #FFFFFF; }
[data-testid="stExpander"] { border-color: var(--line); border-radius: 12px; background: #FFFFFF; }

@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
</style>
"""


def hero_html():
    return (
        '<div class="gs-hero">'
        '<p class="gs-hero-title">GreenSpec AI</p>'
        '<p class="gs-hero-sub">Check how sustainable your product\'s material is, '
        "and find a greener way to make it.</p>"
        "</div>"
    )


def section_html(title):
    return f'<h3 class="gs-sec">{html.escape(title)}</h3>'


def _rating_class(rating):
    return {"Good": "gs-good", "Moderate": "gs-moderate"}.get(rating, "gs-poor")


def _rating_color(rating):
    return {"Good": "#2E7D4F", "Moderate": "#C99A2E"}.get(rating, "#B5543A")


def _bar(label, value):
    pct = max(0, min(100, value * 10))
    return (
        '<div class="gs-bar"><div class="gs-bar-top">'
        f"<span>{html.escape(label)}</span><span>{value:g} / 10</span></div>"
        f'<div class="gs-track"><div class="gs-fill" style="width:{pct}%"></div></div></div>'
    )


def scorecard_html(product, material, process, country, score, rating, bars):
    """bars is a list of (label, value out of 10), higher always = better."""
    bar_html = "".join(_bar(label, value) for label, value in bars)
    return (
        '<div class="gs-card">'
        f'<div class="gs-ring" style="--p:{score};--c:{_rating_color(rating)}">'
        f'<div class="gs-ring-inner"><span class="gs-ring-num">{score:g}</span>'
        '<span class="gs-ring-den">out of 100</span></div></div>'
        '<div class="gs-side">'
        f'<p class="gs-prod">{html.escape(product)}</p>'
        f'<p class="gs-meta">Material: {html.escape(material)}. '
        f"Process: {html.escape(process)}. Market: {html.escape(country)}.</p>"
        f'<span class="gs-badge {_rating_class(rating)}">{html.escape(rating)}</span>'
        f"{bar_html}"
        '<p class="gs-note">Scores are per 1 kg of material, from approximate typical values. '
        "Higher is always better.</p>"
        "</div></div>"
    )
