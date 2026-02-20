#!/usr/bin/env python3
"""Centralized setup for robo_appian (cross-platform)."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path
from shutil import which
from urllib.request import urlopen


HEADER = "=" * 38
POETRY_INSTALLER_URL = "https://install.python-poetry.org"
INSTALLER_TIMEOUT_SECONDS = 30


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    rendered_cmd = shlex.join(cmd)
    if cwd:
        print(f"> (cd {cwd}) {rendered_cmd}")
    else:
        print(f"> {rendered_cmd}")
    subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None, env=env)


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_paths(repo_root: Path) -> tuple[Path, Path]:
    venv_override = os.getenv("ROBO_APPIAN_VENV_PATH")
    venv_dir = Path(venv_override).resolve() if venv_override else repo_root / ".venv"
    venv_bin = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    venv_python = venv_bin / ("python.exe" if os.name == "nt" else "python")
    return venv_dir, venv_python


def resolve_poetry_binary() -> Path | None:
    poetry_path = which("poetry")
    if poetry_path:
        return Path(poetry_path)

    candidates = [
        Path.home() / ".local" / "bin" / "poetry",
        Path.home() / "AppData" / "Roaming" / "Python" / "Scripts" / "poetry.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def ensure_venv(venv_dir: Path, venv_python: Path) -> None:
    if venv_python.exists():
        print(f"Virtual environment already exists at {venv_dir}")
        return

    print(f"Creating virtual environment at {venv_dir}...")
    run([sys.executable, "-m", "venv", str(venv_dir)])
    if not venv_python.exists():
        fail(f"virtual environment creation succeeded but Python was not found: {venv_python}")


def install_with_pip(venv_python: Path, args: list[str]) -> None:
    run([str(venv_python), "-m", "pip", "install", *args])


def ensure_pip(venv_python: Path) -> None:
    try:
        run([str(venv_python), "-m", "pip", "--version"])
        return
    except subprocess.CalledProcessError:
        print("\nPip not found in virtual environment. Bootstrapping pip with ensurepip...")
        run([str(venv_python), "-m", "ensurepip", "--upgrade"])


def ensure_poetry() -> Path:
    poetry_bin = resolve_poetry_binary()
    if poetry_bin:
        return poetry_bin

    print("\nPoetry not found. Installing via official installer...")
    with urlopen(POETRY_INSTALLER_URL, timeout=INSTALLER_TIMEOUT_SECONDS) as response:
        installer_script = response.read()

    subprocess.run([sys.executable, "-"], input=installer_script, check=True)

    poetry_bin = resolve_poetry_binary()
    if poetry_bin is None:
        fail(
            "Poetry installer completed but poetry binary was not found. "
            "Ensure ~/.local/bin is on PATH and retry."
        )
    return poetry_bin


def poetry_cmd(poetry_bin: Path, *args: str, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    run([str(poetry_bin), *args], cwd=cwd, env=env)


def update_poetry(poetry_bin: Path) -> None:
    print("\nUpdating Poetry to the latest stable release...")
    poetry_cmd(poetry_bin, "self", "update", "--no-interaction")


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    requirements_path = repo_root / "requirements.txt"
    if not requirements_path.exists():
        fail(f"requirements file not found: {requirements_path}")

    print(HEADER)
    print("  Setting up robo_appian development")
    print(HEADER)

    venv_dir, venv_python = resolve_paths(repo_root)
    ensure_venv(venv_dir, venv_python)
    ensure_pip(venv_python)

    print("\nUpgrading installer tooling...")
    install_with_pip(venv_python, ["--upgrade", "pip", "setuptools", "wheel"])
    run([str(venv_python), "-m", "pip", "--version"])

    poetry_bin = ensure_poetry()
    update_poetry(poetry_bin)
    poetry_cmd(poetry_bin, "--version")

    print("\nInstalling requirements from requirements.txt...")
    install_with_pip(venv_python, ["-r", str(requirements_path)])

    print("\nInstalling project dependencies via Poetry...")
    poetry_env = os.environ.copy()
    poetry_env["POETRY_VIRTUALENVS_CREATE"] = "false"
    poetry_env["VIRTUAL_ENV"] = str(venv_dir)
    poetry_env["PATH"] = f"{venv_python.parent}{os.pathsep}{poetry_env.get('PATH', '')}"
    poetry_cmd(poetry_bin, "install", "--no-interaction", cwd=repo_root, env=poetry_env)

    print("\nVerifying installed dependency graph...")
    poetry_cmd(poetry_bin, "show", "--tree", cwd=repo_root, env=poetry_env)

    print(f"\n{HEADER}")
    print("  Setup completed successfully")
    print(f"{HEADER}")
    print("\nNext steps:")
    if os.name == "nt":
        print(f"0. Activate venv: {venv_dir}\\Scripts\\activate")
    else:
        print(f"0. Activate venv: source {venv_dir}/bin/activate")
    print(f"1. {poetry_bin} run python -m robo_appian")
    print(f"2. {poetry_bin} run mkdocs serve")
    print(f"3. {poetry_bin} run pytest")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        fail(f"command failed with exit code {exc.returncode}: {' '.join(exc.cmd)}", code=exc.returncode)
