
from decimal import Decimal

from django.test import SimpleTestCase

from .calculations import (
        calculate_annual_pay,
        convert_chf_to_gbp,
        calculate_uk_income_tax,
        calculate_grossed_up_uk_tax,
        calculate_annual_housing_cost,
        )


class CalculationTests(SimpleTestCase):
    def test_annual_pay_adds_salary_and_bonus(self):
        result = calculate_annual_pay(
            Decimal("150000"),
            Decimal("20000"),
        )

        self.assertEqual(result, Decimal("170000"))

    def test_chf_to_gbp_conversion(self):
        result = convert_chf_to_gbp(
            Decimal("150000"),
            Decimal("1.10"),
        )

        self.assertEqual(
            result.quantize(Decimal("0.01")),
            Decimal("136363.64"),
        )

    def test_exchange_rate_must_be_positive(self):
        with self.assertRaises(ValueError):
            convert_chf_to_gbp(
                Decimal("150000"),
                Decimal("0"),
            )

    def test_negative_salary_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_annual_pay(
                Decimal("-1000"),
                Decimal("20000"),
            )
    
    def test_uk_tax_on_50000(self):
        result = calculate_uk_income_tax(Decimal("50000"))
        self.assertEqual(result, Decimal("7486.00"))

    def test_uk_tax_on_150000(self):
        result = calculate_uk_income_tax(Decimal("150000"))
        self.assertEqual(result, Decimal("53703.00"))

    def test_negative_income_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_uk_income_tax(Decimal("-1"))

    
    def test_grossed_up_tax_covers_tax_on_tax(self):
        income = Decimal("50000")
        tax = calculate_grossed_up_uk_tax(income)

        self.assertEqual(
            tax,
            calculate_uk_income_tax(income + tax),
        )

    def test_gross_up_rejects_negative_income(self):
        with self.assertRaises(ValueError):
            calculate_grossed_up_uk_tax(Decimal("-1"))

    def test_annual_housing_cost(self):
        result = calculate_annual_housing_cost(Decimal("3000"))

        self.assertEqual(result, Decimal("36000")) 