import json
from utils import logger


def openai_api_error(exception):
    """Handle and format errors."""

    if hasattr(exception, 'response') and exception.response and exception.response.text:
        try:
            error_info = json.loads(exception.response.text)
            error_code = error_info.get(
                "error", {}).get("code", "unknown_code")
            error_message = error_info.get("error", {}).get(
                "message", "An unknown error occurred.")
            http_status_code = exception.response.status_code if hasattr(
                exception.response, 'status_code') else 'unknown_status_code'
            formatted_error_message = (
                f"Error Code {http_status_code}: {error_code}\n\n"
                f"Error Message: {error_message}"
            )
        except json.JSONDecodeError:
            formatted_error_message = f"Error: {str(exception)}"
    else:
        formatted_error_message = f"Error: {str(exception)}"

    logger.error(f"{formatted_error_message}", True)
    raise exception
