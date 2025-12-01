"""
Audio File Batch Renamer - Mini Project

Goal:
- Iterate through all audio files in a folder
- Clean and rename them with a consistent naming pattern
- Example: speaker1_001.wav, speaker1_002.mp3, etc.
"""

import os
from pathlib import Path
from typing import List
from config import INPUT_DIR, PREFIX, START_INDEX, DRY_RUN


# Allowed audio file extensions
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}


def get_audio_files(directory: Path) -> List[Path]:
    """
    Returns a list of audio files from the given directory.

    directory: Path object representing the audio folder
    """
    # .iterdir() gives you all items inside the folder
    files = [f for f in directory.iterdir() if f.is_file()]

    # Filter only files whose extension is in AUDIO_EXTENSIONS
    audio_files = [f for f in files if f.suffix.lower() in AUDIO_EXTENSIONS]

    return sorted(audio_files)  # sort for consistent order


def build_new_name(index: int, extension: str) -> str:
    """
    Builds a new filename using the prefix and index.

    Example:
    index=1, extension='.wav' -> 'speaker1_001.wav'
    """
    # :03d means pad number with zeros to 3 digits (001, 002, 010, 100...)
    return f"{PREFIX}_{index:03d}{extension}"


def rename_files():
    """
    Main function that performs the renaming logic.
    """
    # Ensure input directory exists
    if not INPUT_DIR.exists():
        print(f"Input directory not found: {INPUT_DIR}")
        return

    audio_files = get_audio_files(INPUT_DIR)

    if not audio_files:
        print(f"No audio files found in: {INPUT_DIR}")
        return

    print(f"Found {len(audio_files)} audio files in '{INPUT_DIR}':")
    for f in audio_files:
        print(" -", f.name)

    print("\nDRY_RUN is", DRY_RUN)
    if DRY_RUN:
        print("No actual renaming will happen. This is a preview.\n")
    else:
        print("Files WILL be renamed. Proceeding...\n")

    current_index = START_INDEX

    for file_path in audio_files:
        # file_path.suffix gives.extension like '.wav'
        extension = file_path.suffix.lower()
        new_name = build_new_name(current_index, extension)

        # full new path in same directory
        new_path = file_path.with_name(new_name)

        # Print what will happen
        print(f"Renaming: {file_path.name} -> {new_name}")

        if not DRY_RUN:
            # os.rename actually changes file name
            os.rename(file_path, new_path)

        current_index += 1

    print("\nDone. If DRY_RUN was True, no changes were made.")


if __name__ == "__main__":
    rename_files()