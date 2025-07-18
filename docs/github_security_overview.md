# GitHub Security Overview

Deze repository maakt gebruik van meerdere beveiligingsfuncties die door GitHub worden aangeboden. Hieronder volgt een overzicht van de belangrijkste features en instellingen.

## Geactiveerde security features

| Feature                         | Status |
|---------------------------------|--------|
| Security advisories             | ✅ Enabled |
| Secret scanning                 | ✅ Enabled |
| Private vulnerability reporting | ✅ Enabled |
| Dependabot alerts               | ✅ Enabled |
| Code scanning (CodeQL)          | ✅ Enabled |

## Ingestelde data en configuratie
- **Laatste config commit:** $(date +%Y-%m-%d)
- **Cron schedule CodeQL:** iedere zaterdag om 23:21
- **Workflow bestand:** [`codeql.yml`](../.github/workflows/codeql.yml)
- **Beveiligingsbeleid:** [`SECURITY.md`](../SECURITY.md)

## Beheerder / contact
- 📧 `security@jaromade.ai`
- 📍 OAuth2 logging en Gmail integratie verloopt via `gmail_module_oauth.py`
