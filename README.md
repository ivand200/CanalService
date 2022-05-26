# Script for google sheet

## Запуск

***sudo docker build -t canalservice .***
***sudo docker run -it canalservice /bin/bash***
***python manage/py runapscheduler***

## Таблица обновляеся с понедельника по пятницу в 10:00 часов

## Сроки по договорам проверяются с понедельника по пятницу в 12:00, если доставка просрочена отправляется собщение в телеграм

## Инструкция telegram_send

*telegram-send --configure* - попросит токен телеграм бота, даст код который нужно ввести боту.
