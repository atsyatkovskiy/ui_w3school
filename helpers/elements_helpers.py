"""Модуль с вспомогательными классами для поиска элементов."""
import sys
import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class ElementsHelpers:
    def __init__(self, base):
        self.wait = base.wait
        self.driver = base.driver
        self.timeout = base.timeout
        self.waits = base.waits

    def click(self, element, message, with_tab=False):
        """Возвращает клик по найденному элементу.
        :param element: элемент
        :param with_tab: с последующим кликом на кнопку Tab
        :param message: сообщение об ошибке, если элемент не будет найден
        """
        for i in range(3):
            try:
                element.click()
                if with_tab:
                    actions = ActionChains(self.driver)
                    actions.send_keys(Keys.TAB).perform()
                return
            except StaleElementReferenceException:
                exception = sys.exc_info()
                time.sleep(0.1)
        raise Exception(F"{message}. Описание ошибки: {exception[0]};\n{exception[1]}")

    def click_action_chains(self, element):
        """Возвращает клик по найденному элементу через ActionChains
        :param element: элемент
        """
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def click_on_element_js(self, element):
        """Возвращает клик по найденному элементу.

        :param element: элемент
        """
        self.driver.execute_script("arguments[0].click();", element)

    def execute_command_js(self, command):
        """Выполнить команду JS.
        :param command: элемент
        """
        self.driver.execute_script(f"{command}")

    @staticmethod
    def get_text_of_element(element):
        """Возвращает текст найденного элемента.

        :param element: элемент
        """
        return element.text

    def scroll_to_element(self, element):
        """ Scroll до элемента.
        :param element: элемент
        """
        if isinstance(element, WebElement):
            self.driver.execute_script("arguments[0].scrollIntoView( true );", element)
        else:
            self.driver.execute_script("$('{}')[0].scrollIntoView( true );".format(element[1]))

    def mouse_move_to_element(self, element):
        """Наводит курсор мыши на элемент.

        :param element: элемент
        """
        ActionChains(self.driver).move_to_element_with_offset(element, 10, 10).perform()

    @staticmethod
    def get_locator_with_text(locator, text):
        """Подставляет в локатор текст

        :param locator: Локатор
        :param text: Текст который нужно добавить в локатор
        """
        result = locator.replace("RESULT_TEXT", text)
        return result

    @staticmethod
    def is_element_clickable(element):
        return element.is_enabled() and element.is_displayed()

    def get_text_alert_with_wait(self, message, timeout=None):
        """Возвращает текст alert

        :param timeout: таймаут поиска элемента
        :param message: сообщение об ошибке, если элемент не будет найден
        """
        timeout = timeout if timeout is not None else self.timeout
        alert = self.waits.alert_is_present(message, timeout)
        return alert.text
