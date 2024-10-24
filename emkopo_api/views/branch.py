import base64
import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import OUTGOING
from emkopo_mixins.signature import load_private_key, sign_data
from emkopo_product.models import District, Fsp


class BranchDetailsAPIView(APIView):
    """
    API View to fetch Branch details and send XML data to third-party system.
    """

    @swagger_auto_schema(
        operation_description="Send XML for branch details fetched from the Branch model.",
        responses={
            200: openapi.Response(description="Data successfully sent."),
            500: openapi.Response(description="Failed to send data to third-party system."),
        }
    )
    def get(self, request):
        return branch()

def branch():
    districts = District.objects.prefetch_related('branch_set').all()

    if not districts:
        return Response({"error": "No districts found."}, status=status.HTTP_404_NOT_FOUND)

    fsp = Fsp.objects.first()

    if not fsp:
        return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

    response = generate_xml_for_branch_details(districts, fsp)

    if response.get('status') == 200:
        return Response({"message": "Data successfully sent and inserted."},
                        status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send data to the third-party system."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_xml_for_branch_details(districts, fsp):
    """
    Generate XML data for branch details.
    """
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = fsp.name
    SubElement(header, "Receiver").text = settings.EMKOPO_UTUMISHI_SYSNAME
    SubElement(header, "FSPCode").text = fsp.code
    SubElement(header, "MsgId").text = str(uuid.uuid4())
    SubElement(header, "MessageType").text = "FSP_BRANCHES"

        # Create the MessageDetails element
    message_details = SubElement(data_elem, "MessageDetails")

    # Iterate over Districts and their related Branches to create XML
    for district in districts:
        branch_detail = SubElement(message_details, "BranchDetail")
        SubElement(branch_detail, "DistrictCode").text = district.DistrictCode  # Assuming the District model has a 'code' field

        # Iterate over branches within the district
        branches = district.branch_set.filter(active=True)  # Only active branches
        for branch in branches:
            branch_elem = SubElement(branch_detail, "Branch")
            SubElement(branch_elem, "BranchCode").text = branch.BranchCode
            SubElement(branch_elem, "BranchName").text = branch.BranchName

    # Convert the XML Element to string (we'll sign this string)
    xml_string = tostring(document, encoding="utf-8").decode("utf-8")

    # Load the private key to sign the data
    private_key = load_private_key(settings.EMKOPO_PRIVATE_KEY)

    # Convert the XML string to bytes
    xml_bytes = xml_string.encode('utf-8')

    # Sign the XML data (xml_bytes) using the private key
    signature = sign_data(private_key, xml_bytes)

    # Encode the signature in base64
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    # Add the Signature element to the document
    SubElement(document, "Signature").text = signature_b64

    # Convert the final XML (with the signature) to string
    final_xml_string = tostring(document, encoding="utf-8").decode("utf-8")

    # Send the API response with the final XML payload
    response = log_and_make_api_call(
        request_type=OUTGOING,
        payload=final_xml_string,
        signature=signature_b64,
        url=settings.ESS_UTUMISHI_API
    )
    return response
