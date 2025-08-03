# TabUtils

The `TabUtils` class provides methods for interacting with tab components in Appian applications. It handles tab navigation, selection, and status checking, enabling seamless navigation through tabbed interfaces.

## Overview

TabUtils is designed to handle Appian's tab components, providing reliable methods to:

- Find currently selected tabs by label text
- Select inactive tabs to navigate between sections
- Handle complex tab structures and hierarchies
- Manage tab state verification

## Class Methods

### findSelectedTabByLabelText()

Finds the currently selected (active) tab by its visible label text.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): The visible text label of the currently selected tab

**Returns:**
- `WebElement`: The currently selected tab element

**Usage Example:**
```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.TabUtils import TabUtils

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# Find the currently selected tab
current_tab = TabUtils.findSelectedTabByLabelText(wait, "General Information")

# Verify current tab selection
try:
    active_tab = TabUtils.findSelectedTabByLabelText(wait, "Contact Details")
    print("Contact Details tab is currently active")
except:
    print("Contact Details tab is not currently selected")

# Get reference to selected tab for further operations
selected_tab = TabUtils.findSelectedTabByLabelText(wait, "Overview")
```

---

### selectInactiveTabByLabelText()

Selects an inactive tab by its label text, making it the active tab.


**Parameters:**
- `wait` (WebDriverWait): Selenium WebDriverWait instance for element waiting
- `label` (str): The visible text label of the tab to select

**Usage Example:**
```python
# Navigate to different tabs
TabUtils.selectInactiveTabByLabelText(wait, "Personal Information")

# Switch to another tab
TabUtils.selectInactiveTabByLabelText(wait, "Employment History")

# Navigate to settings tab
TabUtils.selectInactiveTabByLabelText(wait, "Account Settings")

# Go to the last tab
TabUtils.selectInactiveTabByLabelText(wait, "Summary")
```

## Best Practices

### Tab Navigation Workflow

**Follow logical tab progression**:
```python
# Navigate through tabs in logical order
tabs = ["Basic Info", "Contact Details", "Employment", "Documents", "Review"]

for tab in tabs:
    TabUtils.selectInactiveTabByLabelText(wait, tab)
    
    # Perform tab-specific operations
    if tab == "Basic Info":
        InputUtils.setValueByLabelText(wait, "First Name", "John")
        InputUtils.setValueByLabelText(wait, "Last Name", "Doe")
    
    elif tab == "Contact Details":
        InputUtils.setValueByLabelText(wait, "Email", "john.doe@example.com")
        InputUtils.setValueByLabelText(wait, "Phone", "555-1234")
    
    # Continue with other tabs...
```

### Verify Tab State

**Check current tab before navigation**:
```python
def safe_tab_navigation(wait, target_tab):
    """Safely navigate to a tab, checking current state first"""
    try:
        # Check if target tab is already selected
        TabUtils.findSelectedTabByLabelText(wait, target_tab)
        print(f"Tab '{target_tab}' is already selected")
        return True
    except:
        # Tab is not selected, navigate to it
        try:
            TabUtils.selectInactiveTabByLabelText(wait, target_tab)
            print(f"Successfully navigated to tab '{target_tab}'")
            return True
        except Exception as e:
            print(f"Failed to navigate to tab '{target_tab}': {e}")
            return False

# Usage
safe_tab_navigation(wait, "Contact Information")
```

### Error Handling

**Handle tab navigation errors gracefully**:
```python
def navigate_to_tab_with_retry(wait, tab_name, max_retries=3):
    """Navigate to tab with retry logic"""
    for attempt in range(max_retries):
        try:
            TabUtils.selectInactiveTabByLabelText(wait, tab_name)
            # Verify navigation was successful
            TabUtils.findSelectedTabByLabelText(wait, tab_name)
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for tab '{tab_name}': {e}")
            if attempt == max_retries - 1:
                return False
            # Wait before retry
            time.sleep(1)
    
    return False
```

