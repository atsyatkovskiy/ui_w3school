import pytest
import allure
from pages.w3schools_page import W3schoolsPage


@pytest.mark.positive
@allure.feature("Вывести все строки с ContactName равной 'Giovanni Rovelli' имеет Address = 'Via Ludovico il Moro 22'")
@allure.story("Вывести все строки таблицы Customers и убедиться, что запись с ContactName равной 'Giovanni Rovelli' "
              "имеет Address = 'Via Ludovico il Moro 22'")
def test_select_all_customers(browser):
    """
    Вывести все строки таблицы Customers и убедиться, что запись с ContactName равной 'Giovanni Rovelli' имеет
    Address = 'Via Ludovico il Moro 22'
    """

    select_all = "SELECT * FROM Customers;"

    w3schools = W3schoolsPage(browser)
    w3schools.open_url()
    w3schools.set_request_and_run_sql(select_all, type_r="SELECT")
    index_row_contact_name = w3schools.get_index_by_text(name_column="ContactName",
                                                         search_text="Giovanni Rovelli")
    index_row_address = w3schools.get_index_by_text(name_column="Address",
                                                    search_text="Via Ludovico il Moro 22")
    assert index_row_contact_name == index_row_address, f"Индексы полученных записей не совпадают " \
                                                        f"{index_row_contact_name} != {index_row_address}"


@pytest.mark.positive
@allure.feature("Вывести строки, где city='London'")
@allure.story("Вывести только те строки таблицы Customers, где city='London'. Проверить, что в таблице ровно 6 записей")
@pytest.mark.parametrize("number_rows_with_london", [6])
def test_select_london(browser, number_rows_with_london):
    """
    Вывести только те строки таблицы Customers, где city='London'. Проверить, что в таблице ровно 6 записей.
    """

    select_london = "SELECT * FROM Customers WHERE city='London';"

    w3schools = W3schoolsPage(browser)
    w3schools.open_url()
    w3schools.set_request_and_run_sql(select_london, type_r="SELECT")
    num_elements_london = w3schools.get_number_matches_in_column(name_column="City", search_text="London")

    assert num_elements_london == number_rows_with_london, \
        f"Количество полученных записей 'City'='London' не совпадают {num_elements_london} != {number_rows_with_london}"


@pytest.mark.positive
@allure.feature('Добавление новой записи')
@allure.story('Добавить новую запись в таблицу Customers и проверить, что эта запись добавилась')
@pytest.mark.parametrize("customer_name", ["one", "one"*2])
@pytest.mark.parametrize("contact_name", ["two"])
@pytest.mark.parametrize("address", ["three"])
@pytest.mark.parametrize("city", ["four"])
@pytest.mark.parametrize("postal_code", ["five"])
@pytest.mark.parametrize("country", ["six"])
def test_add_new_entry(browser, customer_name, contact_name, address, city, postal_code, country):
    """
    Добавить новую запись в таблицу Customers и проверить, что эта запись добавилась
    """

    add_entry = "INSERT INTO Customers(CustomerName, ContactName, Address, City, PostalCode, Country) " \
                f"VALUES ('{customer_name}', '{contact_name}', '{address}', " \
                f"'{city}', '{postal_code}', '{country}');"
    select_without_id = "SELECT CustomerName, ContactName, Address, City, PostalCode, Country FROM Customers;"

    w3schools = W3schoolsPage(browser)
    w3schools.open_url()
    w3schools.click_button_run_sql()
    num_rows_before = w3schools.get_number_table_elements()
    w3schools.set_request_and_run_sql(add_entry, type_r="INSERT")
    w3schools.set_request_and_run_sql(select_without_id, type_r="SELECT")
    w3schools.find_row_in_table_with_text(customer_name, contact_name, address, city, postal_code, country)
    num_rows_after = w3schools.get_number_table_elements()
    assert num_rows_before != num_rows_after, f"Количество полученных записей таблицы 'до' и 'после' изменения " \
                                              f"совпадает {num_rows_before} != {num_rows_after}"


@pytest.mark.positive
@allure.feature('Обновление записи')
@allure.story('Обновить все поля (кроме CustomerID) в любой записи таблицы Customers и проверить,'
              ' что изменения записались в базу')
@pytest.mark.parametrize("customer_name", ["one", "one"*2])
@pytest.mark.parametrize("contact_name", ["two"])
@pytest.mark.parametrize("address", ["three"])
@pytest.mark.parametrize("city", ["four"])
@pytest.mark.parametrize("postal_code", ["five"])
@pytest.mark.parametrize("country", ["six"])
@pytest.mark.parametrize("customer_id", [1])
def test_update_entry(browser, customer_name, contact_name, address, city, postal_code, country, customer_id):
    """
    Обновить все поля (кроме CustomerID) в любой записи таблицы Customers и проверить, что изменения записались в базу.
    """

    update_entry = f"UPDATE Customers SET CustomerName = '{customer_name}', ContactName = '{contact_name}', " \
                   f"Address = '{address}', City = '{city}', PostalCode = '{postal_code}', " \
                   f"Country = '{country}' WHERE CustomerID = '{customer_id}';"
    select_without_id = "SELECT CustomerName, ContactName, Address, City, PostalCode, Country FROM Customers;"

    w3schools = W3schoolsPage(browser)
    w3schools.open_url()
    w3schools.set_request_and_run_sql(update_entry, type_r="UPDATE")
    w3schools.set_request_and_run_sql(select_without_id, type_r="SELECT")
    w3schools.find_row_in_table_with_text(customer_name, contact_name, address, city, postal_code, country)


@pytest.mark.positive
@allure.feature('Выполнение некорректного запроса')
@allure.story('Очистить поле ввода редактора запросов, нажать на кнопку и дождаться сообщения с ошибкой в '
              'разделе Result')
@pytest.mark.parametrize("sql_r_empty_value", [""])
def test_empty_request(browser, sql_r_empty_value):
    """
    Очистить поле ввода редактора запросов, нажать на кнопку и дождаться сообщения с ошибкой в разделе Result
    """

    w3schools = W3schoolsPage(browser)
    w3schools.open_url()
    w3schools.set_request_and_run_sql(sql_r_empty_value)
    w3schools.check_text_alert()
