import time
from io import BytesIO
from logging import getLogger

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
        return Image.open(BytesIO(bytes(web_element.screenshot_as_png)))

    def validate_image(self, file_path: str, image_element: str, locator_type: str, timeout: int) -> None:
        log = getLogger(f"{self.test_name}.validate_image")
        image = self.browser.get_web_element(image_element, locator_type, timeout)
        captured_image = self.capture_image(image)
        if not self.are_images_equal(Image.open(file_path), captured_image):
            log.error(f"The image in: '{file_path}' does not match the image in: `{image_element}`")
            assert False, "Images are not identical"

    @staticmethod
    def are_images_equal(image1: Image, image2: Image) -> bool:
        if image1.size != image2.size:
            return False
        image1_pixels = image1.load()
        image2_pixels = image2.load()
        for x in range(image1.size[0]):
            for y in range(image1.size[1]):
                if image1_pixels[x, y] != image2_pixels[x, y]:
                    return False
        return True
