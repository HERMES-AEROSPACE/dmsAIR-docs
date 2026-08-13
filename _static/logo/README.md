# dmsAIR logo — draft v1

Two SVG files, hand-written and immediately usable in a browser,
Sphinx docs, or a LaTeX `\includegraphics` (via `svg` package).

- **`dmsair_logo_horizontal.svg`** (520 × 160) — wide wordmark with a
  molecular icon on the left. Use in website headers and doc banners.
- **`dmsair_logo_square.svg`** (120 × 120) — square badge with
  rounded-square deep-blue background. Use as favicon, GitHub repo
  avatar, or the corner mark on slides / posters.

## Design rationale

| Element | Visual | Reasoning |
|--------|--------|-----------|
| Bent triatomic icon | 3 circles + 2 bonds | Signals the state-resolved molecular-collision physics that dmsAIR actually computes (O₃ / NO₂ / H₂O style geometry). |
| Two side atoms blue | `#1f3b5a` | Matches the HERMES Aerospace deep blue (shared with the CoarseAIR docs site and PLATO). |
| Central atom amber-red | `#c92a2a` | Hypersonic-heating / shock-layer colour — keeps the "AIR" half of the wordmark visually linked to the icon. |
| Left-side velocity streaks | Three small amber lines | Hint at the DSMC collision event in progress. |
| Sans-serif wordmark | Helvetica Neue fallback | Clean, journal-friendly; renders well at any scale. |
| Tagline "DIRECT MOLECULAR SIMULATION" | Wide-tracked caps | Anchors the acronym without competing with it. |

## Previewing

- **Any browser** — open the SVG file directly.
- **Sphinx** — drop into `docs/online-documentation/_static/` and
  reference as `.. image:: /_static/dmsair_logo_horizontal.svg` in
  `index.rst`, or point the theme option
  `html_logo = "_static/dmsair_logo_horizontal.svg"` at it in
  `conf.py`.
- **Raster export** — one-liner via ImageMagick
  (`convert -density 300 dmsair_logo_horizontal.svg logo.png`)
  or `inkscape --export-type=png --export-dpi=300 logo.svg`.

## Variations to ask for

If you want alternates, possibilities include:

1. **Monochrome** — pure white-on-blue or black-on-white, for
   journal figures and stickers.
2. **Alternate icon** — a pair of colliding molecules (to emphasise
   the DSMC aspect more than the QCT one), or a 4-atom / N₂+N₂
   geometry.
3. **Narrower aspect ratio** — banner-strip version for document
   headers (e.g. 1000 × 160).
4. **Italic / scripted** wordmark for a softer look.
5. **Typography** — match a specific font already used in the
   University of Glasgow / UCI brand guidelines.

Tell me which direction to refine and I'll produce a v2.
