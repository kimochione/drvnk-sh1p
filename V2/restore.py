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
NUM_ZIPS = 7

DEST = Path("/content/odysseus_restored")
DEST.mkdir(parents=True, exist_ok=True)

for i in range(1, NUM_ZIPS + 1):
    zip_name = f"odysseus_part_{i:03d}.zip"
    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/{FOLDER}/{zip_name}"
    zip_path = DEST / zip_name
    print(f"Downloading {zip_name}...")
    
    response = requests.get(url, stream=True)
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"   Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(DEST)
    zip_path.unlink()

print("✅ Restore complete!")
print(f"📂 Restored to: {DEST}")
