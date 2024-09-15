from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid

from emkopo_api.mixins import log_and_make_api_call, convert_to_xml
from emkopo_api.serializers import UserResponseSerializer
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import UserResponse
from emkopo_product.models import Fsp


class LoanOfferResponseAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Generate XML for product decommissioning",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='ID of the product to decommission')
            },
            required=['id']
        ),
        responses={
            200: openapi.Response(description="Data sent successfully (simulated)"),
            404: openapi.Response(description="Product not found"),
            500: openapi.Response(description="Failed to send data to third-party system")
        }
    )
    def post(self, request, *args, **kwargs):
        # Retrieve 'id' from the request data
        user_response_id = request.data.get('id')

        if not user_response_id:
            return Response(
                {'error': 'id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the UserResponse instance
        try:
            user_response = UserResponse.objects.get(id=user_response_id)
        except UserResponse.DoesNotExist:
            return Response({'error': 'UserResponse not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        response = self.offer_request_response(user_response)

        if response.get('status') == 200:
            return Response({"message": "Data sent successfully"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get('error', 'Failed to send data')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def offer_request_response(user_response):
        user_response_data = [user_response]
        fsp = Fsp.objects.first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserResponseSerializer(user_response_data, many=True)

        msg_id = str(uuid.uuid4())
        message_type = 'LOAN_INITIAL_APPROVAL_NOTIFICATION'

        # Convert the data dictionary to an XML string
        xml_data = convert_to_xml(OUTGOING, message_type, serializer.data, fsp, msg_id)

        # Send the POST request with the XML data
        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=xml_data,
            signature="XYZ",  # Replace with actual signature if available
            url="https://third-party-api.example.com/endpoint"
            # Replace with actual endpoint URL
        )
        if response.get('status') == 200:
            loan_offer_request = user_response.LoanOfferRequest
            loan_offer_request.status = 2
            loan_offer_request.save()

        return response
