import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class W3schoolsLocators:
    """Локаторы w3schools.com"""

    ALL_ROWS_TABLE = (By.XPATH, '//*[@id="divResultSQL"]/div/table/tbody/tr')  # Элементы таблицы
    ALL_HEADERS_TABLE_NAME = (By.XPATH, '//*[@id="divResultSQL"]/div/table/tbody/tr/th')  # имена заголовков таблицы

    BUTTON_RUN_SQL = (By.XPATH, '//button[@class="ws-btn" and @type="button"]')  # кнопка Run SQL
    RESULT_MESSAGE = (By.XPATH, '//div[@id="divResultSQL"]/div')
    FIND_TEXT_FUNCTION = '//*[text()="RESULT_TEXT"]'

    EXPECTED_RESULT_MESSAGE = 'You have made changes to the database. Rows affected: 1'
    ALERT_ERROR_NOT_EXECUTE = 'Error 1: could not execute statement (0 not an error)'


class W3schoolsPage(BasePage):
    """Класс с методами для страницы https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all"""

    def click_button_run_sql(self):
        """
        Клик по кнопке Run SQL
        """
        with allure.step('Клик по кнопке Run SQL'):
            button = self.waits.find_element_with_wait(*W3schoolsLocators.BUTTON_RUN_SQL, 'Не найдена кнопка Run SQL')
            self.elements.mouse_move_to_element(button)
            self.elements.click(button, 'Не удалось кликнуть кнопку Run SQL')

    def get_index_column_in_table(self, name_column) -> int:
        """
        Найти таблице заголовок с названием name_column, и вернуть индекс элемента заголовка

        :param name_column: Наименование колонки
        """
        with allure.step(f'Проверить текст в колонке с названием: "{name_column}"'):
            column_elements = self.waits.find_elements_with_wait(*W3schoolsLocators.ALL_HEADERS_TABLE_NAME,
                                                                 'Не найдены имена заголовков таблицы')
            index_column = None
            with allure.step(f'Получить индекс колонки с названием: "{name_column}"'):
                for num, column_el in enumerate(column_elements):
                    if self.elements.get_text_of_element(column_el) == name_column:
                        index_column = num
                return index_column + 1

    def find_row_in_table_with_text(self, *args):
        """
        Найти запись в таблице по тексту. Принимает аргументы для сравнения полученных значений с ожидаемыми
        """
        row_value = ' '.join(args)
        list_result_rows = self.get_rows_table_elements()
        for el in list_result_rows:
            if self.elements.get_text_of_element(el) == row_value:
                with allure.step('Найдена запись в таблице со значением '):
                    return
        raise ValueError(f'Совпадений со значением "{row_value}" в таблице не найдено')

    def get_index_by_text(self, name_column, search_text):
        """
        Возвращает индекс строки при совпадении по тексту в указанной колонке

        :param name_column: Наименование колонки
        :param search_text: Значение которое нужно найти в колонке
        """
        column_elements = self.get_elements_with_column_name(name_column)
        index = []
        for num, column_el in enumerate(column_elements):
            if search_text == self.elements.get_text_of_element(column_el):
                with allure.step(f'Найден элемент со значением "{search_text}", индекс записи "{num + 1}"'):
                    index.append(num + 1)
        if len(index) == 1:
            return index[0]
        elif len(index) == 0:
            raise ValueError(f'Запись со значением "{search_text}" не найдена в колонке "{name_column}"')
        elif len(index) > 1:
            raise ValueError(f'Найдено "{index}" записей со значением "{search_text}" в колонке "{name_column}"')

    def get_number_matches_in_column(self, name_column, search_text):
        """
        Возвращает количество всех совпадений по тексту в указанной колонке

        :param name_column: Наименование колонки
        :param search_text: Значение которое нужно найти в колонке
        """
        column_elements = self.get_elements_with_column_name(name_column)
        elements_search = [el for el in column_elements if search_text == self.elements.get_text_of_element(el)]
        return len(elements_search)

    def get_elements_with_column_name(self, name_column):
        """
        Возвращает элементы в колонке с наименованием name_column

        :param name_column: Наименование колонки
        """
        index_column = self.get_index_column_in_table(name_column)
        with allure.step(f'Сформировать локатор для поиска всех элементов таблицы в колонке "{name_column}"'):
            locator_column = W3schoolsLocators.ALL_ROWS_TABLE[1] + f"/td[{str(index_column)}]"
        return self.waits.find_elements_with_wait(By.XPATH, locator_column, 'Элементы не найдены')

    def set_request_in_editor(self, request):
        """
        Установить значение в поле SQL редактора

        :param request: SQL запрос
        """
        with allure.step(f'Установить значение в поле ввода SQL запроса: {request}'):
            self.elements.execute_command_js(f'window.editor.setValue("{request}");')

    def set_request_and_run_sql(self, request, type_r=None):
        """
        :param request: SQL запрос
        :param type_r: Тип запроса (SELECT, UPDATE, INSERT)
        """
        self.set_request_in_editor(request)
        if type_r:
            self.check_value_in_editor(type_r)

        self.click_button_run_sql()
        if type_r and type_r != 'SELECT':
            self.check_result(type_r)

    def check_value_in_editor(self, type_r):
        """
        Проверить значение в поле ввода

        :param type_r: Тип запроса (SELECT, UPDATE, INSERT)
        """
        with allure.step(f'Проверка на изменение типа запроса в редакторе "{type_r}"'):
            message_loc = self.elements.get_locator_with_text(W3schoolsLocators.FIND_TEXT_FUNCTION, type_r)
            assert self.waits.is_element_visible(By.XPATH, message_loc,
                                                 f'Не найден тип запроса "{type_r}" в редакторе') is True

    def check_result(self, type_r):
        """
        После выполнения запроса, проверить результирующее текстовое сообщение в 'Result:'

        :param type_r: Тип запроса (SELECT, UPDATE, INSERT)
        """
        expected_message = None
        if type_r == 'INSERT' or type_r == 'UPDATE':
            expected_message = W3schoolsLocators.EXPECTED_RESULT_MESSAGE
        with allure.step(f'Проверка сообщения с результатом выполнения запроса "{type_r}"'):
            message_loc = self.elements.get_locator_with_text(W3schoolsLocators.FIND_TEXT_FUNCTION, expected_message)
            assert self.waits.is_element_visible(By.XPATH, message_loc,
                                                 f'Не найден тип запроса "{expected_message}" в редакторе') is True

    def get_rows_table_elements(self):
        """
        Получить все элементы в таблице
        """
        with allure.step('Получить все элементы таблицы'):
            rows_table = self.waits.find_elements_with_wait(*W3schoolsLocators.ALL_ROWS_TABLE, 'Не найдена таблица')
            return rows_table

    def get_number_table_elements(self):
        """
        Получить количество всех записей в таблице
        """
        with allure.step('Получить количество всех записей в таблице'):
            return len(self.waits.find_elements_with_wait(*W3schoolsLocators.ALL_ROWS_TABLE, 'Не найдена таблица'))

    def check_text_alert(self):
        """
        Получить текс alert и сравнить с ожидаемым результатом
        """
        text_alert = self.elements.get_text_alert_with_wait('Не найден alert')
        assert text_alert == W3schoolsLocators.ALERT_ERROR_NOT_EXECUTE
