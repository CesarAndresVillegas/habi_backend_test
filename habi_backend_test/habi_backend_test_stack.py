from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _api_gw,
    aws_ssm as _ssm,
    aws_iam as _iam
)


class HabiBackendTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ######################################
        # SSM PARAMS WITH DATABASE INFORMATION
        ######################################

        habi_db_host = _ssm.StringParameter.from_string_parameter_attributes(
            self, "HabiDbHost",
            parameter_name="/habi/test/host"
        ).string_value

        habi_db_port = _ssm.StringParameter.from_string_parameter_attributes(
            self, "HabiDbPort",
            parameter_name="/habi/test/port"
        ).string_value

        habi_db_user = _ssm.StringParameter.from_string_parameter_attributes(
            self, "HabiDbUser",
            parameter_name="/habi/test/dbuser"
        ).string_value

        habi_db_pass = _ssm.StringParameter.from_string_parameter_attributes(
            self, "HabiDbPass",
            parameter_name="/habi/test/dbpass"
        ).string_value

        habi_database = _ssm.StringParameter.from_string_parameter_attributes(
            self, "HabiDataBase",
            parameter_name="/habi/test/database"
        ).string_value

        mysql_ly_arn = _ssm.StringParameter.from_string_parameter_attributes(
            self, "MysqlLayerArn",
            parameter_name="/account/helper/layers/mysql"
        ).string_value

        #################################################
        # IAM ROLE BASIC DEFINITION (TO LAMBDA FUNCTIONS)
        #################################################

        role_basic_lambda = _iam.Role(
            self, "LambdaBasicRole",
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        ################################################
        # ROLE POLICIES DEFINITION (TO LAMBDA FUNCTIONS)
        ################################################
        role_basic_lambda.add_to_policy(_iam.PolicyStatement(
            resources=["*"],
            actions=[
                    "lambda:InvokeFunction",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
        ))

        ############################
        # REQUIRED LAYERS DEFINITION
        ############################

        mysql_layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "mysql",
            mysql_ly_arn
        )

        ############################
        # LAMBDA FUNCTION DEFINITION
        ############################

        # Function to get info from database

        _lambda.Function(
            self, "GetEstates",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("src/sql_service"),
            handler="get_estates.get_estates",
            function_name="GetEstates",
            role=role_basic_lambda,
            layers=[mysql_layer],
            timeout=Duration.seconds(30),
            environment={
                "HOST": habi_db_host,
                "PORT": habi_db_port,
                "DB_USER": habi_db_user,
                "DB_PASS": habi_db_pass,
                "DATABASE": habi_database
            }
        )

        # Function to resolve api request

        available_estate_for_sale = _lambda.Function(
            self, "AvailableEstateForSale",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("src/estates"),
            handler="available_estates.available_estate_for_sale",
            function_name="AvailableEstateForSale",
            role=role_basic_lambda,
            layers=[mysql_layer],
            timeout=Duration.seconds(30)
        )

        ############################
        # API REST CONFIGURATION
        ############################

        # Basic api definition

        api_habi = _api_gw.RestApi(
            self, "ApiHabi",
            rest_api_name="ApiHabi"
        )

        # Basic api - lambda integration definition

        available_estate_integration = _api_gw.LambdaIntegration(
            available_estate_for_sale
        )

        # endpoint definition

        endpoint_testing = api_habi.root.add_resource("estates")
        endpoint_testing.add_method("GET", available_estate_integration)
