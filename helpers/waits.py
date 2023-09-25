"""Модуль с вспомогательными классами для поиска элементов."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WaitsHelpers:

    def __init__(self, base):
        self.wait = base.wait
        self.driver = base.driver
        self.timeout = base.timeout

    def is_element_visible(self, type_locator, el_path, message, timeout=None):
        """Возвращает результат ожидания видимости элемента.
        :param type_locator: тип локатора
        :param el_path: путь до элемента
        :param message: сообщение об ошибке, если элемент не будет найден
        :param timeout: таймаут поиска элемента
        """
        timeout = timeout if timeout is not None else self.timeout
        self.driver.implicitly_wait(0)
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((type_locator, el_path)),
            f'За {timeout} сек: {message}\nЛокатор: {type_locator} {el_path}'
        )
        self.driver.implicitly_wait(self.timeout)
        return True

    def is_element_not_visible(self, type_locator, el_path, message, timeout=None):
        """Возвращает результат ожидания видимости элемента.
        :param type_locator: тип локатора
        :param el_path: путь до элемента
        :param message: сообщение об ошибке, если элемент не будет найден
        :param timeout: таймаут поиска элемента
        """
        timeout = timeout if timeout is not None else self.timeout
        self.driver.implicitly_wait(0)
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((type_locator, el_path)),
            F"За {timeout} сек:{message}"
        )
        self.driver.implicitly_wait(self.timeout)
        return True

    def presence_of_element_located(self, type_locator, el_path, message, timeout=None):
        """Возвращает True если элемент есть в DOM.
        :param type_locator: тип локатора
        :param el_path: путь до элемента
        :param message: сообщение об ошибке, если элемент не будет найден
        :param timeout: таймаут поиска элемента
        """
        timeout = timeout if timeout is not None else self.timeout
        self.driver.implicitly_wait(0)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((type_locator, el_path)),
            f'За {timeout} сек: {message}\nЛокатор: {type_locator} {el_path}'
        )
        self.driver.implicitly_wait(self.timeout)
        return True

    def find_element_with_wait(self, type_locator, el_path, message, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        self.is_element_visible(type_locator, el_path, message, timeout)
        elem = self.driver.find_element(type_locator, el_path)
        return elem

    def find_elements_with_wait(self, type_locator, el_path, message, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        self.is_element_visible(type_locator, el_path, message, timeout)
        elems = self.driver.find_elements(type_locator, el_path)
        return elems

    def url_contains(self, expected_text, message, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        self.driver.implicitly_wait(0)
        WebDriverWait(self.driver, timeout).until(EC.url_contains(expected_text), F"За {timeout} сек:{message}")
        self.driver.implicitly_wait(self.timeout)

    def url_to_be(self, expected_text, message, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        self.driver.implicitly_wait(0)
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(expected_text), F"За {timeout} сек:{message}")
        self.driver.implicitly_wait(self.timeout)

    def alert_is_present(self, message, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        self.driver.implicitly_wait(0)
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present(), F"За {timeout} сек:{message}")
        self.driver.implicitly_wait(self.timeout)
        return alert
