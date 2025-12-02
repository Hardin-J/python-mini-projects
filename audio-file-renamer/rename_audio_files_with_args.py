"""
Audio File Batch Renamer - Production Version (Day 2 Pro)

Features:
- Skips already-renamed files
- Supports CLI arguments
- Supports dry-run and apply modes
- Logs all operations
"""

import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import List
import csv



# ---------- CONSTANTS ----------
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
DEFAULT_INPUT_DIR = Path("input_audio")
LOG_FILE = "rename_log.txt"
MAPPING_FILE = "rename_mapping.csv"



# ---------- HELPER FUNCTIONS ----------

def log(message: str) -> None:
    """
    Writes a log message to both console and log file with timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{timestamp} | {message}"

    print(full_message)

    with open(LOG_FILE, "a") as f:
        f.write(full_message + "\n")


def get_audio_files(directory: Path) -> List[Path]:
    """
    Returns sorted list of valid audio files from a folder.
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    files = [f for f in directory.iterdir() if f.is_file()]
    audio_files = [f for f in files if f.suffix.lower() in AUDIO_EXTENSIONS]

    return sorted(audio_files)


def is_already_renamed(file_path: Path, prefix: str) -> bool:
    """
    Checks if file already follows the naming pattern: <prefix>_001.wav
    """
    return file_path.name.startswith(prefix + "_")


def build_new_name(prefix: str, index: int, extension: str) -> str:
    """
    Builds standardized filename like: speaker1_001.wav
    """
    return f"{prefix}_{index:03d}{extension}"


# ---------- MAIN LOGIC ----------

def rename_files(input_dir: Path, prefix: str, start_index: int, apply: bool):
    """
    Main renaming workflow.
    """
    try:
        audio_files = get_audio_files(input_dir)
    except FileNotFoundError as e:
        log(str(e))
        return

    if not audio_files:
        log("No audio files found. Exiting.")
        return

    log(f"Found {len(audio_files)} audio files in {input_dir}")

    current_index = start_index

    # Open mapping CSV once, write header
    with open(MAPPING_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["old_name", "new_name"])

        for file_path in audio_files:

            # Skip already renamed files
            if is_already_renamed(file_path, prefix):
                log(f"SKIPPED (already renamed): {file_path.name}")
                continue

            extension = file_path.suffix.lower()
            new_name = build_new_name(prefix, current_index, extension)
            new_path = file_path.with_name(new_name)

            if apply:
                os.rename(file_path, new_path)
                log(f"RENAMED: {file_path.name} -> {new_name}")
            else:
                log(f"DRY RUN: {file_path.name} -> {new_name}")

            # Write mapping row (even in dry-run, it's okay as a preview)
            writer.writerow([file_path.name, new_name])

            current_index += 1

        log("Renaming process completed.")


# ---------- CLI ARGUMENT HANDLING ----------

def parse_arguments():
    """
    Handles command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Audio File Batch Renamer")

    parser.add_argument(
        "--input","-i",
        type=str,
        default=str(DEFAULT_INPUT_DIR),
        help="Input folder containing audio files"
    )

    parser.add_argument(
        "--prefix","-p",
        type=str,
        required=True,
        help="Prefix for renamed files (e.g., speaker1)"
    )

    parser.add_argument(
        "--start","-s",
        type=int,
        default=1,
        help="Start index for renaming (default = 1)"
    )

    parser.add_argument(
        "--apply","-a",
        action="store_true",
        help="Actually apply renaming (otherwise dry-run)"
    )

    return parser.parse_args()


# ---------- ENTRY POINT ----------

if __name__ == "__main__":
    args = parse_arguments()

    input_dir = Path(args.input)
    prefix = args.prefix
    start_index = args.start
    apply = args.apply  # False = dry run, True = real rename

    rename_files(input_dir, prefix, start_index, apply)
