import logging
from fastapi import APIRouter
from pyspark.sql import SparkSession, Row
from datetime import datetime, date
import os

router = APIRouter()

@router.post(path = "/api/rates_loading", tags=["ETL"])
async def rates_loading():
    logging.info("Received request for loading currency rates")
    
    spark = SparkSession.builder.create()
    try:
        jdbc_df = spark.read \
            .format("jdbc") \
            .option("dbtable", f"({generate_query()}) as source_query") \
            .option("url", f"jdbc:postgresql://{os.getenv('MARKET_DATA_DB_ADDRESS_OLD')}") \
            .option("user", os.getenv('MARKET_DATA_USER_OLD')) \
            .option("password", os.getenv('MARKET_DATA_PASSWORD_OLD')) \
            .option("driver", "org.postgresql.Driver") \
            .load()
        
        jdbc_df.show(10)
    finally:    
        spark.stop()
    
    return "loaded"

def generate_query():
    return """
        SELECT date, rate
        FROM currency_rate cr 
        INNER JOIN currency c ON cr.cur_id = c.id
        WHERE c."name" = 'Юань'
        ORDER BY cr."date" DESC
        FETCH first 100 ROWS only
    """
