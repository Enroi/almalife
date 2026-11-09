---
sidebar_position: 4
---

# Business Transformations

The main purpose of this project is to demonstrate the convenience of using Apache Spark for ETL (Extract Transform Loading) tasks.\
However, the Transform stage often cannot be described by simple SQL commands that can be specified in a [YAML file](https://github.com/Enroi/almalife/blob/main/api_server/etl/configs/base_example.yaml).\
The Almalife project makes it possible to include more complex transformations — referred to within this project as "Business Transformations" — in the Transform stage of the ETL process. An example of a transformation extension file for adding business logic is shown in the [worker_module.py](https://github.com/Enroi/almalife/blob/main/api_server/etl/business_methods/worker_module.py) file.\
An example of a configuration for launching a business transformation is shown in the [base_example.yaml](https://github.com/Enroi/almalife/blob/main/api_server/etl/configs/base_example.yaml) file.