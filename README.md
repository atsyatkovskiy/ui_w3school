## Проект тестового задания автоматизированного тестирования w3schools.com  

### Описание проекта
+ В директории ./helpers:
  - helpers/elements_helpers.py - Модуль с вспомогательными классами для поиска элементов
  - helpers/waits.py - Модуль с вспомогательными классами для поиска элементов
+ В директории ./pages:
  - pages/base_page.py - общий базовый класс
  - pages/w3schools_page.py - базовый класс w3schools
+ В директории ./tests_ui/test_all.py тесты:
  - ::test_select_all_customers - Вывести все строки таблицы Customers и убедиться, что запись с ContactName равной 'Giovanni Rovelli' имеет
    Address = 'Via Ludovico il Moro 22'
  - ::test_select_london - Вывести только те строки таблицы Customers, где city='London'. Проверить, что в таблице ровно 6 записей
  - ::test_add_new_entry - Добавить новую запись в таблицу Customers и проверить, что эта запись добавилась
  - ::test_update_entry - Обновить все поля (кроме CustomerID) в любой записи таблицы Customers и проверить, что изменения записались в базу
  - ::test_empty_request - Очистить поле ввода редактора запросов, нажать на кнопку и дождаться сообщения с ошибкой в разделе Result

### Запуск в docker контейнере selenium/standalone-chrome

Чтобы запустить тесты в docker контейнере используя selenium/standalone-chrome:

1) Узнать локальный IP адрес и прописать URL запуска тестов (с localhost работать не будет) в Dockerfile строка 13, параметр "--remote-url". 
Чтобы узнать IP на Mac устройстве выполнить команду: 
 
``ifconfig | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 127.0.0.1 | awk '{ print $2 }' | cut -f2 -d: | head -n1``

2) Запустить контейнер с Chrome browser (selenium/standalone-chrome): 

``docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:3.141.59-20210607``

3) Перейти по URL-у и проверить запущен ли контейнер: 

``http://localhost:4444/wd/hub/static/resource/hub.html``

4) Собираем image с тегом w3chools_tests_image в root директории тестами (где находится Dockerfile): 

``docker build -t w3chools_tests_image .``

5) Запустить контейнер с тестами:

``docker run --name w3chools_tests w3chools_tests_image``

Запуск можно осуществить через скрипт ``run_tests_in_docker.sh``, но обязательно перед этим выполнить первый пункт с определением IP адреса. 
Запуск тестов будет выполнен в многопоточном режиме, и с формированием allure отчета (для корректной работы требуется установка allure) 

### Настройка локального окружения в IDE. Установка пакетов и виртуального окружения
- Установить и активировать виртуальное окружение (Linux/Mac):

```
python3 -m venv venv
source venv/bin/activate
```

- Обновить PIP и установить зависимости:

```
pip install -U pip
pip install -r requirements.txt
```
