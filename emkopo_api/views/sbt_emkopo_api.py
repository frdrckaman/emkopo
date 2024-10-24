import re

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import xmltodict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.views import LoanMonthlyDeductionRecordAPIView
from emkopo_api.views.account_validation_request import account_validation_request
from emkopo_api.views.deduction_stop_notification import deduction_stop_notification
from emkopo_api.views.defaulter_detail import defaulter_detail
from emkopo_api.views.full_loan_repayment_request import full_loan_repayment
from emkopo_api.views.general_response import general_response
from emkopo_api.views.loan_charge_request import loan_charge
from emkopo_api.views.loan_final_approval import loan_final_approval
from emkopo_api.views.loan_liquidation_notification import loan_liquidation_notification
from emkopo_api.views.loan_liquidation_request import loan_liquidation_request
from emkopo_api.views.loan_offer_cancellation import offer_cancellation
from emkopo_api.views.loan_offer_request import loan_offer_request
from emkopo_api.views.loan_repayment_request import loan_repayment_request
from emkopo_api.views.loan_takeover_disb_notification import loan_takeover_disb_notification
from emkopo_api.views.partial_loan_repayment_request import partial_loan_repayment_request
from emkopo_api.views.payoff_balance_request import payoff_balance_request
from emkopo_mixins.signature import verify_xml_signature


class SbtEmkopoAPIEndpoint(APIView):
    """
    Unified API Endpoint to handle multiple actions based on the MessageType tag in the XML payload.
    """

    @swagger_auto_schema(
        operation_description="Unified API to handle different actions based on MessageType in XML.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description='XML payload with MessageType for different actions',
        ),
        responses={
            200: openapi.Response(description="Action performed successfully"),
            400: openapi.Response(description="Invalid XML or unknown MessageType"),
            500: openapi.Response(description="Server error"),
        }
    )
    def post(self, request):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response({"error": "Content-Type must be application/xml"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the XML data
        try:
            xml_data = request.body.decode('utf-8').strip()
            xml_data = re.sub(r'>\s+<', '><', xml_data)

            if not settings.EMKOPO_SIT:
                # Verify the XML signature before proceeding
                if not verify_xml_signature(xml_data):
                    return Response({"error": "Signature verification failed"},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Convert XML to Python dictionary using xmltodict
            data_dict = xmltodict.parse(xml_data)

            # Extract 'MessageType' from the XML payload
            message_type = data_dict.get('Document', {}).get('Data', {}).get('Header', {}).get('MessageType', '')

            # Route the request based on the MessageType
            if message_type == "LOAN_CHARGES_REQUEST":
                return loan_charge(data_dict, xml_data)
            elif (message_type == "LOAN_OFFER_REQUEST" or message_type ==
                  "TOP_UP_OFFER_REQUEST") or message_type == "TAKEOVER_EMPLOYEE_DETAILS_TO_FSP2":
                return loan_offer_request(data_dict, xml_data)
            elif message_type == "LOAN_FINAL_APPROVAL_NOTIFICATION":
                return loan_final_approval(data_dict, xml_data)
            elif message_type == "LOAN_CANCELLATION_NOTIFICATION" or message_type == "TAKEOVER_REJECTION_NOTIFICATION":
                return offer_cancellation(data_dict, xml_data)
            elif message_type == "TOP_UP_PAY_0FF_BALANCE_REQUEST" or message_type == "PAY_0FF_BALANCE_REQUEST":
                return payoff_balance_request(data_dict, xml_data)
            elif message_type == "STATUS_NOTIFICATION_AND_LIQUIDATION_REQUEST":
                return loan_liquidation_request(data_dict, xml_data)
            elif message_type == "LIQUIDATION_NOTIFICATION_EMPLOYER_TO_FSP2":
                return loan_liquidation_notification(data_dict, xml_data)
            elif message_type == "TAKEOVER_DISBURSEMENT_NOTIFICATION":
                return loan_takeover_disb_notification(data_dict, xml_data)
            elif message_type == "FSP_REPAYMENT_REQUEST":
                return loan_repayment_request(data_dict, xml_data)
            elif message_type == "FULL_LOAN_REPAYMENT_REQUEST":
                return full_loan_repayment(data_dict, xml_data)
            elif message_type == "PARTIAL_LOAN_REPAYMENT_REQUEST":
                return partial_loan_repayment_request(data_dict, xml_data)
            elif message_type == "DEFAULTER_DETAILS_TO_FSP":
                return defaulter_detail(data_dict, xml_data)
            elif message_type == "ACCOUNT_VALIDATION":
                return account_validation_request(data_dict, xml_data)
            elif message_type == "FSP_MONTHLY_DEDUCTIONS":
                return LoanMonthlyDeductionRecordAPIView().loan_monthly_deduction(data_dict,
                                                                                xml_data)
            elif message_type == "DEDUCTION_STOP_NOTIFICATION":
                return deduction_stop_notification(data_dict, xml_data)

            elif message_type == "RESPONSE":
                return general_response(data_dict, xml_data)

            # Add more MessageType handlers as needed
            else:
                return Response({"error": f"Unknown MessageType: {message_type}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"Failed to process XML: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

