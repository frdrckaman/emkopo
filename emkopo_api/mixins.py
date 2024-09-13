import requests
import xmltodict
from django.conf import settings
from django.utils import timezone
from unittest.mock import Mock
from rest_framework.response import Response
from rest_framework import status
from xml.parsers.expat import ExpatError

from emkopo_product.models import Fsp
from .models import ApiRequest
import uuid
from xml.etree.ElementTree import Element, SubElement, tostring


def log_and_make_api_call(request_type, payload, signature, url):
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

    try:
        # Parse the XML payload to a dictionary
        xml_dict = xmltodict.parse(payload)
        # Extract the MessageType from the XML
        message_type = xml_dict['Document']['Data']['Header']['MessageType']
    except (KeyError, ExpatError) as e:
        return {
            'status': 400,
            'error': f"Failed to parse XML or extract MessageType: {str(e)}"
        }


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


def call_decommission_api(product_id):
    """
    Function to call the GenerateXMLForDecommissionView API with an XML payload.

    Args:
        product_id (str): The ID of the product to decommission.

    Returns:
        dict: A dictionary containing the API response status and content.
    """
    fsp = Fsp.objects.all().first()

    if not fsp:
        return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

    # Define the URL of the API endpoint
    api_url = settings.EMKOPO_PRODUCT_DECOMMISSION_API  # Replace with your actual endpoint URL

    # Create the XML payload
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header element
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = fsp.name  # Get Sender from Fsp model
    SubElement(header, "Receiver").text = settings.EMKOPO_UTUMISHI_SYSNAME
    SubElement(header, "FSPCode").text = fsp.code  # Get FSPCode from Fsp model
    SubElement(header, "MsgId").text = str(uuid.uuid4())  # Generate unique MsgId
    SubElement(header, "MessageType").text = "PRODUCT_DECOMMISSION"

    # Add the product code to the MessageDetails element
    message_details = SubElement(data_elem, "MessageDetails")
    SubElement(message_details, "id").text = product_id

    # Convert the ElementTree to a string
    xml_payload = tostring(document, encoding="utf-8").decode("utf-8")
    # print(xml_payload)

    # Prepare headers for the XML request
    headers = {
        'Content-Type': 'application/xml',  # Set content type to XML
    }

    try:
        # Make the POST request to the API
        response = requests.post(api_url, data=xml_payload, headers=headers)

        # Check the response status
        if response.status_code == 200:
            print("API call successful:", response.content)
        else:
            print("API call failed with status:", response.status_code)
            print("Error message:", response.text)

        # Return the response data
        return {
            'status': response.status_code,
            'content': response.content if response.status_code == 200 else response.text
        }
    except requests.exceptions.RequestException as e:
        print("Error making the API call:", str(e))
        return {
            'status': 500,
            'error': str(e)
        }