## Common Use Cases

### Multi-Step Form Navigation
```python
# Employee onboarding form with multiple tabs
def complete_employee_onboarding(wait, employee_data):
    # Tab 1: Personal Information
    TabUtils.selectInactiveTabByLabelText(wait, "Personal Information")
    InputUtils.setValueByLabelText(wait, "First Name", employee_data['first_name'])
    InputUtils.setValueByLabelText(wait, "Last Name", employee_data['last_name'])
    DateUtils.setValueByLabelText(wait, "Date of Birth", employee_data['dob'])
    
    # Tab 2: Contact Details
    TabUtils.selectInactiveTabByLabelText(wait, "Contact Details")
    InputUtils.setValueByLabelText(wait, "Email", employee_data['email'])
    InputUtils.setValueByLabelText(wait, "Phone", employee_data['phone'])
    InputUtils.setValueByLabelText(wait, "Address", employee_data['address'])
    
    # Tab 3: Employment Information
    TabUtils.selectInactiveTabByLabelText(wait, "Employment")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Department", employee_data['department'])
    DropdownUtils.selectDropdownValueByLabelText(wait, "Position", employee_data['position'])
    DateUtils.setValueByLabelText(wait, "Start Date", employee_data['start_date'])
    
    # Tab 4: Review and Submit
    TabUtils.selectInactiveTabByLabelText(wait, "Review")
    ButtonUtils.clickByLabelText(wait, "Submit Application")

# Usage
employee_info = {
    'first_name': 'John',
    'last_name': 'Doe',
    'dob': '01/15/1990',
    'email': 'john.doe@company.com',
    'phone': '555-1234',
    'address': '123 Main St',
    'department': 'Engineering',
    'position': 'Software Developer',
    'start_date': '01/01/2024'
}

complete_employee_onboarding(wait, employee_info)
```

### Settings Configuration
```python
# Application settings across multiple tabs
def configure_application_settings(wait, settings):
    # General Settings
    TabUtils.selectInactiveTabByLabelText(wait, "General")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Language", settings['language'])
    DropdownUtils.selectDropdownValueByLabelText(wait, "Time Zone", settings['timezone'])
    
    # Security Settings
    TabUtils.selectInactiveTabByLabelText(wait, "Security")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Session Timeout", settings['session_timeout'])
    ButtonUtils.clickByLabelText(wait, "Enable Two-Factor Auth")
    
    # Notification Settings
    TabUtils.selectInactiveTabByLabelText(wait, "Notifications")
    ButtonUtils.clickByLabelText(wait, "Email Notifications")
    ButtonUtils.clickByLabelText(wait, "SMS Notifications")
    
    # Save all settings
    TabUtils.selectInactiveTabByLabelText(wait, "Review")
    ButtonUtils.clickByLabelText(wait, "Save All Settings")
```

### Data Validation Across Tabs
```python
# Validate data across multiple tabs
def validate_form_completion(wait, required_tabs):
    validation_results = {}
    
    for tab_name in required_tabs:
        try:
            # Navigate to tab
            TabUtils.selectInactiveTabByLabelText(wait, tab_name)
            
            # Check for validation errors or required fields
            error_elements = wait.driver.find_elements(By.CLASS_NAME, "validation-error")
            required_elements = wait.driver.find_elements(By.XPATH, "//*[@required and @value='']")
            
            validation_results[tab_name] = {
                'errors': len(error_elements),
                'missing_required': len(required_elements),
                'valid': len(error_elements) == 0 and len(required_elements) == 0
            }
            
        except Exception as e:
            validation_results[tab_name] = {
                'error': str(e),
                'valid': False
            }
    
    return validation_results

# Usage
tabs_to_validate = ["Personal Info", "Contact", "Employment", "Documents"]
results = validate_form_completion(wait, tabs_to_validate)

for tab, result in results.items():
    if result.get('valid', False):
        print(f"✅ {tab}: Valid")
    else:
        print(f"❌ {tab}: Issues found - {result}")
```

