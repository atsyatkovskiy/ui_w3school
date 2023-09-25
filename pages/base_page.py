from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.elements_helpers import ElementsHelpers
from helpers.waits import WaitsHelpers


class BasePage:

    def __init__(self, browser, timeout=None):
        """
        Конструктор класса

        :param browser: фикстура для запуска драйвера
        """

        self.browser = browser
        self.driver = browser["driver"]
        self.url = browser["url"]

        self.timeout = browser["timeout"] if timeout is None else timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

        self.waits = WaitsHelpers(self)
        self.elements = ElementsHelpers(self)

    def open_url(self, url=None):
        """
        :param url: ссылка для перехода
        """
        url = self.url if url is None else url
        self.driver.get(url)

    def is_title_correct(self, title):
        """Проверяем корректность заголовка"""
        self.wait.until(
                EC.title_is(title), f'Ожидалось, что заголовок будет равен "{title}". Получено: {self.driver.title}'
            )

    def get_title(self):
        """Получить title страницы"""
        return self.driver.title

    def get_url(self):
        """Получить url страницы"""
        return self.driver.current_url

    def refresh_browser(self):
        """Обновить страницу браузера"""
        self.driver.refresh()

    def browser_go_to_back(self):
        """Перейти на предыдущую страницу браузера"""
        self.driver.back()

    def browser_go_to_forward(self):
        """Перейти на страницу вперёд"""
        self.driver.forward()
