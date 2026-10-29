# noinspection PyPackageRequirements

from pyspark.sql import SparkSession, Row
from datetime import datetime, date

spark = SparkSession.builder.getOrCreate()

df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])

df.show()
df.printSchema()

"""
jdbc_df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://172.22.130.235:31105/calendars_db") \
    .option("dbtable", "public.calendar_days") \
    .option("user", "calendar_service_user") \
    .option("password", "o2IEVQVrvWuVvcDpVBkW") \
    .option("driver", "org.postgresql.Driver") \
    .load()

jdbc_df.show(10)
"""
