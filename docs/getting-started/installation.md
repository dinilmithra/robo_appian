# Installation

Follow these steps to install Robo Appian and its prerequisites.

## Prerequisites
- Python 3.12+
- Playwright browser binaries installed locally
- pip and (optionally) Poetry for dev work

## Install the package

**Using pip:**
```bash
pip install robo-appian-pr
playwright install
```

**Using Poetry:**
```bash
poetry add robo-appian-pr
poetry run playwright install
```

## Verify installation
```bash
python -c "import robo_appian; print(robo_appian.__version__)"
```

If you see a version string, installation was successful. If Playwright cannot launch a browser, rerun `playwright install` for your environment.
