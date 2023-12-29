# Push Python Code as a Stored Procedure with Snowpark

Creates and executes a stored procedure in Snowflake using a Snowpark decorator:

```
@sproc(name="calc_new_sals",
  is_permanent=True, stage_location="@mystage", replace=True,
  packages=["snowflake-snowpark-python==1.10.0"])
def compute(session: Session) -> str:
  ...

sals = session.call("calc_new_sals")
print(sals)
```

The **stored-proc.py** file encapsulates all fragmented queries from the **raw.py** file, and executes the whole code remote, in the Snowflake virtual warehouse, closer to the data.

## Actions

From the local subfolder, run from a Terminal window **`python raw.py`**, then  **`python stored-proc.py`**.
