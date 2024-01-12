import html2text
from requests_html import HTMLSession

PAGES = [
    "https://quickstarts.snowflake.com/guide/data_engineering_pipelines_with_snowpark_python",
    "https://quickstarts.snowflake.com/guide/cloud_native_data_engineering_with_matillion_and_snowflake",
    "https://quickstarts.snowflake.com/guide/data_engineering_with_apache_airflow",
    "https://quickstarts.snowflake.com/guide/getting_started_with_dataengineering_ml_using_snowpark_python",
    "https://quickstarts.snowflake.com/guide/data_engineering_with_snowpark_python_and_dbt"
]
for url in PAGES:
    session = HTMLSession()
    response = session.get(url, timeout=30)
    response.html.render()
    h = html2text.HTML2Text()
    markdown_content = h.handle(response.html.raw_html.decode("utf-8"))

    filename = url.split("/")[-1] + ".md"
    filename = f"./pages/{filename}"
    print(f"Downloading {url} into {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
