# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.40] - 2026-03-27

### Added
- Playwright-based component utilities for Appian UI automation
- Support for common Appian components: Buttons, Inputs, Dropdowns, Tables, Tabs, Links, Labels, Search components
- BrowserUtils for multi-tab management
- Comprehensive error handling with MyCustomError exception
- Pytest fixtures for e2e testing with Playwright
- Documentation site with MkDocs Material theme
- Dynamic version management via `ComponentUtils.get_version()`
- Resilience helpers with retry mechanisms (RoboUtils.retry_on_timeout)
- ARIA-compliant XPath selectors with NBSP normalization
- Label-driven API design for readable test code

### Fixed
- Version loading fallback to "0.0.0" if pyproject.toml is unavailable

## [Unreleased]

### Planned
- Additional component utilities
- Enhanced error reporting
- Performance optimizations
- Extended documentation examples

---

## Version Strategy

**Single Source of Truth**: Version is defined only in `pyproject.toml` under `[tool.poetry]` section.

**Dynamic Loading**: The `ComponentUtils.get_version()` method reads the version at runtime, ensuring:
- No version duplication across files
- Automatic version availability in `__version__` exports
- Consistency across package metadata

**Versioning Scheme**: Follows [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Release Process**:
1. Update version in `pyproject.toml`
2. Update this CHANGELOG.md with changes
3. Commit and create a git tag (e.g., `v0.0.40`)
4. CI/CD publishes to PyPI automatically
