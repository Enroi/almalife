import logging
from fastapi import APIRouter
from pyspark.sql import SparkSession, Row
from datetime import datetime, date



router = APIRouter()

@router.post(path = "/api/rates_loading", tags=["ETL"])
async def rates_loading():
    logging.info("Received request for loading currency rates")
    spark = SparkSession.builder.getOrCreate()
    
    jdbc_df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://172.22.130.235:31105/calendars_db") \
        .option("dbtable", "public.calendar_days") \
        .option("user", "calendar_service_user") \
        .option("password", "o2IEVQVrvWuVvcDpVBkW") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    jdbc_df.show(10)
    
    return "loaded"