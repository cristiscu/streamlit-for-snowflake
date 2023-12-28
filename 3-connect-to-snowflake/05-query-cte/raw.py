import json

import _utils
conn = _utils.getConnection()

def getNewSals(conn):

  # get average salary in a department
  def getAvgSal(dept: str) -> float:
    query = ("select floor(avg(salary))"
      + f" from employees where department = '{dept}'")
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()[0][0]

  # get managers with current salaries
  def getManagers():
    managers = []
    query = """
    select department, employee_name, salary
      from employees
      where job = 'MANAGER'
      order by department, employee_name
    """
    cur = conn.cursor()
    cur.execute(query)
    for row in cur:
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


sals = getNewSals(conn)
print(sals)