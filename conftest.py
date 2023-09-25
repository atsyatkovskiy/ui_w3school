import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOp
from FakeAgent import Fake_Agent


def pytest_addoption(parser):
    """Получение аргументов из командной строки"""
    parser.addoption(
        "--browser-name",
        default="chrome",
        help="Укажите браузер")
    parser.addoption(
        "--remote",
        default=True,
        help="Флаг удаленного запуска драйвера"
    )
    parser.addoption(
        "--remote-url",
        help="URL образа Selenium Standalone Chrome Docker (обязательно с ip адресом, НЕ использовать localhost), "
             "например: --remote-url=http://192.168.1.136:4444/wd/hub"
    )
    parser.addoption(
        "--headless",
        default=True,
        help="Укажите true или false для параметра headless в настройках браузера")
    parser.addoption(
        "--timeout",
        default="30",
        help="Implicitly wait timeout delay"
    )
    parser.addoption(
        "--local-driver",
        default=False,
        help="Абсолютный путь до локального драйвера: /home/chromedriver"
    )
    parser.addoption(
        "--url",
        default="https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all",
        help="URL приложения w3schools.com"
    )


@pytest.fixture()
def random_agent():
    return Fake_Agent().random()


@pytest.fixture(scope='function')
def browser(request, random_agent):
    """Фикстура для запуска драйвера в зависимости от параметров """
    browser = request.config.getoption("--browser-name")
    remote = request.config.getoption("--remote")
    remote_url = request.config.getoption("--remote-url")
    headless = request.config.getoption("--headless")
    timeout = int(request.config.getoption("--timeout"))
    local_driver = request.config.getoption("--local-driver")
    url = request.config.getoption("--url")

    chrome_optons = ChOp()
    chrome_optons.headless = headless
    chrome_optons.add_argument(f"user-agent={random_agent}")
    chrome_optons.add_argument('--ignore-certificate-errors')
    chrome_optons.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_optons.add_experimental_option('useAutomationExtension', False)
    chrome_optons.add_argument('--disable-dev-shm-usage')
    chrome_optons.add_argument("--disable-blink-features=AutomationControlled")
    chrome_optons.add_argument('--disable-web-security')
    chrome_optons.add_argument('--no-sandbox')

    if browser == "chrome" and remote:
        driver = webdriver.Remote(
                    command_executor=remote_url,
                    desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True},
                    options=chrome_optons
        )
    elif browser == "chrome" and local_driver:
        driver = webdriver.Chrome(options=chrome_optons, executable_path=local_driver)
    else:
        raise pytest.UsageError("Для локального запуска --browser - chrome")

    driver.maximize_window()
    yield {
        "driver": driver,
        "url": url,
        "timeout": timeout
    }
    driver.quit()
