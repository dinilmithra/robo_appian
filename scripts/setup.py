#!/usr/bin/env python3
"""Centralized setup for robo_appian (cross-platform)."""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path
from shutil import which
from typing import NoReturn, Optional
from urllib.request import urlopen

HEADER = "=" * 38
POETRY_INSTALLER_URL = "https://install.python-poetry.org"
INSTALLER_TIMEOUT_SECONDS = 30


def run(
    cmd: list[str], *, cwd: Optional[Path] = None, env: Optional[dict[str, str]] = None
) -> None:
    rendered_cmd = shlex.join(cmd)
    if cwd:
        print(f"> (cd {cwd}) {rendered_cmd}")
    else:
        print(f"> {rendered_cmd}")
    subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None, env=env)


def fail(message: str, *, code: int = 1) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def resolve_paths(repo_root: Path) -> tuple[Path, Path]:
    venv_override = os.getenv("ROBO_APPIAN_VENV_PATH")
    venv_dir = Path(venv_override).resolve() if venv_override else repo_root / ".venv"
    venv_bin = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    venv_python = venv_bin / ("python.exe" if os.name == "nt" else "python")
    return venv_dir, venv_python


def activate_venv_env(venv_dir: Path, venv_python: Path) -> dict[str, str]:
    venv_env = os.environ.copy()
    venv_env["VIRTUAL_ENV"] = str(venv_dir)
    venv_env["PATH"] = f'{venv_python.parent}{os.pathsep}{venv_env.get("PATH", "")}'
    venv_env["POETRY_VIRTUALENVS_CREATE"] = "false"
    venv_env["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"

    # Activate for this setup.py process as well
    os.environ["VIRTUAL_ENV"] = str(venv_dir)
    os.environ["PATH"] = venv_env["PATH"]
    os.environ["POETRY_VIRTUALENVS_CREATE"] = "false"
    os.environ["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"
    return venv_env


def resolve_poetry_binary() -> Optional[Path]:
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
        fail(
            f"virtual environment creation succeeded but Python was not found: {venv_python}"
        )


def install_with_pip(venv_python: Path, args: list[str]) -> None:
    run([str(venv_python), "-m", "pip", "install", *args])


def ensure_pip(venv_python: Path) -> None:
    try:
        run([str(venv_python), "-m", "pip", "--version"])
        return
    except subprocess.CalledProcessError:
        print(
            "\nPip not found in virtual environment. Bootstrapping pip with ensurepip..."
        )
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


def poetry_cmd(
    poetry_bin: Path,
    *args: str,
    cwd: Optional[Path] = None,
    env: Optional[dict[str, str]] = None,
) -> None:
    run([str(poetry_bin), *args], cwd=cwd, env=env)


def update_poetry(poetry_bin: Path) -> None:
    print("\nUpdating Poetry to the latest stable release...")
    poetry_cmd(poetry_bin, "self", "update", "--no-interaction")


def ensure_supported_python() -> None:
    if sys.version_info < (3, 9):
        fail("Python 3.9 or newer is required to set up robo_appian.")


def main() -> None:
    ensure_supported_python()
    repo_root = Path(__file__).resolve().parent.parent

    print(HEADER)
    print("  Setting up robo_appian development")
    print(HEADER)

    print("\n1) Creating virtual environment inside workspace (.venv)...")
    venv_dir, venv_python = resolve_paths(repo_root)
    ensure_venv(venv_dir, venv_python)

    print("\n2) Activating virtual environment context...")
    venv_env = activate_venv_env(venv_dir, venv_python)
    print(f'Activated VIRTUAL_ENV={venv_env["VIRTUAL_ENV"]}')

    print("\n3) Installing/updating pip and Poetry...")
    ensure_pip(venv_python)
    install_with_pip(venv_python, ["--upgrade", "pip"])
    run([str(venv_python), "-m", "pip", "--version"], env=venv_env)

    poetry_bin = ensure_poetry()
    update_poetry(poetry_bin)
    poetry_cmd(poetry_bin, "--version")

    print(
        "\n4) Regenerating the Poetry lock file and installing project dependencies into .venv..."
    )
    poetry_cmd(
        poetry_bin,
        "lock",
        "--regenerate",
        "--no-interaction",
        cwd=repo_root,
        env=venv_env,
    )
    poetry_cmd(
        poetry_bin,
        "install",
        "--with",
        "dev",
        "--no-interaction",
        cwd=repo_root,
        env=venv_env,
    )

    print("\nVerification (must point to .venv):")
    run([str(venv_python), "-m", "pip", "--version"], env=venv_env)
    run(
        [
            str(venv_python),
            "-c",
            'from importlib.metadata import version; print(f"robo-appian-pr {version("robo-appian-pr")}")',
        ],
        env=venv_env,
    )

    print(f"\n{HEADER}")
    print("  Setup completed successfully")
    print(f"{HEADER}")
    print("\nNext steps:")
    if os.name == "nt":
        print(f"source equivalent: {venv_dir}\\Scripts\\activate")
    else:
        print(f"source {venv_dir}/bin/activate")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        fail(
            f'command failed with exit code {exc.returncode}: {" ".join(exc.cmd)}',
            code=exc.returncode,
        )
