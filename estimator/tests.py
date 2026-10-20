
from decimal import Decimal

from django.test import SimpleTestCase

from .calculations import (
        calculate_annual_pay,
        convert_chf_to_gbp,
        calculate_uk_income_tax,
        calculate_grossed_up_uk_tax,
        calculate_annual_housing_cost,
        calculate_taxable_relocation_cost,
        calculate_assignment_costs,
        calculate_class_1a_ni,
        calculate_employer_class_1_ni,
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

    def test_taxable_relocation_cost(self):
        result = calculate_taxable_relocation_cost(
            Decimal("6000"),
            Decimal("4000"),
        )

        self.assertEqual(result, Decimal("2000")) 

    def test_employer_class_1_ni(self):
        result = calculate_employer_class_1_ni(Decimal("50000"))
        self.assertEqual(result, Decimal("6750.00"))

    def test_class_1a_ni(self):
        result = calculate_class_1a_ni(Decimal("36000"))
        self.assertEqual(result, Decimal("5400.00"))

    def test_assignment_costs_include_two_years(self):
        values = {
            "salary": Decimal("150000"),
            "bonus": Decimal("20000"),
            "housing": Decimal("3000"),
            "relocation": Decimal("5000"),
            "moving": Decimal("6000"),
            "temporary": Decimal("4000"),
            "exchange_rate": Decimal("1.10"),
            "swiss_tax": Decimal("0"),
            "swiss_social_security": Decimal("0"),
        }

        result = calculate_assignment_costs(values)

        self.assertEqual(len(result["years"]), 2)
        self.assertGreater(
            result["years"][0]["total_cost_gbp"],
            result["years"][1]["total_cost_gbp"],
        )
        self.assertEqual(
            result["years"][0]["taxable_relocation_gbp"],
            Decimal("2000.00"),
        )

    
    def test_assignment_total_matches_both_years(self):
        values = {
            "salary": Decimal("150000"),
            "bonus": Decimal("20000"),
            "housing": Decimal("3000"),
            "relocation": Decimal("5000"),
            "moving": Decimal("6000"),
            "temporary": Decimal("4000"),
            "exchange_rate": Decimal("1.10"),
            "swiss_tax": Decimal("31076"),
            "swiss_social_security": Decimal("10640.20"),
        }

        result = calculate_assignment_costs(values)

        expected_total = sum(
            year["total_cost_gbp"] for year in result["years"]
        )

        self.assertEqual(
            result["total_assignment_cost_gbp"],
            expected_total,
        )

    def test_year_two_has_no_relocation_costs(self):
        values = {
            "salary": Decimal("150000"),
            "bonus": Decimal("20000"),
            "housing": Decimal("3000"),
            "relocation": Decimal("5000"),
            "moving": Decimal("6000"),
            "temporary": Decimal("4000"),
            "exchange_rate": Decimal("1.10"),
            "swiss_tax": Decimal("31076"),
            "swiss_social_security": Decimal("10640.20"),
        }

        result = calculate_assignment_costs(values)
        year_two = result["years"][1]

        self.assertEqual(year_two["relocation_allowance_gbp"], Decimal("0.00"))
        self.assertEqual(year_two["moving_gbp"], Decimal("0.00"))
        self.assertEqual(year_two["temporary_housing_gbp"], Decimal("0.00"))
        self.assertEqual(year_two["taxable_relocation_gbp"], Decimal("0.00"))