import sys
import shutil
from pathlib import Path


def create_project(name: str):
    target = Path.cwd() / name
    template = Path(__file__).parent / "template"

    if target.exists():
        print("❌ Folder already exists")
        sys.exit(1)

    shutil.copytree(template, target)
    print(f"✅ Project '{name}' created successfully")


def main():
    if len(sys.argv) < 3:
        print("Usage: fastapi-fusion create <project_name>")
        sys.exit(1)

    command = sys.argv[1]
    name = sys.argv[2]

    if command == "create":
        create_project(name)
    else:
        print("Unknown command")