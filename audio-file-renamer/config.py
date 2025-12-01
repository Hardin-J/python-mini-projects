"""
Config file for audio file renamer.

You can change:
- INPUT_DIR: where the original audio files are
- PREFIX: prefix used in new filenames
- START_INDEX: first number to start from
- DRY_RUN: if True, only prints what would happen
"""

from pathlib import Path

# Path to the folder that contains audio files to rename
INPUT_DIR = Path("input_audio")

# Prefix for new file names (e.g., 'speaker', 'datasetA')
PREFIX = "speaker"

# Start counting from this index
START_INDEX = 1

# If True, script will NOT actually rename files, only print planned changes
DRY_RUN = False
