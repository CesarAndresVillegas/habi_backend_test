import boto3
import json
import mysql.connector

from helpers import (
    format_filter_estate_status,
    get_query_filter_params,
    format_estated_information,
    sql_service_invoker
)


def available_estate_for_sale(event: dict, context: dict) -> dict:
    """_summary_

    Args:
        event (Dict): Basic lambda event dictionary from api gw endpoint
        context (Dict): Basic lambda context dictionary from api gw endpoint

    Returns:
        Dict: http response with properties information
    """
    try:
        parameters = event.get("queryStringParameters", {})

        query_filters = format_filter_estate_status(parameters)
        query_params = get_query_filter_params(parameters)

        lambda_payload = {
            "query_filters": query_filters,
            "query_params": query_params
        }

        estate_info = sql_service_invoker(lambda_payload)

        formatted_estate_info = format_estated_information(estate_info)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(formatted_estate_info)
        }

    except Exception as e:
        response = {
            "message": str(e)
        }

        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(response)
        }
