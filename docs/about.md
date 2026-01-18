# About Robo Appian

## Overview

Robo Appian is a specialized Python library designed to simplify and accelerate Appian UI test automation. Built on top of Selenium WebDriver, it provides a clean, label-driven API that makes writing and maintaining Appian automation tests significantly easier.

## Why Robo Appian?

Testing Appian applications presents unique challenges:

- **Complex DOM structures** with dynamically generated IDs
- **Heavy reliance on ARIA patterns** for accessibility
- **Label-based component identification** is more reliable than fragile XPath selectors
- **Timing issues** due to dynamic content loading and animations

Robo Appian addresses these challenges by:

- ✅ **Label-first selectors** - Locate elements by their visible labels, not internal IDs
- ✅ **Appian-aware patterns** - Built-in understanding of Appian's component structure
- ✅ **Resilient interactions** - Smart waits and retry logic for flaky operations
- ✅ **Clean API** - Readable test code that's easy to maintain
- ✅ **Comprehensive coverage** - Support for all major Appian UI components

## Key Features

### Component Support
- Text inputs and search inputs
- Buttons and links
- Dropdowns and search dropdowns
- Date pickers
- Tables with dynamic column/row access
- Tabs and labels
- Custom component extensions

### Built-in Resilience
- Automatic wait handling for element visibility and clickability
- Retry mechanisms for flaky operations
- Safe click handling using ActionChains
- NBSP normalization and hidden element filtering

### Developer-Friendly
- Wait-first pattern for consistent API design
- Static utility methods for easy importing
- Comprehensive documentation with examples
- Integration guides for pytest and unittest

## About the Author

**Dinil Mithra** is a software engineer and test automation specialist with extensive experience in enterprise application testing. With a focus on quality assurance and continuous improvement, Dinil recognized the need for better tooling around Appian UI automation and created Robo Appian to help teams:

- Write more reliable automated tests
- Reduce maintenance overhead
- Improve test readability and collaboration
- Accelerate delivery timelines

Connect with Dinil:

- 🔗 [LinkedIn](https://www.linkedin.com/in/dinilmithra)
- 📧 [Email](mailto:dinilmithra.mailme@gmail.com)

## Contributing

Robo Appian is open source and welcomes contributions! Whether you're:

- Reporting a bug
- Suggesting a new feature
- Improving documentation
- Submitting code changes

Your contributions help make this library better for the entire Appian automation community.

## Technology Stack

- **Python 3.12+** - Modern Python with latest features
- **Selenium 4.34+** - Latest WebDriver capabilities
- **Poetry** - Dependency management and packaging
- **MkDocs Material** - Beautiful documentation
- **pytest** - Recommended testing framework

## License

MIT License - Free to use, modify, and distribute.

Copyright © 2024 Dinil Mithra

## Version History

Current version: **0.0.33**

Check the release notes for the latest updates and improvements.

---

*Built with ❤️ for the Appian testing community*