### Tab-Based Workflow
```python
# Document review workflow
def document_review_workflow(wait, document_id):
    # Step 1: Open document
    TabUtils.selectInactiveTabByLabelText(wait, "Document Details")
    InputUtils.setValueByLabelText(wait, "Document ID", document_id)
    ButtonUtils.clickByLabelText(wait, "Load Document")
    
    # Step 2: Review content
    TabUtils.selectInactiveTabByLabelText(wait, "Content Review")
    # Perform content review operations
    ButtonUtils.clickByLabelText(wait, "Mark as Reviewed")
    
    # Step 3: Approval
    TabUtils.selectInactiveTabByLabelText(wait, "Approval")
    DropdownUtils.selectDropdownValueByLabelText(wait, "Status", "Approved")
    InputUtils.setValueByLabelText(wait, "Comments", "Document approved for publication")
    
    # Step 4: Final submission
    TabUtils.selectInactiveTabByLabelText(wait, "Submit")
    ButtonUtils.clickByLabelText(wait, "Final Submit")
```

## Technical Details

### Tab Element Structure

TabUtils expects Appian tabs with this structure:

**Selected Tab:**
```html
<div>
  <div>
    <div>
      <div>
        <div>
          <div>
            <div>
              <p>
                <strong>Tab Label</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <span>Selected Tab.</span>
</div>
```

**Inactive Tab:**
```html
<div role="link">
  <div>
    <div>
      <div>
        <div>
          <div>
            <p>
              <span>Tab Label</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

### XPath Strategies

**Selected Tab Detection:**
```xpath
.//div[./div[./div/div/div/div/div/p/strong[normalize-space(text())='{label}']]/span[text()='Selected Tab.']]/div[@role='link']
```

**Inactive Tab Selection:**
```xpath
.//div[@role='link']/div/div/div/div/div[./p/span[text()='{label}']]
```

### Navigation Logic

1. **Current Tab Detection**: Checks for `<strong>` element and "Selected Tab." indicator
2. **Inactive Tab Selection**: Looks for `role="link"` with `<span>` containing label text
3. **Click Action**: Performs click on the clickable tab element

## Troubleshooting

### Common Issues

**Tab Not Found:**
```
TimeoutError: Could not find tab with label 'Contact Details'
```
**Solutions:**
- Verify exact tab label text (check case sensitivity)
- Ensure tab is visible (not hidden or collapsed)
- Check if tab is dynamically loaded
- Wait for any loading animations to complete

**Selected Tab Detection Fails:**
```
TimeoutError: Could not find selected tab with label 'Overview'
```
**Solutions:**
- Verify the tab is actually selected
- Check if tab selection state has changed
- Ensure tab structure matches expected format
- Look for alternative selection indicators

**Tab Selection Not Working:**
```
Element not clickable or tab doesn't change
```
**Solutions:**
- Verify tab is not disabled
- Check for overlaying elements blocking click
- Ensure JavaScript has finished executing
- Try explicit wait before tab interaction

### Debugging Tips

1. **Inspect Tab Structure**:
   ```python
   # Find all tab elements
   tabs = wait.driver.find_elements(By.XPATH, "//div[@role='link']")
   for tab in tabs:
       print(f"Tab HTML: {tab.get_attribute('outerHTML')}")
   ```

2. **Check Tab Labels**:
   ```python
   # Extract all available tab labels
   tab_labels = []
   tabs = wait.driver.find_elements(By.XPATH, "//div[@role='link']//p/span")
   for tab in tabs:
       if tab.text:
           tab_labels.append(tab.text)
   print(f"Available tabs: {tab_labels}")
   ```

3. **Verify Current Selection**:
   ```python
   # Find currently selected tab
   selected_tabs = wait.driver.find_elements(By.XPATH, "//p/strong")
   for tab in selected_tabs:
       if tab.text:
           print(f"Currently selected: {tab.text}")
   ```

## Integration Examples

### With pytest and Tab Validation
```python
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.components.TabUtils import TabUtils

