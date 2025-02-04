from typing import List
from math import isclose

from app.models import Loan, LoanScheduleItem, LoanSummary

# Calculating the monthly payment of a loan by using (P*r)/1-(1+r)^-n
def calculate_monthly_payment(principal: float, annual_interest_rate: float, loan_term_months: int) -> float:
    if loan_term_months <= 0:
        return 0
    monthly_interest_rate = annual_interest_rate / 12
    if isclose(monthly_interest_rate, 0):
        return principal / loan_term_months

    numerator = monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months
    denominator = (1 + monthly_interest_rate) ** loan_term_months - 1
    payment = principal * (numerator / denominator)
    return round(payment, 2)

# Calculating amortization schedule over loan term months for principal + interest per month
def generate_amortization_schedule(loan: Loan) -> List[LoanScheduleItem]:
    schedule = []
    monthly_payment = calculate_monthly_payment(loan.amount, loan.annual_interest_rate, loan.loan_term_months)
    remaining = round(loan.amount, 2)
    monthly_interest_rate = loan.annual_interest_rate / 12

    for m in range(1, loan.loan_term_months + 1):
        interest_for_month = round(remaining * monthly_interest_rate, 2)
        
        principal_for_month = round(monthly_payment - interest_for_month, 2)
        if principal_for_month > remaining:
            principal_for_month = remaining
            monthly_payment = principal_for_month + interest_for_month  
        
        remaining = round(remaining - principal_for_month, 2)
        remaining = max(remaining, 0.0)  
        
        schedule.append(LoanScheduleItem(month=m, 
                                         remaining_balance=round(remaining, 2), 
                                         monthly_payment=round(monthly_payment, 2)))
        if isclose(remaining, 0.0, abs_tol=1e-6):
            break  
    return schedule

# Calculating loan summary for month: Interest payment, principal payment, remaining loan balance
def get_loan_summary_for_month(loan: Loan, month: int) -> LoanSummary:
    if month < 0 or month > loan.loan_term_months:
        raise ValueError(f"Month {month} out of valid range [0..{loan.loan_term_months}].")

    monthly_payment = calculate_monthly_payment(loan.amount, loan.annual_interest_rate, loan.loan_term_months)
    monthly_interest_rate = loan.annual_interest_rate / 12
    total_principal_paid = 0.0
    total_interest_paid = 0.0
    remaining = round(loan.amount, 2)

    for _ in range(month):
        if remaining <= 0:
            break
        interest_for_month = round(remaining * monthly_interest_rate, 2)
        principal_for_month = round(monthly_payment - interest_for_month, 2)

        if principal_for_month > remaining:
            principal_for_month = remaining
        total_interest_paid += interest_for_month
        total_principal_paid += principal_for_month

        remaining = round(remaining - principal_for_month, 2)
        remaining = max(remaining, 0.0)

    return LoanSummary(
        month=month,
        current_principal_balance=round(remaining, 2),
        total_principal_paid=round(total_principal_paid, 2),
        total_interest_paid=round(total_interest_paid, 2),
    )