"""
Mini Project #2 - Audio Metadata Analyzer

What this script does:
- Scans a given folder for audio files
- Currently focuses on .wav files for duration (using built-in 'wave' module)
- Collects:
  - file name
  - extension
  - file size in KB
  - duration in seconds (for .wav)
- Prints a summary report
- Saves detailed info into 'audio_report.csv'

This is a realistic first step before training a voice model:
"How much data do I actually have?"
"""

import os
import csv
from pathlib import Path
import wave
from contextlib import closing
from argparse import ArgumentParser


# -------- CONFIG --------

# Folder containing audio files
INPUT_DIR = Path("input_audio")

# Output CSV report file
REPORT_FILE = "audio_report.csv"

# Allowed extensions (we may not get duration for all, but we list them)
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}


# -------- HELPER FUNCTIONS --------

def get_file_size_kb(file_path: Path) -> float:
    """
    Returns file size in kilobytes (KB).
    """
    size_bytes = file_path.stat().st_size  # raw size in bytes
    return round(size_bytes / 1024, 2)     # convert to KB with 2 decimal points


def get_wav_duration_seconds(file_path: Path) -> float | None:
    """
    Returns duration of a .wav file in seconds using the built-in wave module.
    If file is not a valid wav, returns None.
    """
    try:
        # closing() ensures file gets closed even if error occurs
        with closing(wave.open(str(file_path), 'r')) as wf:
            frames = wf.getnframes()       # total number of audio frames
            frame_rate = wf.getframerate() # frames per second (sample rate)
            duration = frames / float(frame_rate)
            return round(duration, 2)
    except Exception as e:
        # If not a proper wav file, or corrupted, just return None
        print(f"Could not read duration for {file_path.name}: {e}")
        return None


def scan_audio_files(directory: Path):
    """
    Scans the directory and yields file metadata one by one.

    Yields:
    dict with keys: name, extension, size_kb, duration_sec
    """
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return

    for item in directory.iterdir():
        if not item.is_file():
            continue

        ext = item.suffix.lower()

        # Ignore non-audio files
        if ext not in AUDIO_EXTENSIONS:
            continue

        size_kb = get_file_size_kb(item)

        # For now, only .wav duration is supported
        duration_sec = None
        if ext == ".wav":
            duration_sec = get_wav_duration_seconds(item)

        yield {
            "name": item.name,
            "extension": ext,
            "size_kb": size_kb,
            "duration_sec": duration_sec
        }

def arg_parser():
    """
    Placeholder for future argument parsing.
    Currently not implemented.
    """
    parser = ArgumentParser(description="Audio Metadata Analyzer")

    parser.add_argument(
        "--input_dir",
        type=str,
        default=str(INPUT_DIR),
        help="Directory containing audio files to analyze"
    )

    parser.add_argument(
        "--report_file",
        type=str,
        default=REPORT_FILE,
        help="Output CSV report file"
    )

    return parser.parse_args()



# -------- MAIN FUNCTION --------

def generate_report():
    """
    Main function to generate audio report.
    - Scans files
    - Prints summary
    - Writes CSV report
    """
    print(f"Scanning audio files in: {INPUT_DIR}")

    audio_entries = list(scan_audio_files(INPUT_DIR))

    if not audio_entries:
        print("No audio files found.")
        return

    # Write to CSV
    with open(REPORT_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "extension", "size_kb", "duration_sec"])

        for entry in audio_entries:
            writer.writerow([
                entry["name"],
                entry["extension"],
                entry["size_kb"],
                entry["duration_sec"]
            ])

    # Summary stats
    total_files = len(audio_entries)
    total_size_kb = sum(e["size_kb"] for e in audio_entries)

    # Only sum durations that are not None
    total_duration_sec = sum(
        e["duration_sec"] for e in audio_entries
        if e["duration_sec"] is not None
    )

    print("\n--- AUDIO REPORT SUMMARY ---")
    print(f"Total audio files: {total_files}")
    print(f"Total size: {round(total_size_kb, 2)} KB")

    # Some files may not have duration (non-wav or errors)
    if total_duration_sec > 0:
        print(f"Total duration (wav only): {round(total_duration_sec, 2)} seconds")
        print(f"Total duration (minutes): {round(total_duration_sec / 60, 2)} minutes")
    else:
        print("No valid wav durations calculated.")

    print(f"\nDetailed report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    args = arg_parser()

    INPUT_DIR = Path(args.input_dir)
    REPORT_FILE = args.report_file
    
    generate_report()
