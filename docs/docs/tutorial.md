---
sidebar_position: 2
---

# Быстрый запуск проекта Almalife-ETL

## Необходимое окружение

Для запуска проекта необходим [Docker Compose](https://docs.docker.com/compose/).

## Порядок установки и запуска

1. Скопировать файл [.env-example](https://github.com/Enroi/almalife/blob/main/.env-example) в файл .env в корне проекта или рядом с файлом [file_tester.py](https://github.com/Enroi/almalife/blob/main/api_server/file_tester.py)
1. В файле .env установить любой пароль в переменной POSTGRES_PASSWORD
1. В корне проекта запустить команду

    ```bash
    docker compose up -d
    ```

1. Дождаться сообщения в log-ах

    ```code
    Running on http://127.0.0.1:8088
    ```

1. На данном этапе будет запущена инфраструктура работы с данными

## Запуск тестовых примеров

Преобразования данных можно запускать двумя путями:

- файловым запуском
- отправкой конфигурации преобразований на FastAPI сервер

### Файловый запуск преобразований

Для запуска преобразований необходимо запустить на выполнение в Python файл [file_tester.py]https://github.com/Enroi/almalife/blob/main/api_server/file_tester.py) с первым параметром в виде пути к файлу конфигураций преобразований. Пример:

```code
python .\file_tester.py .\etl\configs\xml_to_db.yaml  
```

В результате работы Almalife из файла [usd_currencies.xml](https://github.com/Enroi/almalife/blob/main/source_test_data/test_xmls/usd_currencies.xml) будет создана таблица базы данных usd_currencies которую можно посмотреть через UI Prisma по адресу [http://localhost:8089/#schema=public&table=usd_currencies&view=table](http://localhost:8089/#schema=public&table=usd_currencies&view=table)

### Запуск трансформаций с помощью FastAPI сервера

Almalife может работать в серверном режиме предоставляя REST API метод трансформации.\
Для запуска 