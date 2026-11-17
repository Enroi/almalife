from pyspark.sql import SparkSession, Row, DataFrame, Column as SparkColumn
from pyspark.sql.functions import expr, lit
from datetime import datetime, date
import openpyxl as opl
import openpyxl.worksheet.worksheet as oplws
import openpyxl.cell.cell as oplcl
from typing import NamedTuple
import formualizer as fz
from formualizer.visitor import VisitControl


class RawExcelColumn(NamedTuple):
    column_index: int
    name: str
    # Формула в виде текста как есть из Excel файла
    formula: str | None 
    ast: fz.ASTNode


def convert_raw_to_spark_column(ast: fz.ASTNode) -> SparkColumn | None:
    node_type = ast.node_type()
    match node_type:
        case'BinaryOp':
            node_operator = ast.get_operator()
            if node_operator is not None:
                left = convert_raw_to_spark_column(ast.children()[0])
                right = convert_raw_to_spark_column(ast.children()[1])
                match node_operator: 
                    case '+': result_formula = lit(left) + lit(right)
                    case '-': result_formula = lit(left) - lit(right)
                    case '/': result_formula = lit(left) / lit(right)
                    case '*': result_formula = lit(left) * lit(right)
                    case _: result_formula = None
                return result_formula
        case 'Literal':
            return ast.get_literal_value()
    return None


def get_columns(sheet: oplws.Worksheet) -> list[RawExcelColumn]:
    columns: list[RawExcelColumn] = []
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
                name = str(header_cell.value),
                formula = formula,
                ast = ast,
                )
            columns.append(column)
    return columns


def add_column(raw_excel_column: RawExcelColumn, df: DataFrame) -> DataFrame:
    ast: fz.ASTNode = raw_excel_column.ast
    spark_column: SparkColumn | None = convert_raw_to_spark_column(ast)
    if spark_column is not None:
        df = df.withColumn(raw_excel_column.name, spark_column)
    
    return df


def do_work():
    spark = SparkSession.builder.getOrCreate()

    df = spark.createDataFrame([
        Row(a=1, b=2.0, ),
        Row(a=2, b=3.0, ),
        Row(a=4, b=5.0, ),
    ])
    
    workbook: opl.Workbook = opl.load_workbook("simple.xlsx", data_only=False, read_only=True)
    sheet: oplws.Worksheet = workbook['Sheet1']

    columns: list[RawExcelColumn] = get_columns(sheet)
    for column in columns:
        df = add_column(column, df)

    print("-" * 82)

    df.show()
    df.printSchema()
    

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    do_work()
