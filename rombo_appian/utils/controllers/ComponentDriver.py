from rombo_appian.utils.components.ComponentUtils import ComponentUtils
from rombo_appian.utils.components.DateUtils import DateUtils
from rombo_appian.utils.components.DropdownUtils import DropdownUtils
from rombo_appian.utils.components.InputUtils import InputUtils
from rombo_appian.utils.components.LabelUtils import LabelUtils
from rombo_appian.utils.components.LinkUtils import LinkUtils
from rombo_appian.utils.components.TabUtils import TabUtils


class ComponentDriver():

    @staticmethod
    def execute(wait, type, action, label, value):

        match type:

            case "Date":
                match action:
                    case "Set Value":
                        DateUtils.setDateValue(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Input Text":
                match action:
                    case "Set Value":
                        InputUtils.setInputValue(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Search Input Text":
                match action:
                    case "Select":
                        InputUtils.setSearchInputValue(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Label":
                match action:
                    case "Find":
                        LabelUtils.find(wait, label)
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
                        DropdownUtils.selectDropdownValue(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Search Drop Down":
                match action:
                    case "Select":
                        DropdownUtils.selectSearchDropdownValue(wait, label, value)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Button":
                match action:
                    case "Click":
                        ComponentUtils.click_button(wait, label)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case "Tab":
                match action:
                    case "Find":
                        TabUtils.find_selected_tab(wait, label)
                    case _:
                        raise ValueError(f"Unsupported action for {type}: {action}")
            case _:
                raise ValueError(f"Unsupported component type: {type}")
