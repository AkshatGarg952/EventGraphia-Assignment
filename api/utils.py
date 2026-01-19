from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns a standardized error response.
    Format:
    {
        "status": "error",
        "message": "Brief description",
        "code": "ERROR_CODE",
        "details": { ... }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:

        custom_response_data = {
            "status": "error",
            "message": "An error occurred.",
            "code": "API_ERROR",
            "details": response.data
        }

        if isinstance(response.data, dict):
            custom_response_data["details"] = response.data.copy()
            
            if "detail" in response.data:
                custom_response_data["message"] = response.data["detail"]
                custom_response_data["details"].pop("detail", None)
            elif "error" in response.data:

                custom_response_data["message"] = response.data["error"]
                custom_response_data["details"].pop("error", None)

            if not custom_response_data["details"]:
                custom_response_data["details"] = None

        elif isinstance(response.data, list):

            if response.data and isinstance(response.data[0], str):
                custom_response_data["message"] = " ".join(response.data)
            else:
                custom_response_data["message"] = "Validation failed."
                custom_response_data["details"] = response.data
        
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data["code"] = "VALIDATION_ERROR"
            if custom_response_data["message"] == "An error occurred.":
                 custom_response_data["message"] = "Invalid data provided."

        response.data = custom_response_data

    return response
