import pytest
import sys

sys.path.append('src')
import estates.helpers as helpers


@pytest.mark.parametrize("filters, expected", [
    ({}, ""),
    ({"city": "bogota"}, "WHERE city = %(city)s"),
    (
        {"city": "bogota", "year": "2011"},
        "WHERE city = %(city)s AND year = %(year)s"
    ),
    (
        {"city": "bogota", "year": "2011", "status": "pre_venta"},
        "WHERE city = %(city)s AND year = %(year)s AND s.name = %(status)s"
    ),
    (
        {"city": "bogota", "filtro_random": "2011"},
        "WHERE city = %(city)s"
    ),
    (
        {"filtro_random": "2011"}, ""
    )
])
def test_format_filter_estate_status(filters, expected):
    assert helpers.format_filter_estate_status(filters) == expected


@pytest.mark.parametrize("filters, expected", [
    ({}, {}),
    ({"city": "bogota"}, {"city": "bogota"}),
    (
        {"city": "bogota", "year": "2011", "status": "pre_venta"},
        {"city": "bogota", "year": "2011", "status": "pre_venta"},
    ),
    (
        {"city": "bogota", "filtro_random": "2011"},
        {"city": "bogota"}
    ),
    (
        {"filtro_random": "2011"}, {}
    )
])
def test_get_query_filter_params(filters, expected):
    assert helpers.get_query_filter_params(filters) == expected


@pytest.mark.parametrize("information, expected", [
    (
        [],
        [{
            "message":
                "No hay propiedades disponibles con estas características"}]),
    (
        [
            [
                "carrera 100 #15-90w",
                "bogota",
                "pre_venta",
                "350000000",
                "Amplio apartamento en conjunto cerrado"
            ]
        ],
        [
            {
                "address": "carrera 100 #15-90w",
                "city": "bogota",
                "status": "pre_venta",
                "price": "350000000",
                "description": "Amplio apartamento en conjunto cerrado"
            }
        ])
])
def test_format_estated_information(information, expected):
    assert helpers.format_estated_information(information) == expected
