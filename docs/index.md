# Robo Appian

**Automate your Appian code testing with Python. Boost quality, save time.**

<!-- [![PyPI version](https://badge.fury.io/py/robo-appian.svg)](https://badge.fury.io/py/robo-appian)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) -->

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

## 📚 Modules

### Components
Utilities for interacting with Appian UI components:

- **ButtonUtils**: Interact with button components
- **DateUtils**: Interact with date fields and date pickers
- **DropdownUtils**: Interact with dropdown/select components
- **InputUtils**: Interact with input fields and text areas
- **LabelUtils**: Find and interact with labels
- **LinkUtils**: Interact with links and clickable elements
- **TableUtils**: Interact with tables, grids, and data structures
- **TabUtils**: Interact with tab components
- **ComponentUtils**: General utilities for components

### Controllers
High-level interfaces for component interaction:

- **ComponentDriver**: High-level interface to execute actions on components

### Exceptions
Custom exceptions for better error handling:

- **MyCustomError**: Custom exception for specific error conditions

## 🛠️ Requirements

- Python 3.12+
- Selenium WebDriver 4.34.0+
- A compatible web browser (Chrome, Firefox, etc.)

## 📖 Documentation Navigation

Use the navigation menu to explore detailed documentation for each component:

- Click on any component in the **Components** section for detailed API documentation
- Each component page includes method signatures, parameters, and usage examples
- All methods include docstrings with clear explanations and examples

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

    from robo_appian import (
        ButtonUtils, ComponentUtils, DateUtils, DropdownUtils, InputUtils,
        LabelUtils, LinkUtils, TableUtils, TabUtils
    )

#  Set a Date Value
    DateUtils.set_date_value("date_field_id", "2023-10-01")
    
#  Click a Button
    ButtonUtils.click_button("submit_button_id")

#  Select a Dropdown Value
    DropdownUtils.select_value("dropdown_id", "Option 1")

#  Enter Text in an Input Field
    InputUtils.enter_text("input_field_id", "Sample Text")

#  Click a Link
    LinkUtils.click_link("link_id")

#  Click a Tab
    TabUtils.click_tab("tab_id")

#  Get a Table Cell Value
    TableUtils.get_cell_value("table_id", 1, 2)  # Row 1, Column 2

#  Get a Label Value
    LabelUtils.get_label_value("label_id")

#  Get a Component Value
    ComponentUtils.get_component_value("component_id")

#  Use the Component Driver
    from robo_appian.utils.controllers.ComponentDriver import ComponentDriver
    ComponentDriver.execute(wait, "Button", "Click", "Submit", None)

## Dependencies

    Python >= 3.8
    Uses selenium
