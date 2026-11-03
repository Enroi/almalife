from pyspark.sql import DataFrame


class Worker:
    
    def do_work(self, **kwargs):
        print(kwargs['name_of_param'])