# dmsAIR-docs

Public documentation for [**dmsAIR**](https://github.com/HERMES-AEROSPACE/dmsAIR) — the HERMES Aerospace group's Direct Molecular Simulation code for hypersonic-flow chemistry.

Published site: **https://hermes-aerospace.github.io/dmsAIR-docs/**

The dmsAIR source code itself lives in a separate, private repository; this repo contains only the user-facing Sphinx documentation.

## Build locally

```bash
pip install -r requirements.txt
make html
open _build/html/index.html
```

## How it's deployed

On every push to `main`, `.github/workflows/pages.yml` builds the site with Sphinx and publishes to GitHub Pages. No cross-repo tokens or deploy keys are involved — the built-in `GITHUB_TOKEN` with `pages: write` permission handles everything.

## License

MIT — see [LICENSE](LICENSE).
