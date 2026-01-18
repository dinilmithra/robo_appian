---
title: Welcome to Robo Appian
hide:
  - toc
---

# Robo Appian

**Robo Appian** is a Python helper library that makes Appian UI automation readable, label-driven, and resilient. It wraps Selenium with Appian-aware locators so tests stay stable as the DOM shifts.

## Why Robo Appian?
- **Label-first selectors**: Target inputs, buttons, dropdowns, and grids by their visible labels and ARIA structure instead of brittle IDs.
- **Wait-first APIs**: Every public call starts with `WebDriverWait`, then safely drives the underlying `driver` (`wait._driver`).
- **Consistent patterns**: Static `*Utils` classes for components make testing straightforward and maintainable.

## Quick links
- Start fast: [Installation](getting-started/installation.md) · [Quick Start](getting-started/quick-start.md)
- How it works: [Component patterns](user-guide/components.md) · [Best practices](user-guide/best-practices.md)
- API docs: [Component APIs](api/index.md) powered by mkdocstrings
- Examples: [Login](examples/login.md) · [Forms](examples/forms.md) · [Tables](examples/tables.md) · [Workflows](examples/workflows.md)

## At a glance
- **Python**: 3.12
- **Selenium**: >= 4.34.0
- **Docs**: MkDocs + Material + mkdocstrings

---
Ready to script? Jump to the [Quick Start](getting-started/quick-start.md).
