# OAuth2 Veiligheidsadvies

- Gebruik alleen OAuth2 scopes die strikt noodzakelijk zijn (`gmail.send`, `gmail.readonly`).
- Beperk tokenlevensduur via Google Cloud Console.
- Sla tokens nooit hardcoded op in Python-scripts.
- Zet `GOOGLE_CREDENTIALS_PATH` in `.env` en gebruik `.gitignore`.
- Beperk toegang tot credentials via chmod 600.
- Activeer alerts bij verdachte login-activiteit.

Gebruik de integriteitscheck (`tools/system_diagnostics.py`) regelmatig als healthcheck.
Sla wekelijkse CodeQL scanresultaten op via `tools/codeql_integrity_log.py` voor een integriteitslog.
