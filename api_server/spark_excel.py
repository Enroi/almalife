from pyspark.sql import SparkSession, DataFrame, Column as SparkColumn
from pyspark.sql.functions import col, lit
from datetime import datetime, date
import openpyxl as opl
import openpyxl.worksheet.worksheet as oplws
import formualizer as fz
from typing import NamedTuple
import logging
from collections import defaultdict


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(thread)d - %(message)s',
    )

class RawExcelColumn(NamedTuple):
    column_index: int
    name: str
    # Формула в виде текста как есть из Excel файла
    formula: str | None 
    ast: fz.ASTNode | None


def get_columns(sheet: oplws.Worksheet, source_name: str) -> defaultdict:
    columns: defaultdict = defaultdict(list[RawExcelColumn])
    for cell_index in range(sheet.min_column, sheet.max_column + 1):
        header_cell = sheet.cell(1, cell_index)
        second_cell = sheet.cell(2, cell_index)
        formula: str | None = None
        ast: fz.ASTNode | None = None  
        if second_cell.data_type == 'f':
            formula = str(second_cell.value)
            ast = fz.parse(formula)
        column = RawExcelColumn(
            column_index = cell_index, 
            name = str(header_cell.value) + "_calculated",
            formula = formula,
            ast = ast,
            )
        columns[source_name].append(column)
    return columns


def convert_raw_to_spark_column(ast: fz.ASTNode, df: DataFrame) -> SparkColumn | None:
    node_type = ast.node_type()
    match node_type:
        case'BinaryOp':
            node_operator = ast.get_operator()
            if node_operator is not None:
                left = convert_raw_to_spark_column(ast.children()[0], df)
                right = convert_raw_to_spark_column(ast.children()[1], df)
                match node_operator: 
                    case '+': result_formula = lit(left) + lit(right)
                    case '-': result_formula = lit(left) - lit(right)
                    case '/': result_formula = lit(left) / lit(right)
                    case '*': result_formula = lit(left) * lit(right)
                    case _: result_formula = None
                return result_formula
        case 'Literal':
            return ast.get_literal_value()
        case 'Reference':
            rf = ast.get_reference()
            c = rf.col # type: ignore
            return col(df.columns[c - 1])
        case _: 
            return None


def add_column(raw_excel_column: RawExcelColumn, df: DataFrame) -> DataFrame:
    if raw_excel_column.ast is not None:
        ast: fz.ASTNode = raw_excel_column.ast
        spark_column: SparkColumn | None = convert_raw_to_spark_column(ast, df)
        if spark_column is not None:
            df = df.withColumn(raw_excel_column.name, spark_column)
    return df


def do_work(file_path: str, sheet_name: str):
    
    workbook: opl.Workbook = opl.load_workbook(file_path, data_only=False, read_only=True)
    sheet: oplws.Worksheet = workbook[sheet_name]
    columns_dict: defaultdict[str, list[RawExcelColumn]] = get_columns(sheet, sheet_name)

    spark = SparkSession.builder.getOrCreate()

    df = (spark.read
        .format("excel")
        .load(file_path))

    for column in columns_dict[sheet_name]:
        df = add_column(column, df)

    df.show()
    df.printSchema()

if __name__ == '__main__':

    from dotenv import load_dotenv
    load_dotenv()
    
    do_work("source_test_data/test_excel/simple.xlsx", 'Sheet1')
