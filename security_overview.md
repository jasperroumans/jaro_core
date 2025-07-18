# GitHub Security Overzicht

Dit project maakt gebruik van meerdere beveiligingsopties van GitHub en OAuth2.

## ✅ Geactiveerde security features
- **Security Policy** (`SECURITY.md`)
- **CodeQL code scanning** (workflow `codeql.yml`)
- **Private Vulnerability Reporting**
- **Secret scanning** (aanbevolen in `SECURITY.md`)

## 📅 Ingesteld op
- 19 juli 2025: Security policy toegevoegd en CodeQL workflow ingeschakeld

## 👤 Beheerder
- E-mail: [security@jaromade.ai](mailto:security@jaromade.ai)

## 🔐 OAuth2 voor Gmail
- Integratie via `ai_modules/gmail_module.py`
- OAuth2 scopes beperkt tot `gmail.send` en `gmail.readonly` zoals beschreven in `docs/security_recommendations.md`

## 🔎 Meer informatie
- [Beveiligingsbeleid](SECURITY.md)
- [CodeQL workflow](.github/workflows/codeql.yml)
