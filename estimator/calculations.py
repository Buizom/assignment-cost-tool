
from decimal import Decimal, ROUND_HALF_UP


PENNY = Decimal("0.01")
UK_PERSONAL_ALLOWANCE = Decimal("12570")
UK_BASIC_RATE_LIMIT = Decimal("37700")
UK_HIGHER_RATE_LIMIT = Decimal("125140")
UK_RELOCATION_EXEMPTION = Decimal("8000")
UK_EMPLOYER_NI_RATE = Decimal("0.15")
UK_EMPLOYER_NI_THRESHOLD = Decimal("5000")
UK_CLASS_1A_RATE = Decimal("0.15")


def money(value):
    """Round a monetary amount to two decimal places."""
    return value.quantize(PENNY, rounding=ROUND_HALF_UP)


def convert_chf_to_gbp(amount_chf, chf_per_gbp):
    """Convert CHF to GBP using the number of CHF per £1."""
    if not amount_chf.is_finite() or amount_chf < 0:
        raise ValueError("The CHF amount must be non-negative.")
    if not chf_per_gbp.is_finite() or chf_per_gbp <= 0:
        raise ValueError("The exchange rate must be greater than zero.")
    return money(amount_chf / chf_per_gbp)


def calculate_annual_pay(salary_chf, bonus_chf):
    """Add annual salary and bonus, both expressed in CHF."""
    if (
        not salary_chf.is_finite()
        or not bonus_chf.is_finite()
        or salary_chf < 0
        or bonus_chf < 0
    ):
        raise ValueError("Salary and bonus must be non-negative.")
    return salary_chf + bonus_chf


def calculate_uk_income_tax(gross_income):
    """Estimate 2026/27 England employment income tax.

    Assumes standard Personal Allowance and no other income,
    pension deductions, or tax reliefs.
    """
    if not gross_income.is_finite() or gross_income < 0:
        raise ValueError("Income must be non-negative.")

    allowance = UK_PERSONAL_ALLOWANCE

    if gross_income > Decimal("100000"):
        reduction = (gross_income - Decimal("100000")) / Decimal("2")
        allowance = max(Decimal("0"), allowance - reduction)

    taxable = max(Decimal("0"), gross_income - allowance)
    basic = min(taxable, UK_BASIC_RATE_LIMIT)
    higher = min(
        max(taxable - UK_BASIC_RATE_LIMIT, Decimal("0")),
        UK_HIGHER_RATE_LIMIT - UK_BASIC_RATE_LIMIT,
    )
    additional = max(taxable - UK_HIGHER_RATE_LIMIT, Decimal("0"))

    tax = (
        basic * Decimal("0.20")
        + higher * Decimal("0.40")
        + additional * Decimal("0.45")
    )
    return money(tax)


def calculate_grossed_up_uk_tax(income_before_tax):
    """Iterate until employer-paid tax also has tax applied to it."""
    if not income_before_tax.is_finite() or income_before_tax < 0:
        raise ValueError("Income must be non-negative.")

    tax = calculate_uk_income_tax(income_before_tax)

    for _ in range(100):
        updated_tax = calculate_uk_income_tax(income_before_tax + tax)
        if updated_tax == tax:
            return tax
        tax = updated_tax

    raise RuntimeError("The tax gross-up calculation did not converge.")


def calculate_annual_housing_cost(monthly_housing_gbp):
    """Calculate twelve months of employer-paid housing."""
    if not monthly_housing_gbp.is_finite() or monthly_housing_gbp < 0:
        raise ValueError("Housing cost must be non-negative.")
    return money(monthly_housing_gbp * Decimal("12"))


def calculate_taxable_relocation_cost(
    moving_cost_gbp,
    temporary_housing_gbp,
):
    """Estimate costs above the £8,000 qualifying-cost exemption.

    This simplified function assumes all costs entered qualify for
    consideration under the relocation rules. Actual eligibility
    depends on HMRC conditions and time limits.
    """
    if (
        not moving_cost_gbp.is_finite()
        or not temporary_housing_gbp.is_finite()
        or moving_cost_gbp < 0
        or temporary_housing_gbp < 0
    ):
        raise ValueError("Relocation costs must be non-negative.")

    total = moving_cost_gbp + temporary_housing_gbp
    return money(max(Decimal("0"), total - UK_RELOCATION_EXEMPTION))


