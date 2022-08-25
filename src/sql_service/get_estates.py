import os
import mysql.connector
from queries import get_estates_query


def get_estates(event: dict, context: dict) -> list:
    """_summary_

    Args:
        event (dict): expected a dictionary with query string and
                      with query params dictionary
        context (dict): non relevant.
                        Used to convention on AWS lambda function

    Returns:
        list: properties information
    """
    filters = event.get("query_filters")

    query = get_estates_query(filters)

    params = event.get("query_params")

    return execute_basic_select(query, params)


def execute_basic_select(query: str, params: dict) -> list:
    """_summary_

    Args:
        query (str): mysql SELECT fetch all query
        params (dict): mysql SELECT fetch all query

    Returns:
        list: query result on a list of list
    """
    my_db = mysql.connector.connect(host=os.getenv("HOST"),
                                    port=os.getenv("PORT"),
                                    database=os.getenv("DATABASE"),
                                    user=os.getenv("DB_USER"),
                                    password=os.getenv("DB_PASS"))
    my_cursor = my_db.cursor()
    my_cursor.execute(query, params)
    return my_cursor.fetchall()
