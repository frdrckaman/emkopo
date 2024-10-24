import xmltodict
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import INCOMING
from emkopo_mixins.signature import verify_xml_signature


class GeneralResponseAPIView(APIView):
    """
    API View to receive XML data from a third-party system, validate it, and respond with the status.
    """

    @swagger_auto_schema(
        operation_description="Receive XML response from a third-party system",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="XML payload with response details"
        ),
        responses={
            200: openapi.Response(description="Success"),
            400: openapi.Response(description="Invalid XML or missing fields"),
        }
    )
    def post(self, request):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response({"error": "Content-Type must be application/xml"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the XML data from the request body
        try:
            xml_data = request.body_cache.decode('utf-8').strip()
            if not xml_data:
                raise ValueError("Empty request body")

            # Remove whitespace between XML tags
            xml_data = re.sub(r'>\s+<', '><', xml_data)
        except Exception as e:
            return Response(
                {'error': f'Invalid XML data in request body: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        if not settings.EMKOPO_SIT:
            # Verify the XML signature before proceeding
            if not verify_xml_signature(xml_data):
                return Response({"error": "Signature verification failed"},
                                status=status.HTTP_400_BAD_REQUEST)

        # Convert XML data to a dictionary
        try:
            data_dict = xmltodict.parse(xml_data)
        except Exception as e:
            return Response(
                {'error': f'Failed to parse XML: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        return general_response(data_dict, xml_data)


def general_response(data_dict, xml_data):
    document_data = data_dict.get('Document')
    if not document_data:
        return Response(
            {'error': 'Document node is missing in the XML data.'},
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/xml'
        )

    try:
        response = log_and_make_api_call(
            request_type=INCOMING,
            payload=xml_data,
            signature=settings.ESS_SIGNATURE,
            url=settings.ESS_UTUMISHI_API
        )
        if response.get('status') == 200:
            return Response({"message": "Data sent successfully"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get('error', 'Failed to send data')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response(
            {'error': f'Failed to save API request: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/xml'
        )