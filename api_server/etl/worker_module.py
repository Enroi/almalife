from pyspark.sql import DataFrame


class Worker:
    
    def do_work(self, df: DataFrame):
        print("i am working")