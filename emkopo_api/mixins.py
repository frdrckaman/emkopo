import re

import requests
import xmltodict
from django.conf import settings
from django.utils import timezone
from django.forms.models import model_to_dict
from unittest.mock import Mock
from rest_framework.response import Response
from rest_framework import status
from xml.parsers.expat import ExpatError

from emkopo_constants.constants import OUTGOING
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

    if request_type == OUTGOING:

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
    else:
        mock_response = Mock()
        mock_response.status_code = 200  # Simulate a 200 OK response
        mock_response.content = "Data Saved successfully"

        api_request.Status = mock_response.status_code
        api_request.save()

        return {
            'status': mock_response.status_code,
            'content': mock_response.content
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


def convert_to_xml(request_type, message_type, data, fsp, msg_id):
    if request_type == OUTGOING:
        sender = fsp.name
        receiver = settings.EMKOPO_UTUMISHI_SYSNAME
    else:
        sender = settings.EMKOPO_UTUMISHI_SYSNAME
        receiver = fsp.name
    # Create the root element
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header element
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = sender
    SubElement(header, "Receiver").text = receiver
    SubElement(header, "FSPCode").text = fsp.code
    SubElement(header, "MsgId").text = msg_id
    SubElement(header, "MessageType").text = message_type

    # Add each product as a MessageDetails element
    for product in data:
        message_details = SubElement(data_elem, "MessageDetails")
        for key, value in product.items():
            if key == 'terms_conditions':
                for term in value:
                    term_elem = SubElement(message_details, "TermsCondition")
                    for term_key, term_value in term.items():
                        SubElement(term_elem, term_key).text = str(term_value)
            else:
                SubElement(message_details, key).text = str(value)

    # Add the Signature element
    SubElement(document, "Signature").text = "XYZ"

    # Convert the Element to a string
    xml_string = tostring(document, encoding="utf-8").decode("utf-8").strip()
    xml_data = re.sub(r'>\s+<', '><', xml_string)
    return xml_data


def model_instance_to_dict(instance):
    if not hasattr(instance, 'pk'):
        raise ValueError("Provided instance is not a valid Django model instance.")
    return model_to_dict(instance)
