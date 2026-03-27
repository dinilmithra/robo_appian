from typing import Any, Optional

from robo_appian.components.ButtonUtils import ButtonUtils
from robo_appian.components.DateUtils import DateUtils
from robo_appian.components.DropdownUtils import DropdownUtils
from robo_appian.components.InputUtils import InputUtils
from robo_appian.components.LabelUtils import LabelUtils
from robo_appian.components.LinkUtils import LinkUtils
from robo_appian.components.SearchDropdownUtils import SearchDropdownUtils
from robo_appian.components.SearchInputUtils import SearchInputUtils
from robo_appian.components.TabUtils import TabUtils
from robo_appian.exceptions.MyCustomError import MyCustomError

Page = Any


class ComponentDriver:
    @staticmethod
    def execute(
        page: Page,
        component_type: str,
        action: str,
        label: str,
        value: Optional[str],
    ):
        match (component_type, action):
            case ("Input Text", "Set Value"):
                if value is None:
                    raise MyCustomError("Input Text / Set Value requires a value.")
                return InputUtils.setValueByLabelText(page, label, value)
            case ("Button", "Click"):
                return ButtonUtils.clickByLabelText(page, label)
            case ("Drop Down", "Select"):
                if value is None:
                    raise MyCustomError("Drop Down / Select requires a value.")
                return DropdownUtils.selectDropdownValueByLabelText(page, label, value)
            case ("Search Drop Down", "Select"):
                if value is None:
                    raise MyCustomError("Search Drop Down / Select requires a value.")
                return SearchDropdownUtils.selectSearchDropdownValueByLabelText(
                    page, label, value
                )
            case ("Search Input Text", "Select"):
                if value is None:
                    raise MyCustomError("Search Input Text / Select requires a value.")
                return SearchInputUtils.selectSearchInputByLabelText(page, label, value)
            case ("Date", "Set Value"):
                if value is None:
                    raise MyCustomError("Date / Set Value requires a value.")
                return DateUtils.setValueByLabelText(page, label, value)
            case ("Tab", "Find"):
                return TabUtils.findTabByLabelText(page, label)
            case ("Tab", "Click"):
                return TabUtils.selectTabByLabelText(page, label)
            case ("Link", "Click"):
                return LinkUtils.click(page, label)
            case ("Label", "Find"):
                return LabelUtils.isLabelExists(page, label)
            case _:
                raise MyCustomError(
                    f"Unsupported component/action combination: {component_type} / {action}"
                )
