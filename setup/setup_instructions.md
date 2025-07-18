# Setup Instructions

These steps help you install **jaro_core** on macOS, Windows and Linux. They also
cover Codex integration for syncing the project with GPT memory `jasper_vonk_core`.

## Requirements
- Python 3.11+
- pip

## Installation
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.template` to `.env` and fill in your credentials.

## Codex integration
Run the sync script to push repository contents to GPT memory:
```bash
python tools/sync_codex_memory.py
```

This will update the memory store `jasper_vonk_core` with relevant files.

## Platform notes
- **macOS/Linux**: Use the terminal commands above.
- **Windows**: Use PowerShell or `cmd` with the same commands. Ensure Python is
  added to your PATH.
