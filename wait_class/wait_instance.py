from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


class Wait:

    def __init__(self, driver):
        self.wait = wait(driver, timeout=10)

    def element_is_visible(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def elements_are_visible(self, locator: tuple):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def element_is_presence(self, locator: tuple):
        return self.wait.until(EC.presence_of_element_located(locator))

    def url_is(self, url: str):
        return self.wait.until(EC.url_to_be(url))

    def title_is(self, title: str):
        return self.wait.until(EC.title_is(title))

    def element_is_clickable(self, locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def until(self, method: object) -> object:
        return self.wait.until(method)

    def url_contain(self, url: str):
        return self.wait.until(EC.url_contains(url))
