import requests
from django.utils import timezone
from unittest.mock import Mock
from .models import ApiRequest
import uuid


def log_and_make_api_call(message_type, request_type, payload, signature, url):
    """
    Logs the API request to the database, makes the API call, and updates the status.

    Args:
        message_type (str): The message type for the API request.
        request_type (str): The system name or request type.
        payload (str): The payload to send in the API request.
        signature (str): The signature for the API request.
        url (str): The URL of the API endpoint.

    Returns:
        dict: A dictionary containing the response status and content.
    """
    # Log the initial API request
    api_request = ApiRequest.objects.create(
        MessageType=message_type,
        RequestType=request_type,
        TimeStamp=timezone.now(),
        ApiUrl=url,  # Add the new ApiUrl field
        PayLoad=payload,
        Signature=signature,
        Status=0  # Initial status, assuming 0 for "pending"
    )

    # Make the API call
    try:
        # headers = {'Content-Type': 'application/xml', 'Signature': signature}
        # response = requests.post(url, data=payload, headers=headers)
        #
        # # Update the ApiRequest object with the response status
        # api_request.Status = response.status_code
        # api_request.save()

        # return {
        #     'status': response.status_code,
        #     'content': response.content
        # }

        mock_response = Mock()
        mock_response.status_code = 200  # Simulate a 200 OK response
        mock_response.content = "Data sent successfully (simulated)"

        # Update the ApiRequest object with the simulated response status
        api_request.Status = mock_response.status_code
        api_request.save()

        return {
            'status': mock_response.status_code,
            'content': mock_response.content
        }
    except requests.exceptions.RequestException as e:
        # Log the error in the database
        api_request.Status = 500  # Assuming 500 for internal errors
        api_request.save()

        return {
            'status': 500,
            'error': str(e)
        }
