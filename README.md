# Robo Appian

[![PyPI version](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://pypi.org/project/robo-appian-pr/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

Robo Appian is a Python library for automated UI testing of Appian applications. It provides user-friendly utilities and best practices to help you write robust, maintainable, and business-focused test automation.

## Features
- Simple, readable API for Appian UI automation
- Utilities for buttons, inputs, dropdowns, tables, tabs, and more
- Playwright-based page-first APIs with direct component utilities
- Data-driven and workflow testing support
- Error handling and debugging helpers
- Designed for both technical and business users

## Documentation
Full documentation, guides, and API reference are available at:

➡️ [Robo Appian Documentation](https://dinilmithra.github.io/robo_appian/)

## Quick Start
1. Install Robo Appian:
   ```bash
   pip install robo-appian-pr
   ```
2. Install browser binaries:
   ```bash
   playwright install
   ```
3. See the [Getting Started Guide](docs/getting-started/installation.md) for setup and your first test.

## Example Usage
```python
from robo_appian import InputUtils, ButtonUtils

# Set value in a text field by label
InputUtils.setValueByLabelText(page, "Username", "testuser")

# Click a button by label
ButtonUtils.clickByLabelText(page, "Sign In")
```

## Project Structure
- `robo_appian/` - Library source code
- `docs/` - Documentation and guides

## Version Management

The version is managed centrally in `pyproject.toml` and automatically loaded at runtime via `ComponentUtils.get_version()`. This ensures:
- Single source of truth for versioning
- No version synchronization issues
- Dynamic version reporting in logs and debug info

Current version: **0.0.1**

See [CHANGELOG.md](CHANGELOG.md) for release history and updates.

## Contributing
Contributions are welcome! Please see the [contributing guidelines](CONTRIBUTING.md) or open an issue to get started.

## License
Apache License 2.0. See [LICENSE](LICENSE) for details.

---

For questions or support, contact [Dinil Mithra](mailto:dinilmithra.mailme@gmail.com) or connect on [LinkedIn](https://www.linkedin.com/in/dinilmithra).
