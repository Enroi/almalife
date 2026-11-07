---
sidebar_position: 2
---

# Быстрый запуск проекта Almalife-ETL

## Необходимое окружение

Для запуска проекта необходим [Docker Compose](https://docs.docker.com/compose/).

## Порядок установки и запуска

1. Скопировать файл [.env-example](https://github.com/Enroi/almalife/blob/main/.env-example) в файл .env в корне проекта или рядом с файлом [file_tester.py](https://github.com/Enroi/almalife/blob/main/api_server/file_tester.py)
1. Файл .env-example скопировать с именем .env
1. Файл .env-docker-example скопировать с именем .env-docker
1. В файлах .env и .env-docker установить любой одинаковый пароль в переменной POSTGRES_PASSWORD
1. В корне проекта запустить команду

    ```bash
    docker compose up -d
    ```

1. Дождаться сообщения в log-ах запущенного приложения superset текста:

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
Для запуска трансформаций через FastAPI сервер в Docker необходимо:

1. Открыть ссылку [FastAPI сервера](http://localhost:8090/docs#) запущенного в Docker
1. В открывшемся окне "Swagger UI" выбрать метод /api/transform
1. Нажать на "Try it out"
1. Выбрать любой файл из раздела [конфигураций трансформации](https://github.com/Enroi/almalife/tree/main/api_server/etl/configs)
1. Проверить результат в [UI Prisma Studio](http://localhost:8089/)
