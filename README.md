# Robo Appian

**Automate your Appian code testing with Python. Boost quality, save time.**

[![PyPI version](https://badge.fury.io/py/robo-appian.svg)](https://badge.fury.io/py/robo-appian)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://dinilmithra.github.io/robo_appian/)

## 🚀 Quick Start

### Installation

```bash
pip install robo-appian
```

### Basic Usage

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian import ButtonUtils, InputUtils, TableUtils

# Setup your driver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Interact with Appian components
ButtonUtils.click(wait, "Submit")
InputUtils.set_text(wait, "Username", "john.doe")
TableUtils.click_cell_link(wait, "Actions", 1, "Edit")
```

## 📚 Features

### Components
- **ButtonUtils**: Find and click buttons
- **DateUtils**: Interact with date fields and date pickers  
- **DropdownUtils**: Interact with dropdown/select components
- **InputUtils**: Interact with input fields and text areas
- **LabelUtils**: Find and interact with labels
- **LinkUtils**: Click links and navigate
- **TableUtils**: Interact with tables and grids
- **TabUtils**: Switch between tabs
- **ComponentUtils**: General component utilities

### Controllers
- **ComponentDriver**: High-level interface for component interaction

### Exceptions
- **MyCustomError**: Custom exceptions for better error handling

## 📖 Documentation

Visit our [full documentation](https://dinilmithra.github.io/robo_appian/) for:
- Detailed API reference
- Complete examples and tutorials
- Installation guide
- Best practices

## 🛠️ Requirements

- Python 3.12+
- Selenium WebDriver 4.34.0+
- Compatible web browser (Chrome, Firefox, etc.)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- [Documentation](https://dinilmithra.github.io/robo_appian/)
- [PyPI Package](https://pypi.org/project/robo-appian/)
- [GitHub Repository](https://github.com/dinilmithra/robo_appian)
    ButtonUtils, ComponentUtils, DateUtils, DropdownUtils, InputUtils,
    LabelUtils, LinkUtils, TableUtils, TabUtils
)

# Example: Set a Date Value
    DateUtils.set_date_value("date_field_id", "2023-10-01")
    
# Example: Click a Button
    ButtonUtils.click_button("submit_button_id")

# Example: Select a Dropdown Value
    DropdownUtils.select_value("dropdown_id", "Option 1")

# Example: Enter Text in an Input Field
    InputUtils.enter_text("input_field_id", "Sample Text")

# Example: Click a Link
    LinkUtils.click_link("link_id")

# Example: Click a Tab
    TabUtils.click_tab("tab_id")

# Example: Get a Table Cell Value
    TableUtils.get_cell_value("table_id", 1, 2)  # Row 1, Column 2

# Example: Get a Label Value
    LabelUtils.get_label_value("label_id")

# Example: Get a Component Value
    ComponentUtils.get_component_value("component_id")

# Example: Use the Component Driver
    from robo_appian.utils.controllers.ComponentDriver import ComponentDriver
    ComponentDriver.execute(wait, "Button", "Click", "Submit", None)

## Dependencies

    Python >= 3.8
    Uses selenium

## License

    MIT License. See LICENSE.