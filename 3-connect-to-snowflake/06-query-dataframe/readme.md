# Build a Complex Query with the Snowpark DataFrame API

Alternative to a more complex SQL query with a CTE (see the **cte.py** file) using the Snowpark DataFrame API (see the **data-frame.py** file).

The query we built:

```
with q1 as (
  select department, floor(avg(salary)) as avg_sal
    from employees
    group by department
    order by department)
    
select e.department, e.employee_name, e.salary,
  e.salary + (0.1 * q1.avg_sal) as new_sal
  from employees e
  join q1 on q1.department = e.department
  where job = 'MANAGER'
  order by department, employee_name;
```