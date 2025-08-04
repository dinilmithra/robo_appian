class MyCustomError(Exception):
    """A custom exception for specific error conditions."""

    def __init__(self, message="This is a custom error!"):
        self.message = message
        super().__init__(self.message)
