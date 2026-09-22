from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def filter_open_cases(cases: DataFrame) -> DataFrame:
    return cases.filter(F.col("status") == "OPEN")


def join_cases_with_employees(cases: DataFrame, employees: DataFrame) -> DataFrame:
    return cases.join(employees, on="employee_id", how="left")


def aggregate_cases_by_priority(cases: DataFrame) -> DataFrame:
    return (
        cases.groupBy("priority")
        .agg(F.count("case_id").alias("case_count"))
        .orderBy("priority")
    )


def add_employee_case_rank(cases: DataFrame) -> DataFrame:
    window = Window.partitionBy("employee_id").orderBy(
        F.when(F.col("priority") == "HIGH", 1)
        .when(F.col("priority") == "MEDIUM", 2)
        .when(F.col("priority") == "LOW", 3)
        .otherwise(4)
    )

    return cases.withColumn(
        "priority_rank",
        F.row_number().over(window),
    )


def deduplicate_cases(cases: DataFrame) -> DataFrame:
    return cases.dropDuplicates(["case_id"])


def handle_nulls(cases: DataFrame) -> DataFrame:
    return cases.fillna(
        {
            "status": "UNKNOWN",
            "priority": "UNKNOWN",
            "category": "UNKNOWN",
        }
    )