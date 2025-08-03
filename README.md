# Robo Appian

Robo Appian is a Python library for automated UI testing of Appian applications. It provides user-friendly utilities and best practices to help you write robust, maintainable, and business-focused test automation.

## Features
- Simple, readable API for Appian UI automation
- Utilities for buttons, inputs, dropdowns, tables, tabs, and more
- Data-driven and workflow testing support
- Error handling and debugging helpers
- Designed for both technical and business users

## Documentation
Full documentation, guides, and API reference are available at:

➡️ [Robo Appian Documentation](https://dinilmithra.github.io/robo_appian/)

## Quick Start
1. Install Robo Appian:
   ```bash
   pip install robo_appian
   ```
2. See the [Getting Started Guide](docs/getting-started/installation.md) for setup and your first test.

## Example Usage
```python
from robo_appian.components import InputUtils, ButtonUtils

# Set value in a text field by label
InputUtils.setValueByLabelText(wait, "Username", "testuser")

# Click a button by label
ButtonUtils.clickByLabelText(wait, "Sign In")
```

## Project Structure
- `robo_appian/` - Library source code
- `docs/` - Documentation and guides

## Contributing
Contributions are welcome! Please see the [contributing guidelines](CONTRIBUTING.md) or open an issue to get started.

## License
MIT License. See [LICENSE](LICENSE) for details.

---

For questions or support, contact [Dinil Mithra](mailto:dinilmithra.mailme@gmail.com) or connect on [LinkedIn](https://www.linkedin.com/in/dinilmithra).
