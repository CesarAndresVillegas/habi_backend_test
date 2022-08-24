import sys

sys.path.append('src')
import estates.available_estates as available_estates


def test_available_estate_for_sale():
    response = available_estates.available_estate_for_sale(None, None)
    expected = {
        "statusCode": 200,
        "body": "Hello, CDK! You have hit"
    }

    assert response["statusCode"] == expected["statusCode"]
    assert response["body"] == expected["body"]
