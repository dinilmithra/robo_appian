import logging
import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


class RoboUtils:

    @staticmethod
    def retry_on_timeout(
        operation,
        max_retries=3,
        operation_name="operation",
        retry_delay_seconds=1.0,
    ):
        """
        Retries an operation that may fail due to Playwright timeout exceptions.

        This utility method automatically retries a given operation if it encounters a
            PlaywrightTimeoutError, which is common in web automation when elements take longer
        to load than expected. It will retry up to the specified number of attempts
        before giving up. Any non-timeout exceptions are immediately re-raised without
        retry attempts.

        Args:
            operation (callable): A callable (function or lambda) that performs the
                desired operation. The callable should take no arguments and return
                a value. Example: lambda: page.locator("#submit-button").click()
            max_retries (int, optional): The maximum number of total attempts (initial + retries).
                Defaults to 3 (meaning 1 initial attempt + up to 2 retries).
            operation_name (str, optional): A descriptive name for the operation
                being performed, used in error messages and logging. Defaults to
                "operation".
            retry_delay_seconds (float, optional): Delay between retries to allow the
                UI time to recover. Defaults to 1.0 second.

        Returns:
            The return value from the successful execution of the operation callable.

        Raises:
            PlaywrightTimeoutError: If the operation fails with PlaywrightTimeoutError for all
                retry attempts (including the initial attempt).
            Exception: Any non-timeout exceptions are immediately re-raised without
                retry attempts.

        Note:
            The method logs errors when all retry attempts are exhausted. Make sure
            logging is properly configured to capture these messages.
        """
        retry_count = 0

        while retry_count < max_retries:
            try:
                return operation()
            except PlaywrightTimeoutError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    msg = f"Failed to execute {operation_name} after {max_retries} attempts."
                    logger.error(msg)
                    raise PlaywrightTimeoutError(msg) from e
                else:
                    logger.warning(
                        f"Timeout during {operation_name}, retrying ({retry_count}/{max_retries})..."
                    )
                    if retry_delay_seconds > 0:
                        time.sleep(retry_delay_seconds)
            except Exception as e:
                msg = f"Error during {operation_name}: {e}"
                logger.error(msg)
                raise
