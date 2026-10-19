
from decimal import Decimal


def convert_chf_to_gbp(amount_chf, chf_per_gbp):
    """Convert an amount in CHF into GBP using CHF per GBP."""
    if chf_per_gbp <= 0:
        raise ValueError("The exchange rate must be greater than zero.")

    return amount_chf / chf_per_gbp


def calculate_annual_pay(salary_chf, bonus_chf):
    """Calculate annual salary plus bonus in CHF."""
    if salary_chf < 0 or bonus_chf < 0:
        raise ValueError("Salary and bonus cannot be negative.")

    return salary_chf + bonus_chf


def calculate_uk_income_tax(gross_income):
    """Estimate UK income tax using 2026/27 England rates.

    Assumptions: employment income only, standard Personal Allowance,
    no pension deductions or other reliefs.
    """
    if not gross_income.is_finite() or gross_income < 0:
        raise ValueError("Income must be a valid, non-negative amount.")

    personal_allowance = Decimal("12570")

    # Reduce the Personal Allowance by £1 for every £2 above £100,000.
    if gross_income > Decimal("100000"):
        reduction = (gross_income - Decimal("100000")) / Decimal("2")
        personal_allowance = max(
            Decimal("0"),
            personal_allowance - reduction,
        )

    taxable_income = max(
        Decimal("0"),
        gross_income - personal_allowance,
    )

    basic_band = min(taxable_income, Decimal("37700"))
    higher_band = min(
        max(taxable_income - Decimal("37700"), Decimal("0")),
        Decimal("87440"),
    )
    additional_band = max(
        taxable_income - Decimal("125140"),
        Decimal("0"),
    )

    tax = (
        basic_band * Decimal("0.20")
        + higher_band * Decimal("0.40")
        + additional_band * Decimal("0.45")
    )

    return tax.quantize(Decimal("0.01"))


def calculate_grossed_up_uk_tax(income_before_tax):
    """Calculate employer-paid UK income tax, including tax-on-tax."""
    if not income_before_tax.is_finite() or income_before_tax < 0:
        raise ValueError("Income must be a valid, non-negative amount.")

    # Start with the tax on income before the employer-paid tax.
    tax = calculate_uk_income_tax(income_before_tax)

    # Recalculate tax after adding the employer-paid tax.
    for _ in range(100):
        updated_tax = calculate_uk_income_tax(
            income_before_tax + tax
        )

        if updated_tax == tax:
            return tax

        tax = updated_tax

    raise RuntimeError("The tax gross-up calculation did not converge.")

def calculate_annual_housing_cost(monthly_housing_gbp):
    """Calculate the annual cost of monthly housing in GBP."""
    if not monthly_housing_gbp.is_finite() or monthly_housing_gbp < 0:
        raise ValueError("Monthly housing cost must be non-negative.")

    return monthly_housing_gbp * Decimal("12")