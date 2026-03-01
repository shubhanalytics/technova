# Technova — Discover tech at a glance

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://shubhanalytics.github.io/technova/)
[![Resources](https://img.shields.io/badge/resources-2%2C200%2B-blue)]()
[![Categories](https://img.shields.io/badge/categories-50-purple)]()

A lightweight, privacy-focused directory for discovering technology tools, frameworks, programming languages, and developer resources.

**Live demo:** https://shubhanalytics.github.io/technova/

## Features

- **2,200+ Resources** across 50 categories
- **Fast Search** — instant filtering as you type
- **Privacy-First** — no tracking, no cookies, no analytics
- **Accessible** — keyboard navigation, screen reader support
- **Mobile-Friendly** — responsive design for all devices
- **Open Source** — community-maintained, MIT license

## Categories

| Development | Data & AI | Infrastructure | Business |
|-------------|-----------|----------------|----------|
| Programming Languages | AI/ML | Cloud | Business Tools |
| Libraries | Data Science | Hosting | Payment |
| Frontend | Data Engineering | Container | Email |
| Backend | Database | DevOps | Collaboration |
| Testing | Analytics | Security | Design |

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/shubhanalytics/technova.git
cd technova
```

2. Start a local server:
```bash
# Python 3
python -m http.server 8000

# Then open http://localhost:8000
```

## Project Structure

```
technova/
├── index.html          # Main application
├── about.html          # About page
├── community.html      # Community page
├── contribute.html     # Contribution form
├── styles.css          # Stylesheet
├── app.js              # Application logic
├── data.json           # Resource database
└── scripts/            # Utility scripts
```

## Contributing

We welcome contributions! To add a new resource:

1. Visit the [Contribute page](https://shubhanalytics.github.io/technova/contribute.html)
2. Fill out the form with the tool details
3. Submit for review

Or create a pull request with changes to `data.json`.

## Tech Stack

- **Frontend:** Vanilla JavaScript, CSS3, HTML5
- **Fonts:** Inter, Poppins (Google Fonts)
- **Hosting:** GitHub Pages
- **No dependencies** — pure static site

## Security

- Content Security Policy (CSP) headers
- URL sanitization for all external links
- XSS protection via HTML escaping
- No external tracking scripts

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ by the community
