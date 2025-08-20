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
    Utility class for interacting with various components in Appian UI.
    Usage Example:
    from robo_appian.utils.controllers.ComponentDriver import ComponentDriver
    # Set a date value
    ComponentDriver.execute(wait, "Date", "Set Value", "Start Date", "01/01/2024")
    """

    @staticmethod
    def execute(wait: WebDriverWait, type, action, label, value):
        """
        Executes an action on a specified component type.
        Parameters:
            wait: Selenium WebDriverWait instance.
            type: The type of component (e.g., "Date", "Input Text", "Search Input Text", etc.).
            action: The action to perform on the component (e.g., "Set Value", "Click", "Select").
            label: The visible text label of the component.
            value: The value to set in the component (if applicable).
        Example:
            ComponentDriver.execute(wait, "Date", "Set Value", "Start Date", "01/01/2024")
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
                        SearchInputUtils.selectSearchDropdownByLabelText(wait, label, value)
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
                        SearchDropdownUtils.selectSearchDropdownValueByLabelText(wait, label, value)
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
