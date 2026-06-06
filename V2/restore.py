#!/usr/bin/env python3
# ============================================================
# RESTORE ODYSSEUS FROM GITHUB
# ============================================================
import os
import zipfile
import requests
from pathlib import Path

print("=" * 50)
print("RESTORING ODYSSEUS")
print("=" * 50)

REPO_OWNER = "kimochione"
REPO_NAME = "drvnk-sh1p"
BRANCH = "main"
FOLDER = "V2"
NUM_ZIPS = 13

DEST = Path("/content/odysseus_restored")
TEMP_DIR = Path("/content/odysseus_temp")

DEST.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

print("\n📥 Downloading ZIP files...")

for i in range(1, NUM_ZIPS + 1):
    zip_name = f"odysseus_part_{i:03d}.zip"
    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{FOLDER}/{zip_name}"
    zip_path = TEMP_DIR / zip_name
    
    print(f"   Downloading {zip_name}...")
    response = requests.get(url, stream=True)
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"   Extracting {zip_name}...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(TEMP_DIR)
    zip_path.unlink()

print("\n🔧 Reassembling split files...")

# Reassemble any split files
for split_info in TEMP_DIR.rglob("*.split_info"):
    with open(split_info, 'r') as f:
        lines = f.read().strip().split('\n')
        original = None
        chunks = 0
        for line in lines:
            if line.startswith("original="):
                original = line.split("=")[1]
            elif line.startswith("chunks="):
                chunks = int(line.split("=")[1])
        
        if original and chunks > 0:
            base_path = split_info.parent / original
            base_path.parent.mkdir(parents=True, exist_ok=True)
            with open(base_path, 'wb') as outfile:
                for chunk_num in range(1, chunks + 1):
                    part_file = split_info.parent / f"{split_info.stem}.part{chunk_num:03d}"
                    if part_file.exists():
                        with open(part_file, 'rb') as infile:
                            outfile.write(infile.read())
                        part_file.unlink()
            split_info.unlink()

print("\n📂 Moving files to destination...")

# Move all files from temp to destination
for item in TEMP_DIR.rglob("*"):
    if item.is_file():
        dest_file = DEST / item.relative_to(TEMP_DIR)
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        item.rename(dest_file)

import shutil
shutil.rmtree(TEMP_DIR)

print("\n✅ Restore complete!")
print(f"📂 Odysseus restored to: {DEST}")
