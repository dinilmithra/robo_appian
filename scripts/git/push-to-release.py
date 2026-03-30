#!/usr/bin/env python3
"""
Push changes to playwright_release branch.
This script manages merging and pushing code to the playwright_release branch.
"""

import argparse
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    CYAN = "\033[0;36m"
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    RESET = "\033[0m"


def write_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.CYAN}=== {text} ==={Colors.RESET}")


def write_success(text: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def write_error(text: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def write_info(text: str) -> None:
    """Print an info message."""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")


def run_git_command(args: list[str], capture_output: bool = False) -> str | None:
    """Run a git command and return output if requested."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=capture_output,
            text=True,
            check=False
        )
        if capture_output:
            return result.stdout.strip()
        return None
    except FileNotFoundError:
        write_error("Git is not installed or not in PATH")
        sys.exit(1)


def main() -> None:
    """Main script execution."""
    parser = argparse.ArgumentParser(
        description="Push changes to playwright_release branch"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip test validation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without pushing"
    )
    parser.add_argument(
        "-m", "--message",
        default="Update playwright_release branch",
        help="Commit message (currently unused, reserved for future use)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force push (overwrites remote branch) - use with caution"
    )

    args = parser.parse_args()

    # Get repo root (3 levels up from this script: scripts/git/push-to-release.py)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent
    
    # Change to repo root
    import os
    os.chdir(repo_root)

    write_header("Playwright Release Push Script")
    print(f"Working directory: {repo_root}")

    # Check git status
    git_status = run_git_command(["status", "--porcelain"], capture_output=True)
    if git_status:
        write_error("Working directory has uncommitted changes:")
        print(git_status)
        print(f"\n{Colors.YELLOW}Please commit or stash changes before pushing to release.{Colors.RESET}")
        sys.exit(1)
    write_success("Working tree is clean")

    # Get current branch
    current_branch = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], capture_output=True)
    write_info(f"Current branch: {current_branch}")

    # Verify playwright_release branch exists
    branches = run_git_command(["branch", "-a"], capture_output=True)
    if "playwright_release" not in branches:
        write_error("Branch 'playwright_release' not found locally or remotely")
        write_info("Available branches:")
        run_git_command(["branch", "-a"])
        sys.exit(1)
    write_success("playwright_release branch exists")

    # Show what will be pushed
    write_header("Changes to push")
    commits = run_git_command(
        ["log", "origin/playwright_release..HEAD", "--oneline"],
        capture_output=True
    )
    if commits:
        print(commits)
    else:
        write_info(f"No new commits to push from {current_branch} to playwright_release")

    # Confirm action
    print()
    if args.force:
        write_info("⚠️  FORCE PUSH enabled - will overwrite remote branch")
    if args.dry_run:
        write_info(f"[DRY RUN] Would push from {current_branch} to playwright_release")
    else:
        confirm = input("Continue with push? (yes/no) ").strip().lower()
        if confirm not in ("yes", "y"):
            write_info("Push cancelled")
            sys.exit(0)

    # Run tests if not skipped
    if not args.skip_tests:
        write_header("Running tests")
        # Uncomment if tests are configured:
        # result = subprocess.run(["poetry", "run", "pytest", "tests/", "-v"], check=False)
        # if result.returncode != 0:
        #     write_error("Tests failed")
        #     sys.exit(1)
        # write_success("Tests passed")

    # Push current branch to playwright_release
    write_header("Pushing to playwright_release")
    push_opts = ["push"]
    if args.dry_run:
        push_opts.append("--dry-run")
    if args.force:
        push_opts.append("--force-with-lease")
    push_opts.extend(["origin", f"{current_branch}:playwright_release"])
    
    if args.dry_run:
        write_info("[DRY RUN MODE]")
        run_git_command(push_opts)
        write_success("Dry run completed")
    else:
        result = subprocess.run(
            ["git"] + push_opts,
            check=False
        )
        if result.returncode == 0:
            write_success("Successfully pushed to playwright_release")
            print()
            write_info("Release branch updated!")
            run_git_command(["log", "origin/playwright_release", "-1", "--format=%h - %s (%an)"])
        else:
            write_error("Push failed")
            sys.exit(1)

    print()


if __name__ == "__main__":
    main()
