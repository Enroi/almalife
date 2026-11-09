---
sidebar_position: 2
---

# Almalife-ETL Quick Start

## Prerequisites

To run the project, you need [Docker Compose](https://docs.docker.com/compose/).

## Installation and Launch Procedure

1. Copy the [.env-example](https://github.com/Enroi/almalife/blob/main/.env-example) file to a .env file in the project root or next to the [file_tester.py](https://github.com/Enroi/almalife/blob/main/api_server/file_tester.py) file
1. Copy the .env-docker-example file with the name .env-docker
1. In the .env and .env-docker files, set any identical password in the POSTGRES_PASSWORD variable
1. In the project root, run the command

    ```bash
    docker compose up -d
    ```

1. Wait for the following message in the logs of the launched superset application:

    ```code
    Running on http://127.0.0.1:8088
    ```

1. At this point, the data processing infrastructure will be up and running

## Running Test Examples

Data transformations can be launched in two ways:

- file-based launch
- sending the transformation configuration to the FastAPI server

### File-Based Transformation Launch

To run transformations, execute the [file_tester.py](https://github.com/Enroi/almalife/blob/main/api_server/file_tester.py) file in Python with the first parameter being the path to the transformation configuration file. Example:

```code
python .\file_tester.py .\etl\configs\xml_to_db.yaml  
```

As a result of Almalife's operation, a usd_currencies database table will be created from the [usd_currencies.xml](https://github.com/Enroi/almalife/blob/main/source_test_data/test_xmls/usd_currencies.xml) file, which can be viewed through the Prisma UI at [http://localhost:8089/#schema=public&table=usd_currencies&view=table](http://localhost:8089/#schema=public&table=usd_currencies&view=table)

### Running Transformations via the FastAPI Server

Almalife can run in server mode, providing a REST API transformation method.\
To run transformations via the FastAPI server in Docker, you need to:

1. Open the [FastAPI server](http://localhost:8090/docs#) link launched in Docker
1. In the opened "Swagger UI" window, select the /api/transform method
1. Click on "Try it out"
1. Select any file from the [transformation configurations](https://github.com/Enroi/almalife/tree/main/api_server/etl/configs) section
1. Check the result in [Prisma Studio UI](http://localhost:8089/)