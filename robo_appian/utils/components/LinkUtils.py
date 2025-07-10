from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LinkUtils():
    """    
    Utility class for interacting with link components in Appian UI.

    Usage Example:
    from robo_appian.utils.components.LinkUtils import LinkUtils    

    # Click a link with a specific label
    LinkUtils.click(wait, "Learn More")

    """

    @staticmethod
    def click(wait, label):
        """        
        Clicks a link identified by its label.

        Parameters:
            wait: Selenium WebDriverWait instance.
            label: The visible text label of the link.
            
        Example:
            LinkUtils.click(wait, "Learn More")
        """
        # This method locates a link that contains a span with the specified label text.
        # It uses XPath to find the element that matches the text and waits until it is clickable.
        # The link component is expected to have a structure where the label is within a span inside a paragraph element.

        xpath = f'.//p/span[text()="{label}"]'
        # component = wait.until(EC.presence_of_element_located((By.XPATH, xpath)) )
        component = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        component.click()
        return component
