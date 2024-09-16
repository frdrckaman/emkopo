import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import xmltodict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import LoanOfferRequest


class LoanOfferCancellationNotificationAPIView(APIView):
    """
    API View to receive loan cancellation notification from the third-party system.
    """

    @swagger_auto_schema(
        operation_description="Receive loan cancellation notification from the third-party system",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="XML payload containing loan cancellation notification",
        ),
        responses={
            200: openapi.Response(
                description="Successful Response",
                examples={
                    'application/json': {
                        'message': 'Loan offer request updated successfully.'
                    }
                }
            ),
            400: openapi.Response(description="Invalid XML data or missing required fields"),
            404: openapi.Response(description="LoanOfferRequest not found"),
            500: openapi.Response(description="Internal Server Error"),
        },
        consumes=['application/xml'],  # Indicate that the API consumes XML
    )
    def post(self, request, *args, **kwargs):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response(
                {'error': 'Content-Type must be application/xml'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Decode the XML data from the request body
            xml_data = request.body.decode('utf-8').strip()
            xml_data = re.sub(r'>\s+<', '><', xml_data)

            # Parse the XML data to a Python dictionary
            data_dict = xmltodict.parse(xml_data)

            # Extract data from the parsed dictionary
            document = data_dict.get('Document', {})
            data = document.get('Data', {})
            message_details = data.get('MessageDetails', {})

            # Extract specific fields from the XML payload
            application_number = message_details.get('ApplicationNumber')
            reason = message_details.get('Reason')
            fsp_reference_number = message_details.get('FSPReferenceNumber')
            loan_number = message_details.get('LoanNumber')

            # Validate required fields
            if not application_number or not fsp_reference_number:
                return Response(
                    {'error': 'ApplicationNumber and FSPReferenceNumber are required fields.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Find and update the LoanOfferRequest
            try:
                log_and_make_api_call(
                    request_type=INCOMING,
                    payload=xml_data,
                    signature="XYZ",  # Replace with actual signature if available
                    url="https://third-party-api.example.com/endpoint"
                    # Replace with actual endpoint URL
                )

                loan_offer_request = LoanOfferRequest.objects.get(
                    ApplicationNumber=application_number,
                    FSPReferenceNumber=fsp_reference_number
                )

                if loan_offer_request.status >= 3:
                    return Response(
                        {'error': 'Operation not allowed. Status must be less than 3.'},
                        status=status.HTTP_409_CONFLICT
                    )
                # Update fields
                loan_offer_request.CancellationReason = reason
                loan_offer_request.status = 9
                loan_offer_request.save()

            except LoanOfferRequest.DoesNotExist:
                return Response(
                    {'error': f'LoanOfferRequest with ApplicationNumber {application_number} and LoanNumber {loan_number} not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({'message': 'Loan offer request updated successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any exceptions that occur during XML parsing
            return Response({'error': f'Invalid XML data: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
