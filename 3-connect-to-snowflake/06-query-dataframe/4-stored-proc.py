import json
from snowflake.snowpark import Session
from snowflake.snowpark.functions import sproc

import _utils;
session = _utils.getSession()

@sproc(name="calc_new_sals",
  is_permanent=True, stage_location="@mystage", replace=True,
  packages=["snowflake-snowpark-python==1.10.0"])
def compute(session: Session) -> str:

  # get average salary in a department
  def getAvgSal(dept: str) -> float:
    query = ("select floor(avg(salary))"
      + f" from employees where department = '{dept}'")
    rows = session.sql(query).collect()
    return rows[0][0]

  # get managers with current salaries
  def getManagers():
    managers = []
    query = """
    select department, employee_name, salary
      from employees
      where job = 'MANAGER'
      order by department, employee_name
    """
    rows = session.sql(query).collect()
    for row in rows:
        managers.append({
            "department": str(row[0]),
            "employee_name": str(row[1]),
            "salary": int(row[2])
        })
    return managers

  # get managers with current and projected salaries
  managers = getManagers()
  for manager in managers:
      manager["new_sal"] = (manager["salary"]
        + 0.1 * getAvgSal(manager["department"]))
  return json.dumps(managers, indent=2)


#sals = getNewSals(session)
sals = session.call("calc_new_sals")
print(sals)