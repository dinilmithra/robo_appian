#!/usr/bin/env python3
"""Centralized setup for robo_appian (cross-platform)."""

from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print(f"> {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    # Create .venv at parent workspace level (outside repo folder)
    # Can be overridden via ROBO_APPIAN_VENV_PATH environment variable
    venv_path = os.getenv("ROBO_APPIAN_VENV_PATH")
    if venv_path:
        venv_dir = Path(venv_path).resolve()
    else:
        venv_dir = repo_root.parent / ".venv"

    venv_bin = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    venv_python = venv_bin / ("python.exe" if os.name == "nt" else "python")

    print("======================================")
    print("  Setting up robo_appian development  ")
    print("======================================")
    print()

    if not venv_python.exists():
        print("Creating virtual environment...")
        run([sys.executable, "-m", "venv", str(venv_dir)])
        print(f"Virtual environment created at {venv_dir}")
    else:
        print(f"Virtual environment already exists at {venv_dir}")

    print("\nUpgrading pip...")
    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(venv_python), "-m", "pip", "--version"])

    print("\nInstalling requirements (including Poetry)...")
    run(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "-r",
            str(repo_root / "requirements.txt"),
        ]
    )

    print("\nConfiguring Poetry to use system virtualenv...")
    run([str(venv_python), "-m", "poetry", "config", "virtualenvs.in-project", "false"])

    print("\nInstalling project dependencies with Poetry...")
    run([str(venv_python), "-m", "poetry", "install"])

    print("\nVerifying installation...")
    run([str(venv_python), "-m", "poetry", "show", "--tree"])

    print("\n======================================")
    print("  Setup completed successfully! 🎉   ")
    print("======================================")
    print()
    print("Next steps:")
    print("1. Start developing: poetry run python -m robo_appian")
    print("2. Build docs: poetry run mkdocs serve")
    print("3. Run tests: poetry run pytest (after setting up tests)")


if __name__ == "__main__":
    main()
