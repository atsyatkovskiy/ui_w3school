#!/bin/bash

# Запуск образа Selenium Standalone Chrome Docker
# docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:3.141.59-20210607

# Собираем image с тегом w3chools_tests_image в текущей директории
docker build -t w3chools_tests_image .

# Запускаем контейнер из image w3chools_tests_image
docker run --name w3chools_tests w3chools_tests_image

# Копируем из контейнера созданный allure-report
docker cp w3chools_tests:/app/allure-report .

allure serve allure-report