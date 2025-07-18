# Installatie-instructies

Volg deze stappen om **jaro_core** te installeren en te gebruiken. De handleiding werkt op macOS, Windows en Linux.

## Vereisten
- ✅ Python 3.9 of hoger
- ✅ [VSCode](https://code.visualstudio.com/)
- ✅ pip

## Installatie
1. 📂 Clone of download deze repository.
2. Maak een virtuele omgeving aan en activeer deze.
3. Installeer de dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Kopieer `.env.template` naar `.env` en vul je sleutels in.

## Dashboard starten
Start het dashboard met:
```bash
python interface/dashboard_cli.py
```

## Codex synchronisatie
💡 Synchroniseer de repository naar Codex-geheugen met:
```bash
python tools/sync_repo_to_memory.py
```
Dit script verstuurt de relevante bestanden naar het geheugenprofiel.