def calculate_employer_class_1_ni(earnings):
    """Simplified annual employer Class 1 NI estimate for 2026/27."""
    if not earnings.is_finite() or earnings < 0:
        raise ValueError("Earnings must be non-negative.")
    return money(
        max(Decimal("0"), earnings - UK_EMPLOYER_NI_THRESHOLD)
        * UK_EMPLOYER_NI_RATE
    )


def calculate_class_1a_ni(taxable_benefits):
    """Estimate employer Class 1A NI on taxable benefits."""
    if not taxable_benefits.is_finite() or taxable_benefits < 0:
        raise ValueError("Taxable benefits must be non-negative.")
    return money(taxable_benefits * UK_CLASS_1A_RATE)


def calculate_assignment_costs(values):
    """Calculate a two-year illustrative assignment cost estimate.

    `values` contains validated Decimal inputs from the website.
    Swiss tax and social-security deductions are user-supplied
    assumptions and are used only to estimate net home pay.
    """
    rate = values["exchange_rate"]
    annual_pay_chf = calculate_annual_pay(
        values["salary"], values["bonus"]
    )
    annual_pay_gbp = convert_chf_to_gbp(annual_pay_chf, rate)
    annual_housing = calculate_annual_housing_cost(values["housing"])

    relocation_allowance_gbp = convert_chf_to_gbp(
        values["relocation"], rate
    )
    taxable_relocation = calculate_taxable_relocation_cost(
        values["moving"], values["temporary"]
    )

    swiss_tax_chf = values.get("swiss_tax", Decimal("0"))
    swiss_social_chf = values.get("swiss_social_security", Decimal("0"))

    if (
        not swiss_tax_chf.is_finite()
        or not swiss_social_chf.is_finite()
        or swiss_tax_chf < 0
        or swiss_social_chf < 0
    ):
        raise ValueError("Swiss deductions must be non-negative.")

    net_home_pay_chf = max(
        Decimal("0"),
        annual_pay_chf - swiss_tax_chf - swiss_social_chf,
    )
    net_home_pay_gbp = convert_chf_to_gbp(net_home_pay_chf, rate)

    years = []

    for year_number in (1, 2):
        year_relocation_allowance = (
            relocation_allowance_gbp if year_number == 1 else Decimal("0")
        )
        year_moving = values["moving"] if year_number == 1 else Decimal("0")
        year_temporary = (
            values["temporary"] if year_number == 1 else Decimal("0")
        )
        year_taxable_relocation = (
            taxable_relocation if year_number == 1 else Decimal("0")
        )

        taxable_benefits = annual_housing + year_taxable_relocation
        taxable_income_before_gross_up = (
            annual_pay_gbp
            + annual_housing
            + year_relocation_allowance
            + year_taxable_relocation
        )

        grossed_up_tax = calculate_grossed_up_uk_tax(
            taxable_income_before_gross_up
        )

        employer_ni_earnings = (
            annual_pay_gbp + year_relocation_allowance
        )
        employer_class_1_ni = calculate_employer_class_1_ni(
            employer_ni_earnings
        )
        employer_class_1a_ni = calculate_class_1a_ni(taxable_benefits)

        direct_benefit_costs = (
            annual_housing
            + year_relocation_allowance
            + year_moving
            + year_temporary
        )
        total_cost = money(
            annual_pay_gbp
            + direct_benefit_costs
            + grossed_up_tax
            + employer_class_1_ni
            + employer_class_1a_ni
        )

        years.append({
            "year_number": year_number,
            "annual_pay_gbp": annual_pay_gbp,
            "housing_gbp": annual_housing,
            "relocation_allowance_gbp": year_relocation_allowance,
            "moving_gbp": year_moving,
            "temporary_housing_gbp": year_temporary,
            "taxable_relocation_gbp": year_taxable_relocation,
            "taxable_income_before_gross_up_gbp": money(
                taxable_income_before_gross_up
            ),
            "grossed_up_tax_gbp": grossed_up_tax,
            "employer_class_1_ni_gbp": employer_class_1_ni,
            "employer_class_1a_ni_gbp": employer_class_1a_ni,
            "total_cost_gbp": total_cost,
            "net_home_pay_gbp": net_home_pay_gbp,
            "cost_multiple": (
                (total_cost / net_home_pay_gbp).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                if net_home_pay_gbp > 0
                else None
            ),
        })

    return {
        "years": years,
        "total_assignment_cost_gbp": money(
            sum((year["total_cost_gbp"] for year in years), Decimal("0"))
        ),
        "net_home_pay_gbp": net_home_pay_gbp,
    }