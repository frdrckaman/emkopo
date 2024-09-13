from decimal import Decimal, InvalidOperation
from django.db import IntegrityError
import logging

from emkopo_loan.models import LoanChargeResponse

# Set up logging
logger = logging.getLogger(__name__)


class LoanCalculator:
    def __init__(self, loan_request):
        self.loan_request = loan_request

    def safe_decimal(self, value):
        """
        Convert a value to Decimal safely, handling strings and None values.
        """
        try:
            return Decimal(value)
        except (TypeError, InvalidOperation):
            return Decimal('0.00')

    def calculate_max_loan_amount(self):
        net_salary = self.safe_decimal(self.loan_request.NetSalary)
        one_third_amount = net_salary / Decimal(3)
        requested_amount = self.safe_decimal(self.loan_request.RequestedAmount)
        return min(one_third_amount, requested_amount or one_third_amount)

    def calculate_deductible_amount(self):
        """
        Calculate the deductible amount safely after converting all fields to Decimal.
        """
        desired_deductible_amount = self.safe_decimal(
            self.loan_request.DesiredDeductibleAmount)
        max_loan_amount = self.calculate_max_loan_amount()

        if desired_deductible_amount > Decimal('0'):
            return min(desired_deductible_amount, max_loan_amount)
        return self.safe_decimal(self.loan_request.DeductibleAmount)

    def calculate_loan_duration(self):
        """
        Calculate the loan duration in months.
        """
        if not self.loan_request.Tenure:
            # Calculate tenure in months up to the retirement date
            return max(0, (
                        self.loan_request.RetirementDate - 2024) * 12)  # Assuming retirement year format
        return self.loan_request.Tenure

    def calculate_total_deduction(self):
        """
        Calculate the total deduction for the loan.
        """
        tenure_months = Decimal(
            self.calculate_loan_duration())  # Convert to Decimal for safe multiplication
        deductible_amount = self.calculate_deductible_amount()  # Ensure it's a Decimal
        return deductible_amount * tenure_months

    def calculate_loan_details(self):
        """
        Calculate and return loan details.
        """
        max_loan_amount = self.calculate_max_loan_amount()
        total_deduction = self.calculate_total_deduction()

        return {
            'MaxLoanAmount': max_loan_amount,
            'DeductibleAmount': self.calculate_deductible_amount(),
            'LoanDurationMonths': Decimal(self.calculate_loan_duration()),
            # Ensure Decimal for consistency
            'TotalDeduction': total_deduction,
            'NetLoanAmount': max_loan_amount - (Decimal('0.02') * max_loan_amount),
            # Example calculation
            'TotalInterestRateAmount': Decimal('0.1') * max_loan_amount,  # Example calculation
            'TotalAmountToPay': total_deduction + Decimal('0.02') * total_deduction,
            # Example calculation
        }

    def create_loan_response(self):
        """
        Creates a LoanChargeResponse record after calculating the loan details.
        """
        loan_details = self.calculate_loan_details()

        try:
            # Attempt to create a LoanChargeResponse object
            loan_response = LoanChargeResponse.objects.create(
                LoanChargeRequest=self.loan_request,
                DesiredDeductibleAmount=self.calculate_deductible_amount(),
                TotalInsurance=Decimal('0.02') * loan_details['MaxLoanAmount'],
                # Example calculation
                TotalProcessingFees=Decimal('100.00'),  # Example fixed processing fees
                TotalInterestRateAmount=loan_details['TotalInterestRateAmount'],
                OtherCharges=Decimal('50.00'),  # Example fixed other charges
                NetLoanAmount=loan_details['NetLoanAmount'],
                TotalAmountToPay=loan_details['TotalAmountToPay'],
                Tenure=int(self.calculate_loan_duration()),
                # Convert duration to integer for model field
                EligibleAmount=loan_details['MaxLoanAmount'],
                MonthlyReturnAmount=loan_details['TotalAmountToPay'] / loan_details[
                    'LoanDurationMonths'],  # Use Decimal duration
                MessageType=self.loan_request.MessageType,
                RequestType=self.loan_request.RequestType,
                status=1
            )
            return loan_response

        except IntegrityError as e:
            logger.error(f"IntegrityError while creating LoanChargeResponse: {e}")
            return None

        except Exception as e:
            logger.error(f"An error occurred while creating LoanChargeResponse: {e}")
            return None
