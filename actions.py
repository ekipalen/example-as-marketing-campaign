"""
An example Action to assist with customer data and marketing campaigns.
Queries are stored in a separate DB and LLM doesn't create actual DB queries but uses the predifined ones.

Check out the base guidance on AI Actions in our main repository readme:
https://github.com/robocorp/robocorp/blob/master/README.md
"""

from robocorp.actions import action
import sqlite3
from pydantic import BaseModel
from typing import Any, List


class QueryExecutionParams(BaseModel):
    query_name: str
    params: List[Any]


@action(is_consequential=False)
def get_allowed_queries() -> str:
    """Initial Action, other actions are not allowed before executing this. Fetch allowed db queries and their descriptions.

    Args:
        None.

    Returns:
        str: A detailed formatted string listing all the allowed queries.
    """
    conn = sqlite3.connect("allowed_queries_with_json.db")
    cursor = conn.cursor()

    cursor.execute("SELECT query_name, query_sql, description FROM allowed_queries")
    queries = cursor.fetchall()

    conn.close()

    if queries:
        detailed_queries = ["Allowed Queries with Details:"]
        for name, sql, description in queries:
            detailed_queries.append(f"Query Name: {name}\nDescription: {description}\n")
        print("\n".join(detailed_queries))
        return "\n".join(detailed_queries)
    else:
        return "No allowed queries found."


@action(is_consequential=False)
def execute_allowed_query(execution_params: QueryExecutionParams) -> str:
    """
    Executes named queries with 0-4 params. Action "get_allowed_queries" needs to be executed once before this!

    Args:
        execution_params: Query name, params list.

    Returns:
        Query results or error.

    """
    allowed_db_path = (
        "allowed_queries_with_json.db"  # Path to your DB with allowed queries
    )
    target_db_path = "marketing_campaign_demo.db"  # Path to your main DB for execution

    conn_allowed = sqlite3.connect(allowed_db_path)
    cursor_allowed = conn_allowed.cursor()

    cursor_allowed.execute(
        "SELECT query_sql FROM allowed_queries WHERE query_name = ?",
        (execution_params.query_name,),
    )
    allowed_query = cursor_allowed.fetchone()

    conn_allowed.close()

    if not allowed_query:
        return "Query not allowed or does not exist."

    query_sql = allowed_query[0]

    # Adjust parameters for queries expecting an upper limit
    if execution_params.query_name in [
        "purchases_by_amount_range",
        "customers_by_email_open_rate",
    ]:
        # Check if the upper limit flag and value are set to 0, None respectively
        if len(execution_params.params) >= 4 and execution_params.params[3] == 0:
            # Set the upper limit flag to 1 and use a very high value to effectively ignore the upper limit
            execution_params.params[2] = 1
            execution_params.params[3] = (
                100000  # Or any other high number that suits your data
            )

    try:
        conn_target = sqlite3.connect(target_db_path)
        cursor_target = conn_target.cursor()
        print(execution_params.params)
        # Execute the query with the dynamic number of parameters
        cursor_target.execute(query_sql, execution_params.params)

        results = cursor_target.fetchall()
        result_str = "\n".join(str(row) for row in results)

        conn_target.close()
        return result_str

    except sqlite3.Error as e:
        return f"An error occurred: {e}"
