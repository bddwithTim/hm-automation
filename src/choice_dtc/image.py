import time

from io import BytesIO
from PIL import Image
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.lib.browser import Browser


class ChoiceDTCImage:
    """
    Utility class for handling image operations.
    """

    def __init__(self, test_name, driver: WebDriver) -> None:
        self.test_name = test_name
        self.driver = driver
        self.browser = Browser(self.test_name, self.driver)

    def crop_image(self, image, x, y, width, height):
        return image.crop((x, y, x + width, y + height))

    def capture_image(self, web_element: WebElement) -> Image:
        if web_element is None:
            raise ValueError("Web element cannot be None")
        self.browser.scroll_to_element(web_element)
        time.sleep(0.8)
        return Image.open(BytesIO(web_element.screenshot_as_png))

    def save_image(self, image: Image, file_name: str) -> None:
        # save image as png
        image.save("./tests/results/images/" + file_name + ".png")
