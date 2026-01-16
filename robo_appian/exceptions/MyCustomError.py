class MyCustomError(Exception):
    """
    Custom exception for robo_appian-specific error conditions.

    Use this exception when robo_appian operations encounter conditions that require
    special handling distinct from standard Selenium or Python exceptions.

    Examples:
        >>> raise MyCustomError("Element not found in expected state")
        >>> try:
        ...     some_operation()
        ... except MyCustomError as e:
        ...     print(f"Custom error occurred: {e.message}")
    """

    def __init__(self, message="This is a custom error!"):
        self.message = message
        super().__init__(self.message)
