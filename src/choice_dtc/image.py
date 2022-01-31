import time

from io import BytesIO
from PIL import Image, ImageChops
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
        image.save("./tests/data/images/" + file_name + ".png")

    def are_images_equal(self, image1: Image, image2: Image) -> bool:
        """
        If the images are identical, all pixels
        in the difference image are zero,
        and the bounding box function returns None.
        """
        return ImageChops.difference(image1, image2).getbbox() is None

    def validate_image(self, file_name: str, image_element: str, locator_type: str, timeout: int) -> bool:
        image = self.browser.get_web_element(image_element, locator_type, timeout)
        captured_image = self.capture_image(image)
        return self.are_images_equal(Image.open(file_name), captured_image)
