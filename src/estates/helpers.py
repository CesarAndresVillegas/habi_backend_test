from array import array
import json
import boto3

VALID_FILTERS = ("city", "year", "status")


def format_filter_estate_status(filters: dict) -> str:
    """_summary_

    Args:
        filters (dict): filters received from api queryStringParameters

    Returns:
        str: WHERE condition to mysql query based on received filters
    """
    conditions = []

    if filters:
        for filter_key, filter_value in filters.items():
            if filter_value and filter_key in VALID_FILTERS:
                if filter_key == "status":
                    conditions.append(
                        f"s.name = %({filter_key})s"
                    )
                else:
                    conditions.append(
                        f"{filter_key} = %({filter_key})s"
                    )

    where = ''
    if conditions:
        where = "WHERE "
        where += " AND ".join(conditions)

    return where


def get_query_filter_params(filters: dict) -> dict:
    """_summary_

    Args:
        filters (dict): filters received from api queryStringParameters

    Returns:
        dict: params attribute required to mysql query,
              dictionary based on valid filters
    """
    params = {}

    if filters:
        for filter_key, filter_value in filters.items():
            if filter_value and filter_key in VALID_FILTERS:
                params[filter_key] = filter_value

    return params


def format_estated_information(information: list) -> list:
    """_summary_

    Args:
        information (array): unformatted properties information,
                             result from mysql query

    Returns:
        array: formatted properties information to return to the user
    """
    formatted_info = []
    if information:
        for item in information:
            formatted_register = {}
            formatted_register["address"] = item[0]
            formatted_register["city"] = item[1]
            formatted_register["status"] = item[2]
            formatted_register["price"] = item[3]
            formatted_register["description"] = item[4]

            formatted_info.append(formatted_register)

        return formatted_info
    else:
        return [
            {"message":
                "No hay propiedades disponibles con estas características"}]


def sql_service_invoker(lambda_payload: dict) -> list:
    """_summary_

    Args:
        lambda_payload (dict): query and params required to use
                               sql_service -> get_states function

    Returns:
        list: sql_service -> get_states function result
    """
    lambda_client = boto3.client('lambda')
    lambda_response = lambda_client.invoke(
        FunctionName='GetEstates',
        InvocationType='RequestResponse',
        Payload=json.dumps(lambda_payload))

    return json.loads(lambda_response['Payload'].read().decode())
