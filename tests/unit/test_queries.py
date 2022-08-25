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


"""

,
    (
        "WHERE city = %(city)s",
        ("SELECT address, city, status, price, description FROM "
         "(SELECT p.id, p.address, p.city, s.name AS status, p.price, "
         "p.description, date_format(max(sh.update_date),'%d-%m-%y') as date "
         "FROM property p JOIN status_history sh ON p.id = sh.property_id "
         "JOIN status s ON s.id = sh.status_id WHERE city = %(city)s "
         "GROUP BY p.id) as aux  WHERE status in ('pre_venta', 'en_venta', "
         "'vendido')")
    ),
    (
        "WHERE city = %(city)s AND year = %(year)s AND s.name = %(status)s",
        ("SELECT address, city, status, price, description FROM "
         "(SELECT p.id, p.address, p.city, s.name AS status, p.price, "
         "p.description, date_format(max(sh.update_date),'%d-%m-%y') as date "
         "FROM property p JOIN status_history sh ON p.id = sh.property_id "
         "JOIN status s ON s.id = sh.status_id WHERE city = %(city)s "
         "AND year = %(year)s AND s.name = %(status)s GROUP BY p.id) as aux "
         "WHERE status in ('pre_venta', 'en_venta', 'vendido')")
    )


"""


"SELECTp.address,p.city,s.nameASstatus,p.price,p.descriptionFROMstatus_historyshINNERJOIN(SELECTid,property_id,status_id,MAX(update_date)asmxdateFROMstatus_historyGROUPBYproperty_id)bONsh.property_id=b.property_idANDsh.update_date=b.mxdateJOINstatussONsh.status_id=s.idJOINpropertypONsh.property_id=p.idWHEREs.namein('pre_venta','en_venta','vendido')GROUPBYp.id"
"SELECTp.address,p.city,s.nameASstatus,p.price,p.descriptionFROMstatus_historyshINNERJOIN(SELECTid,property_id,status_id,MAX(update_date)asmxdateFROMstatus_historyGROUPBYproperty_id)bONsh.property_id=b.property_idANDsh.update_date=b.mxdateJOINstatussONsh.status_id=s.idJOINpropertypONsh.property_id=p.idWHEREcity=%(city)sANDyear=%(year)sANDs.name=%(status)sANDs.namein('pre_venta','en_venta','vendido')GROUPBYp.id"



"""


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


"""