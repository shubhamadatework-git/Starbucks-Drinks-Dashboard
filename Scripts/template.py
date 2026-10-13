"""Create the repository folder layout (safe to run more than once).

Run from anywhere:  python Scripts/template.py
It never overwrites existing files.
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent

folders = [
    root / "Data",
    root / "Data" / "sample",
    root / "Previews",
    root / "Scripts",
]

# Create each folder. A .gitkeep file lets git commit a folder that is still empty.
for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)
    if not any(folder.iterdir()):
        (folder / ".gitkeep").touch()

# Create the README only if it does not exist yet
readme = root / "README.md"
if not readme.exists():
    readme.touch()
