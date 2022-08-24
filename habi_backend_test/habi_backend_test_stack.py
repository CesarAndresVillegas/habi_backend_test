from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _api_gw
)


class HabiBackendTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        available_estate_for_sale = _lambda.Function(
            self, "AvailableEstateForSale",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("src/estates"),
            handler="available_estates.available_estate_for_sale",
            function_name="AvailableEstateForSale",
        )

        api_habi = _api_gw.RestApi(
            self, "ApiHabi",
            rest_api_name="ApiHabi"
        )

        available_estate_integration = _api_gw.LambdaIntegration(
            available_estate_for_sale
        )

        endpoint_testing = api_habi.root.add_resource("estates")
        endpoint_testing.add_method("GET", available_estate_integration)
