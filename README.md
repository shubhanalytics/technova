# technova — simple static directory

Live demo: https://shubhanalytics.github.io/technova/

This is a minimal static site for the "technova" directory: a searchable, sortable list of programming languages, tools, frameworks, and startups.

Quick start

1. Open `index.html` in your browser. (Modern browsers disallow `fetch` from `file://` in some setups.)
2. Or run a simple local server from the project folder:

```bash
# Python 3
python -m http.server 8000

# then open http://localhost:8000
```

Files

- `index.html` — main UI
- `styles.css` — styles
- `app.js` — logic (loads `data.json`)
- `data.json` — sample data (edit to add entries)

Next steps (optional):

- Add a small admin UI to add items (if you want persistence, add a backend and DB).
- Add categories/sectors/states as you expand the dataset.
