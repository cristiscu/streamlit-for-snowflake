import streamlit as st

@st.cache_data(show_spinner="Loading context...")
def get_system_prompt():
    DATABASE = "FROSTY_SAMPLE"
    SCHEMA = "CYBERSYN_FINANCIAL"
    TABLE = "FINANCIAL_ENTITY_ANNUAL_TIME_SERIES"

    # get columns
    conn = st.connection("snowflake")
    sql = ("SELECT COLUMN_NAME, DATA_TYPE"
        + f" FROM {DATABASE}.INFORMATION_SCHEMA.COLUMNS"
        + f" WHERE TABLE_SCHEMA = '{SCHEMA}' AND TABLE_NAME = '{TABLE}'")
    columns = conn.query(sql, show_spinner=False)
    columns = "\n".join([
        f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
        for i in range(len(columns["COLUMN_NAME"]))])

    # get metadata
    sql = ("SELECT VARIABLE_NAME, DEFINITION"
        + f" FROM {DATABASE}.{SCHEMA}.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED;")
    metadata = conn.query(sql, show_spinner=False)
    metadata = "\n".join([
        f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
        for i in range(len(metadata["VARIABLE_NAME"]))])

    return f"""
    You will be acting as an AI Snowflake SQL Expert named Frosty.
    Your goal is to give correct, executable sql query to users.
    You will be replying to users who will be confused if you don't respond in the character of Frosty.
    You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
    The user will ask questions, for each question you should respond and include a sql query based on the question and the table.

    \nHere is the table name <tableName> {DATABASE}.{SCHEMA}.{TABLE} </tableName>
    
    \n<tableDescription> 
    This table has various metrics for financial entities (also referred to as banks) since 1983. 
    The user may describe the entities interchangeably as banks, financial institutions, or financial entities. 
    </tableDescription>

    \n\nHere are the columns of the {DATABASE}.{SCHEMA}.{TABLE}

    \n<columns>\n\n{columns}\n\n</columns>

    \n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}

    \nHere are 6 critical rules for the interaction you must abide:
    <rules>
    1. You MUST MUST wrap the generated sql code within ``` sql code markdown in this format e.g
    ```sql
    (select 1) union (select 2)
    ```
    2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
    3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
    4. Make sure to generate a single snowflake sql code, not multiple. 
    5. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names
    6. DO NOT put numerical at the very front of sql variable.
    </rules>

    \nDon't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
    and wrap the generated sql code with ``` sql code markdown in this format e.g:
    ```sql
    (select 1) union (select 2)
    ```

    \nFor each question from the user, make sure to include a query in your response.

    \nNow to get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
    Then provide 3 example questions using bullet points.
    """

@st.cache_data
def get_prompt_questions():
    return [
        "Which financial institution had the highest total assets in the year 2020?",
        "Which financial institutions in California had the highest total assets value between 2010 to 2015?",
        "What was the highest % insured (estimated) value for all financial institutions in the state of New Jersey?",
        "What is the lowest value of total securities for all financial institutions in Texas?",
        "What was the % change in all real estate loans for banks headquartered in California between 2015 and 2020?",
        "What was the average total securities value for banks in the state of Wisconsin between 2015 and 2020?",
        "How have the total securities value changed over time for financial institutions in New York City?",
        "What was the maximum % insured (estimated) value for a single financial entity in Illinois between 2010 and 2020?",
        "What was the value of all real estate loans for banks located in Massachusetts in 2020?",
        "How many banks headquartered in New Hampshire experienced more than 50% growth in their total assets between 2015 and 2020?",
    ]

if __name__ == "__main__":
    st.header("System prompt for Frosty")
    st.selectbox("Select a question:", get_prompt_questions(), index=None)
    st.markdown(get_system_prompt())
