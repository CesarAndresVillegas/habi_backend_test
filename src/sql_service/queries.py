
SELECT_ESTATES_STATUS = (
    "SELECT "
    "p.address, p.city, s.name AS status, p.price, p.description "
    "FROM status_history sh "
    "INNER JOIN "
    "( "
    "SELECT  id, property_id, status_id, MAX(update_date) as mxdate "
    "FROM status_history "
    "GROUP BY property_id) b ON sh.property_id = b.property_id "
    "AND sh.update_date = b.mxdate "
    "JOIN status s ON sh.status_id = s.id "
    "JOIN property p ON sh.property_id  = p.id "
)

VALID_STATUS = ("pre_venta", "en_venta", "vendido")


def get_estates_query(query_filters: str) -> str:
    """_summary_

    Args:
        query_filters (str): string with the query WHERE condition

    Returns:
        str: mysql query to get estes information
    """
    select = SELECT_ESTATES_STATUS
    group = "GROUP BY p.id"

    if query_filters:
        aux = "AND"
    else:
        aux = "WHERE"

    valid_status = f" s.name in {VALID_STATUS}"

    return f"{select} {query_filters} {aux} {valid_status} {group}"
