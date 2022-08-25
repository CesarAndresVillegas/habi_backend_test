import pytest
import sys

sys.path.append('src')
import sql_service.queries as queries


@pytest.mark.parametrize("subquery_filters, expected", [
    (
        "",
        ("SELECT p.address, p.city, s.name AS status, p.price, p.description "
         "FROM status_history sh "
         "INNER JOIN "
         "(SELECT id, property_id, status_id, MAX(update_date) as mxdate "
         "FROM status_history GROUP BY property_id) b ON "
         "sh.property_id = b.property_id AND sh.update_date = b.mxdate "
         "JOIN status s ON sh.status_id = s.id "
         "JOIN property p ON sh.property_id = p.id "
         "WHERE "
         "s.name in ('pre_venta', 'en_venta', 'vendido') GROUP BY p.id")
    ),
    (
        "WHERE city = %(city)s AND year = %(year)s AND s.name = %(status)s",
        ("SELECT p.address, p.city, s.name AS status, p.price, p.description "
         "FROM status_history sh "
         "INNER JOIN "
         "(SELECT id, property_id, status_id, MAX(update_date) as mxdate "
         "FROM status_history GROUP BY property_id) b ON "
         "sh.property_id = b.property_id AND sh.update_date = b.mxdate "
         "JOIN status s ON sh.status_id = s.id "
         "JOIN property p ON sh.property_id = p.id "
         "WHERE "
         "city = %(city)s AND year = %(year)s AND s.name = %(status)s AND "
         "s.name in ('pre_venta', 'en_venta', 'vendido') GROUP BY p.id")
    ),
    (
        "WHERE city = %(city)s",
        ("SELECT p.address, p.city, s.name AS status, p.price, p.description "
         "FROM status_history sh "
         "INNER JOIN "
         "(SELECT id, property_id, status_id, MAX(update_date) as mxdate "
         "FROM status_history GROUP BY property_id) b ON "
         "sh.property_id = b.property_id AND sh.update_date = b.mxdate "
         "JOIN status s ON sh.status_id = s.id "
         "JOIN property p ON sh.property_id = p.id "
         "WHERE "
         "city = %(city)s AND "
         "s.name in ('pre_venta', 'en_venta', 'vendido') GROUP BY p.id")
    )
])
def test_get_query_filter_params(subquery_filters, expected):
    query = queries.get_estates_query(subquery_filters)
    formatted_query = ''.join(ch for ch in query if not ch.isspace())
    formatted_expected = ''.join(ch for ch in expected if not ch.isspace())

    assert formatted_query == formatted_expected
