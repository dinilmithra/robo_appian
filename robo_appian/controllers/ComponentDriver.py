from robo_appian.components.ButtonUtils import ButtonUtils
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.DateUtils import DateUtils
from robo_appian.components.DropdownUtils import DropdownUtils
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.LabelUtils import LabelUtils
from robo_appian.components.LinkUtils import LinkUtils
from robo_appian.components.TabUtils import TabUtils
from robo_appian.components.SearchInputUtils import SearchInputUtils
from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils


class ComponentDriver:
    """
    High-level action router for Appian UI components: unifies all component interactions.

    Instead of importing individual utilities (InputUtils, ButtonUtils, etc.), use ComponentDriver
    to route actions by component type and label. This simplifies test code and centralizes
    the mapping between component types and available actions.

    Supported component types: Date, Input Text, Button, Drop Down, Search Input Text,
    Search Drop Down, Label, Link, Tab.

    All methods follow the wait-first pattern: pass WebDriverWait as the first argument.

    Examples:
        >>> from robo_appian.controllers.ComponentDriver import ComponentDriver
        >>> # Set a date value
        >>> ComponentDriver.execute(wait, "Date", "Set Value", "Start Date", "01/01/2024")
        >>> # Fill a text input
        >>> ComponentDriver.execute(wait, "Input Text", "Set Value", "Username", "john_doe")
        >>> # Click a button
        >>> ComponentDriver.execute(wait, "Button", "Click", "Submit", None)
        >>> # Select dropdown option
        >>> ComponentDriver.execute(wait, "Drop Down", "Select", "Status", "Active")
    """

    @staticmethod
    def execute(wait: WebDriverWait, type, action, label, value):
        """
        Execute a high-level action on an Appian component by type, action, label, and value.

        Routes the action to the appropriate utility class (InputUtils, ButtonUtils, etc.) based
        on component type and action. Eliminates need for direct utility imports in tests.

        Args:
            wait: WebDriverWait instance (required by all robo_appian utilities).
            type: Component type string. Supported: "Date", "Input Text", "Button", "Drop Down",
                "Search Input Text", "Search Drop Down", "Label", "Link", "Tab".
            action: Action string. Common values: "Set Value", "Click", "Select", "Find".
                Valid actions depend on component type (see supported combinations below).
            label: Exact visible label text of the component on the page (used to locate element).
            value: Value to set or select. None for click/find actions; required for Set Value/Select.

        Returns:
            None

        Raises:
            ValueError: If component type or action is not supported.
            TimeoutException: If component not found or not clickable within wait timeout.

        Examples:
            >>> # Set date value
            >>> ComponentDriver.execute(wait, "Date", "Set Value", "Start Date", "01/01/2024")
            >>> # Fill text input
            >>> ComponentDriver.execute(wait, "Input Text", "Set Value", "Email", "test@example.com")
            >>> # Click button
            >>> ComponentDriver.execute(wait, "Button", "Click", "Submit", None)
            >>> # Select dropdown
            >>> ComponentDriver.execute(wait, "Drop Down", "Select", "Department", "Sales")
            >>> # Search and select from search dropdown
            >>> ComponentDriver.execute(wait, "Search Drop Down", "Select", "Employee", "John Doe")
            >>> # Click link
            >>> ComponentDriver.execute(wait, "Link", "Click", "Learn More", None)
            >>> # Check if label exists
            >>> ComponentDriver.execute(wait, "Label", "Find", "Important Notice", None)
            >>> # Select tab
            >>> ComponentDriver.execute(wait, "Tab", "Find", "Details", None)
        """
        # This method executes an action on a specified component type based on the provided parameters.

        match type:
            case "Date":
                match action:
                    case "Set Value":
                        DateUtils.setValueByLabelText(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Input Text":
                match action:
                    case "Set Value":
                        InputUtils.setValueByLabelText(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Search Input Text":
                match action:
                    case "Select":
                        SearchInputUtils.selectSearchDropdownByLabelText(
                            wait, label, value
                        )
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Label":
                match action:
                    case "Find":
                        LabelUtils.isLabelExists(wait, label)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Link":
                match action:
                    case "Click":
                        LinkUtils.click(wait, label)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Drop Down":
                match action:
                    case "Select":
                        DropdownUtils.selectDropdownValueByLabelText(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Search Drop Down":
                match action:
                    case "Select":
                        SearchDropdownUtils.selectSearchDropdownValueByLabelText(
                            wait, label, value
                        )
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Button":
                match action:
                    case "Click":
                        ButtonUtils.clickByLabelText(wait, label)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Tab":
                match action:
                    case "Find":
                        TabUtils.selectTabByLabelText(wait, label)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case _:
                raise ValueError(f"Unsupported component type: {type}")
