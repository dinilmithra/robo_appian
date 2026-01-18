# Installation

Follow these steps to install Robo Appian and its prerequisites.

## Prerequisites
- Python 3.12+
- A working Selenium WebDriver for your browser (e.g., ChromeDriver, GeckoDriver) on PATH
- pip and (optionally) Poetry for dev work

## Install the package

**Using pip:**
```bash
pip install robo_appian
```

**Using Poetry:**
```bash
poetry add robo_appian
```

## Verify installation
```bash
python -c "import robo_appian; print(robo_appian.__version__)"
```

If you see a version string, installation was successful. If WebDriver fails to start, confirm the driver binary (ChromeDriver, GeckoDriver, etc.) matches your browser version and is on PATH.
