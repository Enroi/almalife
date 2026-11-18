from pyspark.sql import SparkSession, DataFrame, Column as SparkColumn, Window
from pyspark.sql.functions import col, lit, row_number
import openpyxl as opl
import openpyxl.worksheet.worksheet as oplws
import formualizer as fz
from typing import NamedTuple
import logging
from collections import defaultdict
import sys
import re


SYNTHETIC_COLUMN_NAME = "added_for_range_links"

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


def convert_raw_to_spark_column(ast: fz.ASTNode, 
                                df: DataFrame, 
                                excel_ranges_as_dfs: dict[str, DataFrame]
                                ) -> tuple[SparkColumn | None, DataFrame] :
    node_type = ast.node_type()
    match node_type:
        case'BinaryOp':
            node_operator = ast.get_operator()
            if node_operator is not None:
                left = convert_raw_to_spark_column(ast.children()[0], df, excel_ranges_as_dfs)
                right = convert_raw_to_spark_column(ast.children()[1], df, excel_ranges_as_dfs)
                match node_operator: 
                    case '+': result_formula = lit(left) + lit(right)
                    case '-': result_formula = lit(left) - lit(right)
                    case '/': result_formula = lit(left) / lit(right)
                    case '*': result_formula = lit(left) * lit(right)
                    case _: result_formula = None
                return result_formula, df
        case 'Literal':
            return ast.get_literal_value(), df
        case 'Reference':
            rf = ast.get_reference()
            match rf:
                case fz.CellRef():
                    c = rf.col # type: ignore
                    return col(df.columns[c - 1]), df
                case fz.TableRef():
                    linked_df_name = rf.name
                    if linked_df_name is not None:
                        linked_df = excel_ranges_as_dfs[linked_df_name]
                        spec = rf.spec
                        if spec is not None:
                            cols_spec_list: list[str] = spec.split(",")
                            if len(cols_spec_list) == 2 and cols_spec_list[0] == '[@]':
                                matches = re.search(r'\[(.+)\]', cols_spec_list[1])
                                if matches is not None and len(matches.groups()) == 1:
                                    join_column_name = matches[1]
                                    df = df.join(linked_df, on=SYNTHETIC_COLUMN_NAME, how="left")
                                    return col(join_column_name), df
    return None, df


def add_column(raw_excel_column: RawExcelColumn, df: DataFrame, excel_ranges_as_dfs: dict[str, DataFrame]) -> DataFrame:
    if raw_excel_column.ast is not None:
        ast: fz.ASTNode = raw_excel_column.ast
        spark_column, df = convert_raw_to_spark_column(ast, df, excel_ranges_as_dfs)
        spark_column: SparkColumn | None
        
        if spark_column is not None:
            df = df.withColumn(raw_excel_column.name, spark_column)
            
    return df


def add_synthetic_column(df: DataFrame) -> DataFrame:
    synthetic_column = lit(1)
    df = df.withColumn(
        SYNTHETIC_COLUMN_NAME, 
        row_number().over(Window.orderBy(synthetic_column)),
        )
    return df
    

def get_named_ranges_dfs(workbook, file_path, spark: SparkSession):
    result_dict = {}
    for ws in workbook.worksheets:
        ws: oplws.Worksheet
        tables = ws.tables
        for table_name in tables:
            table = tables[table_name]
            data_address = f"{ws.title}!{table.ref}"
            df = (spark.read
                .format("excel")
                .option("dataAddress", data_address)
                .load(file_path))
            df = add_synthetic_column(df)
            df.show()
            result_dict[table_name] = df
    return result_dict


def do_work(file_path: str, sheet_name: str):
    spark = SparkSession.builder.getOrCreate()
    
    workbook_with_dfn: opl.Workbook = opl.load_workbook(file_path)
    excel_ranges_as_dfs: dict[str, DataFrame] = get_named_ranges_dfs(workbook_with_dfn, file_path, spark)
    
    workbook: opl.Workbook = opl.load_workbook(file_path, data_only=False, read_only=True)
    sheet: oplws.Worksheet = workbook[sheet_name]
    columns_dict: defaultdict[str, list[RawExcelColumn]] = get_columns(sheet, sheet_name)

    df = (spark.read
        .format("excel")
        .load(file_path))

    df = add_synthetic_column(df)

    for column in columns_dict[sheet_name]:
        df = add_column(column, df, excel_ranges_as_dfs)

    df.show()
    df.printSchema()

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    if len(sys.argv) == 3:
        file_path = sys.argv[1]
        sheet_name = sys.argv[2]
        do_work(file_path, sheet_name)
