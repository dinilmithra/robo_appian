# Robo Appian

Python library for automating Appian web UI test cases!

# Modules
## Components

    ButtonUtils: Interact with button components.
    DateUtils: Interact with date fields.
    DropdownUtils: Interact with dropdowns.
    InputUtils: Interact with input fields.
    LabelUtils: Interact with date Find labels.
    LinkUtils: Interact with date  links.
    TableUtils: Interact with tables.
    TabUtils: Interact with tabs.
    ComponentUtils: General utilities for components.

## Controllers

    ComponentDriver: High-level interface to execute actions on components.

## Exceptions

    MyCustomError: Custom exception for specific error conditions.

# Usage

Import the utilities in your test scripts:

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
