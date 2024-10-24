from .branch import BranchDetailsAPIView
from .product_catalog import ProductCatalogXMLView
from .product_decommission import GenerateXMLForDecommissionView
from .loan_charge_request import LoanChargesRequestAPIView
from .loan_offer_request import LoanOfferRequestAPIView
from .loan_offer_response import LoanOfferResponseAPIView
from .loan_final_approval import LoanFinalApprovalNotificationAPIView
from .disbursement_notification import LoanDisbursementNotificationAPIView
from .fail_disbursement import LoanDisbursementFailureNotificationAPIView
from .loan_offer_cancellation import LoanOfferCancellationNotificationAPIView
from .payoff_balance_request import LoanPayOffBalanceRequestAPIView
from .settlement_balance_response import LoanSettlementBalanceResponseAPIView
from .loan_restructuring import LoanRestructuringRequestAPIView
from .loan_takeover_details import LoanTakeOverDetailsAPIView
from .loan_liquidation_request import LoanLiquidationRequestAPIView
from .loan_notification_employer import LoanNotificationToEmployerAPIView
from .loan_liquidation_notification import LoanLiquidationNotificationAPIView
from .loan_takeover_disb_notification import LoanTakeoverDisbursementNotificationAPIView
from .loan_repayment_request import LoanRepaymentRequestAPIView
from .repayment_offbalance_request import LoanRepaymentOffBalanceRequestAPIView
from .payoff_payment_response import LoanPayoffPaymentResponseAPIView
from .full_loan_repayment_notification import FullLoanRepaymentNotificationAPIView
from .full_loan_repayment_request import FullLoanRepaymentRequestAPIView
from .loan_repayment_notification import LoanRepaymentNotificationAPIView
from .defaulter_detail_employer import LoanDefaulterDetailEmployerAPIView
from .defaulter_detail import LoanDefaulterDetailAPIView
from .account_validation_request import AccountValidationRequestAPIView
from .account_validation_response import AccountValidationResponseAPIView
from .loan_monthly_deduction import LoanMonthlyDeductionRecordAPIView
from .partial_loan_repayment_response import PartialLoanRepaymentResponseAPIView
from .partial_loan_repayment_request import PartialLoanRepaymentRequestAPIView
from .partial_loan_repayment_response import PartialLoanRepaymentResponseAPIView
from .deduction_stop_notification import LoanDeductionStopNotificationAPIView
from .general_response import GeneralResponseAPIView
from .sbt_emkopo_api import SbtEmkopoAPIEndpoint






