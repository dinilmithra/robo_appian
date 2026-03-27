# Version Management

This document explains how version management works in Robo Appian and the recommended approach for maintaining consistency.

## Overview

Robo Appian uses a **single source of truth** approach for version management:
- Version is defined **only** in [`pyproject.toml`](../pyproject.toml)
- Version is loaded **dynamically** at runtime via `ComponentUtils.get_version()`
- No manual syncing required across multiple files

## Why This Approach?

✅ **Benefits:**
- **DRY Principle**: No version duplication (one place to update)
- **No Sync Issues**: Impossible to have mismatched versions
- **Runtime Awareness**: Version available in logs and debugging
- **Clean Builds**: Wheel/sdist automatically pick up the correct version
- **Zero Dependencies**: Uses only `tomli` (already required for parsing)

## How It Works

### 1. Version Definition

Update version in `pyproject.toml`:
```toml
[tool.poetry]
name = "robo_appian"
version = "0.0.41"  # Update here only
```

### 2. Dynamic Loading

The version is loaded at runtime:
```python
# robo_appian/__init__.py
__version__ = ComponentUtils.get_version()  # Reads from pyproject.toml
```

### 3. Runtime Access

Access version anywhere in your application:
```python
from robo_appian import __version__

print(f"Using Robo Appian v{__version__}")
```

## Implementation Details

The `ComponentUtils.get_version()` method:
- Reads `pyproject.toml` from the package root
- Parses the TOML structure to extract `tool.poetry.version`
- Returns the version string or `"0.0.0"` as fallback

```python
@staticmethod
def get_version():
    try:
        toml_path = Path(__file__).parents[2] / "pyproject.toml"
        with open(toml_path, "rb") as handle:
            data = tomllib.load(handle)
            return data.get("tool", {}).get("poetry", {}).get("version", "0.0.0")
    except Exception:
        return "0.0.0"
```

## Release Process

To release a new version:

### 1. Update Version in `pyproject.toml`
```bash
# Choose version number following Semantic Versioning
# MAJOR.MINOR.PATCH
# Example: 0.0.40 → 0.0.41 (patch), 0.1.0 (minor), 1.0.0 (major)
```

### 2. Update CHANGELOG.md
```markdown
## [0.0.41] - 2026-03-28

### Added
- Description of new features

### Fixed
- Description of bug fixes
```

### 3. Commit and Tag
```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Release v0.0.41"
git tag -a v0.0.41 -m "Version 0.0.41"
git push origin --tags
```

### 4. Build and Publish
```bash
poetry build  # Creates wheel and sdist in dist/
twine upload dist/*  # Publishes to PyPI
```

## Notes for Developers

- ✅ **Do**: Update only `pyproject.toml` for version changes
- ❌ **Don't**: Manually edit `__version__` in `__init__.py` files
- ✅ **Do**: Keep `CHANGELOG.md` updated with each release
- ✅ **Do**: Use semantic versioning for clarity
- ✅ **Do**: Reference the version in README and docs badges

## External References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
