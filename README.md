# laroccod.github.io

Personal portfolio of **Daniel La Rocco** — physics Ph.D. (UC Irvine, 2026),
scientific software developer.

**Live site:** https://laroccod.github.io

Built with [Flet](https://flet.dev) (Python → static Pyodide/WASM build),
styled with the "instrument" theme from my
[labforge](https://github.com/laroccod/labforge) framework, and deployed to
GitHub Pages via GitHub Actions.

## Develop

```bash
pip install flet[all]==0.86.0
flet run src/main.py                       # desktop preview
flet build web --route-url-strategy hash   # static build → build/web
```
