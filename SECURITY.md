## Security policies and checks

This project includes a lightweight security checklist and automated checks run on push to `main`.

What we check automatically:
- `scripts/security_checks.py` validates `data.json` for unsafe URL schemes (no `javascript:` or `data:`) and checks for suspicious `<` characters in names/descriptions.
- A GitHub Action (`.github/workflows/predeploy.yml`) runs these checks and the Python tests.

Before public deployment (recommended):
- Enable HTTPS and HSTS for your hosting.
- Configure server response headers: Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Strict-Transport-Security.
- Avoid including user-supplied HTML; render only sanitized text; do not use `innerHTML`.
- Review any external resources (fonts, analytics) and add them explicitly to CSP.
- Scan third-party dependencies and scripts for vulnerabilities.

If you find a security issue, please report it to the repository owner.
