# Code Style Rules

- Python 3.11, conda environment: life-assistant
- All file I/O through core/file_handler.py only
- No hardcoded paths – use pathlib throughout
- Functions max 30 lines, single responsibility
- All agent functions return dict with keys: success, message, data
- Error handling: catch specific exceptions, never bare except
- No print() – use logging module
