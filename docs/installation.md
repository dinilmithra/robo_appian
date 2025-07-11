# Installation Guide

## Prerequisites

Before installing Robo Appian, ensure you have:

- Python 3.12 or higher
- pip package manager
- A compatible web browser (Chrome, Firefox, Edge, Safari)
- Selenium WebDriver for your chosen browser

## Installation Methods

### Method 1: pip (Recommended)

```bash
pip install robo-appian
```

### Method 2: Poetry

```bash
poetry add robo-appian
```

### Method 3: From Source

```bash
git clone https://github.com/dinilmithra/robo_appian.git
cd robo_appian
pip install -e .
```

## WebDriver Setup

### Chrome WebDriver

```bash
# Install ChromeDriver
pip install webdriver-manager

# Usage in your code
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

### Firefox WebDriver

```bash
# Install GeckoDriver
pip install webdriver-manager

# Usage in your code
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
```

## Verification

Verify your installation:

```python
import robo_appian
print(f"Robo Appian version: {robo_appian.__version__}")

# Test basic import
from robo_appian import ButtonUtils
print("Installation successful!")
```

## Next Steps

- Check out the [Quick Start Guide](index.md#quick-start)
- Explore the [Component Documentation](ButtonUtils.md)
- Review [Examples](examples.md)
