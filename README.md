**Python Mini Projects — Audio Analyzer & File Renamer**

This repository contains two small utilities for working with audio files:

- `audio-analyzer`: scans a folder of audio files and generates a CSV report (`audio_report.csv`) containing file name, extension, size (KB), and duration (for `.wav`).
- `audio-file-renamer`: batch renames audio files with a consistent naming pattern and provides a dry-run mode and logging.

**Requirements**
- **Python**: 3.8+ (the workspace has been used with Python 3.11). No external packages are required — both scripts use the standard library.

**Repository Layout**
- `audio-analyzer/` — contains `audio_analyzer.py` and an example `audio_report.csv`.
- `audio-file-renamer/` — contains `rename_audio_files.py`, `rename_audio_files_with_args.py`, and `config.py`.
- `Speaker_0000/` — example audio folder (if present in your workspace).

**Quick Setup (macOS / zsh)**
- Optional: create and activate a virtual environment:

```zsh
python3 -m venv .venv
source .venv/bin/activate
```

- No pip installs required for the current scripts. If you add external libraries later, collect them in `requirements.txt`.

**Usage: Audio Analyzer**
- Purpose: generate `audio_report.csv` summarizing audio files in a folder. The analyzer uses the built-in `wave` module to compute duration for `.wav` files only.

- Run from the repository root (example):

```zsh
python audio-analyzer/audio_analyzer.py --input_dir Speaker_0000 --report_file audio_report.csv
```

- Notes:
  - The default input folder is `audio-analyzer/input_audio` if you run the script from inside the `audio-analyzer` directory.
  - `--report_file` controls where the CSV is written; by default it writes `audio_report.csv` in the current working directory.
  - The script looks for files with extensions `{.wav, .mp3, .flac, .ogg, .m4a}` but duration is only calculated for `.wav` files.

**Usage: Audio File Renamer (simple config)**
- The simple renamer reads configuration from `audio-file-renamer/config.py`.

- Edit `audio-file-renamer/config.py` to set:
  - `INPUT_DIR` — folder containing audio files to rename
  - `PREFIX` — the prefix for renamed files (e.g. `speaker`)
  - `START_INDEX` — starting index (integer)
  - `DRY_RUN` — `True` to preview only (no changes), `False` to apply

- Run the renamer:

```zsh
python audio-file-renamer/rename_audio_files.py
```

**Usage: Audio File Renamer (CLI, safer / production)**
- `rename_audio_files_with_args.py` supports command-line arguments, dry-run vs apply, and generates a mapping CSV and log.

- Example dry-run (preview):

```zsh
python audio-file-renamer/rename_audio_files_with_args.py --prefix speaker1 --input input_audio --start 1
```

- Example apply (actually rename files):

```zsh
python audio-file-renamer/rename_audio_files_with_args.py --prefix speaker1 --input input_audio --start 1 --apply
```

- Output produced by this script:
  - `rename_log.txt` — append-only log of operations
  - `rename_mapping.csv` — CSV mapping of old_name -> new_name

**Files of Interest**
- `audio-analyzer/audio_analyzer.py` — main analyzer script.
- `audio-file-renamer/config.py` — quick configuration for the simple renamer.
- `audio-file-renamer/rename_audio_files_with_args.py` — CLI-enabled renamer (preferred for controlled runs).

**Safety Tips**
- Always run with dry-run first (`DRY_RUN = True` or omit `--apply`) to confirm the planned renames.
- Keep backups of original files if they are important.

**Next Steps / Suggestions**
- Add a `requirements.txt` if you install external libraries (e.g., `pydub`, `librosa`).
- Improve `audio_analyzer.py` to compute durations for formats other than `.wav` using `pydub` or `mutagen` if needed.

If you want, I can:
- create a `requirements.txt` and a small test dataset, or
- run the analyzer/renamer on a sample folder and show the output.

---
File created: `README.md` (root of repository)
