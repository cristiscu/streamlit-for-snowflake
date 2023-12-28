from snowflake.snowpark.functions import call_function, col
import _utils;
session = _utils.getSession()

avgSales = (session
  .table("EMPLOYEES")
  .select("DEPARTMENT", "SALARY")
  .group_by("DEPARTMENT")
  .agg({ "SALARY": "avg" })
  .select("DEPARTMENT", call_function("floor", col("AVG(SALARY)"))
  .alias("AVG_SAL"))
  .sort("DEPARTMENT"))
#avgSales.show()

managers = (session
  .table("EMPLOYEES")
  .select("DEPARTMENT", "EMPLOYEE_NAME", "SALARY")
  .filter(col("JOB") == 'MANAGER')
  .sort("DEPARTMENT", "EMPLOYEE_NAME"))
#print(managers.collect())

(managers
  .join(avgSales, managers.department == avgSales.department)
  .select(managers.department.alias("DEPARTMENT"),
          managers.employee_name,
          managers.salary,
          (managers.salary + (0.1 * col("AVG_SAL"))).alias("NEW_SAL"))
  .show())





