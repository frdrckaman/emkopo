import random
import string
from datetime import datetime

from django.conf import settings

from emkopo_loan.models import UserResponse


def generate_unique_loan_id():
    # Fixed prefix
    prefix = settings.LOAN_ID_PREFIX

    # Current date in YYYYMMDD format
    current_date = datetime.now().strftime('%Y%m%d')

    # Loop until a unique loan ID is found
    while True:
        # Generate a random 4-digit number
        random_number = ''.join(random.choices(string.digits, k=4))

        # Combine all parts to create the loan ID
        loan_id = f"{prefix}{current_date}{random_number}"

        # Check if this ID already exists in the database
        if not UserResponse.objects.filter(LoanNumber=loan_id).exists():
            return loan_id