class TestTabNavigation:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def teardown_method(self):
        self.driver.quit()
    
    @pytest.mark.parametrize("tab_name", [
        "Personal Information",
        "Contact Details", 
        "Employment History",
        "Documents"
    ])
    def test_tab_navigation(self, tab_name):
        self.driver.get("https://your-appian-app.com")
        
        # Navigate to tab
        TabUtils.selectInactiveTabByLabelText(self.wait, tab_name)
        
        # Verify tab is now selected
        selected_tab = TabUtils.findSelectedTabByLabelText(self.wait, tab_name)
        assert selected_tab is not None, f"Tab '{tab_name}' should be selected"
```

### With Page Object Model
```python
class MultiTabFormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navigate_to_tab(self, tab_name):
        """Navigate to specified tab"""
        TabUtils.selectInactiveTabByLabelText(self.wait, tab_name)
    
    def get_current_tab(self):
        """Get the currently selected tab name"""
        # Implementation would need to extract current tab name
        pass
    
    def complete_personal_info_tab(self, data):
        """Fill personal information tab"""
        self.navigate_to_tab("Personal Information")
        
        InputUtils.setValueByLabelText(self.wait, "First Name", data['first_name'])
        InputUtils.setValueByLabelText(self.wait, "Last Name", data['last_name'])
        DateUtils.setValueByLabelText(self.wait, "Date of Birth", data['dob'])
    
    def complete_contact_tab(self, data):
        """Fill contact information tab"""
        self.navigate_to_tab("Contact Details")
        
        InputUtils.setValueByLabelText(self.wait, "Email", data['email'])
        InputUtils.setValueByLabelText(self.wait, "Phone", data['phone'])
        InputUtils.setValueByLabelText(self.wait, "Address", data['address'])
    
    def submit_form(self):
        """Navigate to review tab and submit"""
        self.navigate_to_tab("Review")
        ButtonUtils.clickByLabelText(self.wait, "Submit")
```

### With Configuration-Driven Navigation
```python
import yaml

class TabWorkflowManager:
    def __init__(self, wait):
        self.wait = wait
    
    def execute_workflow(self, workflow_config):
        """Execute tab-based workflow from configuration"""
        
        for step in workflow_config['steps']:
            tab_name = step['tab']
            actions = step['actions']
            
            # Navigate to tab
            TabUtils.selectInactiveTabByLabelText(self.wait, tab_name)
            
            # Execute actions for this tab
            for action in actions:
                action_type = action['type']
                
                if action_type == 'input':
                    InputUtils.setValueByLabelText(
                        self.wait, action['label'], action['value']
                    )
                elif action_type == 'dropdown':
                    DropdownUtils.selectDropdownValueByLabelText(
                        self.wait, action['label'], action['value']
                    )
                elif action_type == 'button':
                    ButtonUtils.clickByLabelText(self.wait, action['label'])
                elif action_type == 'date':
                    DateUtils.setValueByLabelText(
                        self.wait, action['label'], action['value']
                    )

# Load workflow from YAML
with open('tab_workflow.yaml') as f:
    workflow = yaml.safe_load(f)

# Execute workflow
manager = TabWorkflowManager(wait)
manager.execute_workflow(workflow)
```

## Related Components

- **[ButtonUtils](button-utils.md)** - For buttons within tab content
- **[InputUtils](input-utils.md)** - For form fields in tabs
- **[DropdownUtils](dropdown-utils.md)** - For dropdowns in tab content
- **[ComponentDriver](component-driver.md)** - For universal component interactions

---

*TabUtils provides essential tab navigation capabilities for Appian applications, enabling seamless movement through multi-step forms and complex interfaces while maintaining reliability and ease of use.*
