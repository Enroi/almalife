---
sidebar_position: 4
---

# Бизнес трансформации

Основной смысл данного проекта показать удобство использования Apache Spark для задач ETL (Extract Transform Loading).\
Однако этап Transform часто не может быть описан простыми SQL командами, которые можно описать в [yaml файле](https://github.com/Enroi/almalife/blob/main/api_server/etl/configs/base_example.yaml).\
Проект Almalife дает возможность включить в этап Transform, процесса ETL, этап более сложных преобразований, в рамках данного проекта называемых "Бизнес Транформации". Пример файла расширения трансформаций для добавления бизнес логики показан в файле [worker_module.py](https://github.com/Enroi/almalife/blob/main/api_server/etl/business_methods/worker_module.py).\
Пример конфигурации запуска бизнес преобразования показан в файле [base_example.yaml](https://github.com/Enroi/almalife/blob/main/api_server/etl/configs/base_example.yaml).
