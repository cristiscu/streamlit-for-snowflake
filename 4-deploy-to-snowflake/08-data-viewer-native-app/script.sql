-- consumer script, automatically triggered after an APPLICATION is created in the deploy script
CREATE APPLICATION ROLE hierarchical_data_role;

-- create versioned schema
CREATE OR ALTER VERSIONED SCHEMA app;
GRANT USAGE ON SCHEMA app
  TO APPLICATION ROLE hierarchical_data_role;

-- create secure views
CREATE SECURE VIEW app.emp_man AS
  SELECT e.employee_name as employee,
    m.employee_name as manager
  FROM private.employees e
    LEFT JOIN private.employees m
    ON e.manager_id = m.employee_id;
GRANT SELECT ON VIEW app.emp_man
  TO APPLICATION ROLE hierarchical_data_role;

CREATE SECURE VIEW app.emp_dept AS
  select '(company)' as child, null as parent
  union select distinct department, '(company)' from private.employees
  union select employee_name, department from private.employees;
GRANT SELECT ON VIEW app.emp_dept
  TO APPLICATION ROLE hierarchical_data_role;

-- create secure procedure
create secure procedure app.show_path(
  tableName varchar, child varchar, parent varchar)
  returns table(name varchar, path varchar)
  language sql
as
begin
  let stmt varchar := 'select repeat(''  '', level - 1) || ' || :child || ' as name,'
    || ' ltrim(sys_connect_by_path(' || :child || ', ''.''), ''.'') as path'
    || ' from ' || :tableName
    || ' start with ' || :parent || ' is null'
    || ' connect by prior ' || :child || ' = ' || :parent
    || ' order by path';
  let rs resultset := (execute immediate :stmt);
  return table(rs);
end;
GRANT USAGE ON PROCEDURE app.show_path(varchar, varchar, varchar)
  TO APPLICATION ROLE hierarchical_data_role;

-- add Streamlit object
CREATE STREAMLIT app.hierarchical_data
  FROM '/'
  MAIN_FILE = '/app.py';
GRANT USAGE ON STREAMLIT app.hierarchical_data
  TO APPLICATION ROLE hierarchical_data_role;
