# jaro_core

## 🟢 Starten van de AI-dashboard CLI

Om het AI-controlecentrum van JARO-CORE te starten, gebruik je het volgende script:

```bash
python interface/dashboard_cli.py
```

## Memory utilities

Nieuwe tools zijn toegevoegd voor het beheren van de GPT-geheugenstatus:

- `tools/memory_visualizer.py` genereert een overzicht van de huidige geheugenlog.
- `tools/memory_feedback_loop.py` schrijft verbeteradviezen weg in `data/log_002.json`.

## Overige modules

- `modules/tracker_recovery_module.py` maakt dagelijkse herstelbestanden in JSON en XLSX.
- `modules/task_focus_module.py` biedt een CLI voor het bijhouden van focus/blokkades.
