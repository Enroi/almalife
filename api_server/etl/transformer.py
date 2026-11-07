from io import TextIOWrapper

import yaml
import logging
import os
import re
from pyspark.sql import DataFrame, SparkSession, functions as F
import importlib
import asyncio
from concurrent.futures import ThreadPoolExecutor


_executor = ThreadPoolExecutor(max_workers=4)

def replacer(match) -> str:
    var_name = match.group(1)
    return os.getenv(var_name, f"${{{var_name}}}")

def column_modifications(column_mod_yaml_block: dict, df: DataFrame):
    for column_name, modification in column_mod_yaml_block.items():
        df = df.withColumn(column_name, F.expr(str(modification)))
    return df

def load_from_source(extract_yaml_block: dict, spark: SparkSession) -> DataFrame:
    options: dict = extract_yaml_block.get('options') or {}
    
    df: DataFrame = (
        spark
        .read
        .options(**options)
        .format(extract_yaml_block['format'])
        .load(extract_yaml_block['source'])
    )
    
    if 'select' in extract_yaml_block:
        select = extract_yaml_block["select"]
        df = df.selectExpr(select)
    
    print_schema = extract_yaml_block.get("print_schema", False)
    if str(print_schema).lower() == 'true':
        df.printSchema()

    if 'show_loaded' in extract_yaml_block:
        df.show(extract_yaml_block['show_loaded'])

    if 'drop_columns' in extract_yaml_block:
        drop_columns: list = extract_yaml_block['drop_columns']
        for column in drop_columns:
            df = df.drop(column)
    
    if 'column_modifications' in extract_yaml_block:
        df = column_modifications(extract_yaml_block['column_modifications'], df)
    
    return df

def save_to_target(df: DataFrame, load_yaml_block: dict):
    print_schema = load_yaml_block.get("print_schema", False)
    if str(print_schema).lower() == 'true':
        df.printSchema()

    if 'show_rows_before_save' in load_yaml_block:
        df.show(load_yaml_block['show_rows_before_save'])

    save_format: str = load_yaml_block['format']
    target_name: str = load_yaml_block['target_name']
    write_mode: str = load_yaml_block['write_mode']
    options: dict = load_yaml_block.get('options') or {}

    (df .write
        .mode(write_mode)
        .options(**options)
        .format(save_format)
        .save(target_name))
    
def transform(yaml_config: str) -> str:
    logging.info("started work with config")

    pattern: re.Pattern[str] = re.compile(r'\$\{([^}]+)\}')
    content: str = pattern.sub(replacer, yaml_config)
    config_dict: dict = yaml.safe_load(content)
    
    extract_yaml_block: dict = config_dict['extract']
    load_yaml_block: dict = config_dict['load']

    spark: SparkSession = SparkSession.builder.create()
    try:
        additional_sources = {}
        if 'additional_sources' in config_dict:
            for k, v in (config_dict["additional_sources"]).items():
                additional_df = load_from_source(v, spark)
                additional_sources[k] = additional_df

        df: DataFrame = load_from_source(extract_yaml_block, spark)
        
        if 'business_modification' in config_dict:
            module_name = config_dict['business_modification']['module']
            class_name = config_dict['business_modification']['class']
            method_name = config_dict['business_modification']['method']
            
            parameters = config_dict['business_modification'].get("parameters") or {}
            parameters['extract'] = df
            parameters.update(additional_sources)
            
            business_module = importlib.import_module(module_name)
            cls = getattr(business_module, class_name)
            obj = cls()
            getattr(obj, method_name)(**parameters)
        
        save_to_target(df, load_yaml_block)
    finally:
        spark.stop()
    
    logging.info("finished work with config ")
    return "success"

async def async_transform(yaml_config: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, transform, yaml_config)