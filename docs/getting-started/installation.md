# Installation

## Requirements

Before installing Robo Appian, ensure you have the following requirements:

- **Python 3.12 or higher**
- **A supported web browser** (Chrome, Firefox, Edge, Safari)
- **Internet connection** for downloading dependencies

## Install Robo Appian

### Using pip (Recommended)

Install Robo Appian from PyPI using pip:

```bash
pip install robo_appian
```

### Using poetry

If you're using Poetry for dependency management:

```bash
poetry add robo_appian
```

## WebDriver Setup

Robo Appian requires a WebDriver to control your browser. Here are the setup instructions for different browsers:

### Chrome (Recommended)

=== "Automatic Setup"
    ```bash
    pip install webdriver-manager
    ```
    
    Then in your Python code:
    ```python
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    ```

=== "Manual Setup"
    1. Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
    2. Extract the executable and add it to your system PATH
    3. Or specify the path directly in your code:
    
    ```python
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    
    service = Service('/path/to/chromedriver')
    driver = webdriver.Chrome(service=service)
    ```

### Firefox

=== "Automatic Setup"
    ```bash
    pip install webdriver-manager
    ```
    
    ```python
    from selenium import webdriver
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.service import Service
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    ```

=== "Manual Setup"
    1. Download GeckoDriver from [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)
    2. Extract and add to PATH or specify path directly

### Edge

=== "Automatic Setup"
    ```bash
    pip install webdriver-manager
    ```
    
    ```python
    from selenium import webdriver
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.service import Service
    
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    ```

## Verify Installation

Create a simple test script to verify everything is working:

```python title="test_installation.py"
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from robo_appian.utils.ComponentUtils import ComponentUtils

def test_installation():
    """Test script to verify Robo Appian installation"""
    
    # Initialize WebDriver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Test basic functionality
        driver.get("https://www.google.com")
        
        # Test Robo Appian utilities
        today = ComponentUtils.today()
        print(f"✅ Robo Appian installed successfully!")
        print(f"✅ Today's date: {today}")
        print(f"✅ WebDriver working correctly")
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_installation()
```

Run the test:

```bash
python test_installation.py
```

Expected output:
```
✅ Robo Appian installed successfully!
✅ Today's date: 08/03/2025
✅ WebDriver working correctly
```

## Troubleshooting

### Common Issues

#### 1. WebDriver Path Issues

**Error**: `selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH`

**Solution**: Use webdriver-manager or add ChromeDriver to your system PATH:

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

#### 2. Browser Version Mismatch

**Error**: `SessionNotCreatedException: session not created: This version of ChromeDriver only supports Chrome version X`

**Solution**: Update your browser or use webdriver-manager to automatically download the correct version:

```bash
pip install --upgrade webdriver-manager
```

#### 3. Import Errors

**Error**: `ModuleNotFoundError: No module named 'robo_appian'`

**Solution**: Ensure you're using the correct Python environment:

```bash
# Check your Python version
python --version

# Check if robo_appian is installed
pip list | grep robo_appian

# Reinstall if necessary
pip install --upgrade robo_appian
```

#### 4. Permission Issues (Linux/Mac)

**Error**: `Permission denied` when running WebDriver

**Solution**: Make the WebDriver executable:

```bash
chmod +x /path/to/chromedriver
```

### Getting Help

If you encounter issues not covered here:

1. **Contact the author** for support:
   - **Email**: dinilmithra.mailme@gmail.com
   - **LinkedIn**: [Dinil Mithra](https://www.linkedin.com/in/dinilmithra)
2. **When contacting, please include**:
   - Your operating system
   - Python version (`python --version`)
   - Browser version
   - Complete error message
   - Minimal code example that reproduces the issue

## Next Steps

Now that you have Robo Appian installed, you're ready to:

- [Write your first test](quick-start.md)
- [Learn about the core components](../user-guide/components.md)
- [Explore examples](../examples/login.md)

## Virtual Environment (Recommended)

For better dependency management, consider using a virtual environment:

=== "venv"
    ```bash
    # Create virtual environment
    python -m venv robo_appian_env
    
    # Activate (Windows)
    robo_appian_env\Scripts\activate
    
    # Activate (Linux/Mac)
    source robo_appian_env/bin/activate
    
    # Install Robo Appian
    pip install robo_appian
    ```

=== "conda"
    ```bash
    # Create conda environment
    conda create -n robo_appian python=3.12
    
    # Activate environment
    conda activate robo_appian
    
    # Install Robo Appian
    pip install robo_appian
    ```

This keeps your project dependencies isolated and prevents conflicts with other Python projects.
