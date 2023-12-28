# Enhance the Hierarchical Data Viewer with Recursive Queries

For any connected Snowflake table or view, a second "Path" tab will generate a tabular view with an indented name hierarchy, and the full path of the current entry:

![path](https://miro.medium.com/v2/resize:fit:828/format:webp/1*1HueGBF1Blv_lzSjI_Jw9w.png)

Example of hard-coded generic query for hierarchical data:

```
select repeat('  ', level - 1) || ${child_index} as name,
ltrim(sys_connect_by_path(${child_index}, '.'), '.') as path
from {tableName}
start with ${parent_index} is null
connect by prior ${child_index} = ${parent_index}
order by path;
```

Read more in my blog posts [**How to Query Hierarchical Data in Snowflake**](https://cristian-70480.medium.com/how-to-query-hierarchical-data-in-snowflake-f4ac77f692cb) and [**How to Easily Visualize Hierarchical Tabular Data**](https://medium.com/snowflake/how-to-easily-visualize-hierarchical-tabular-data-90f97e5e4168) about the recursive SQL queries.