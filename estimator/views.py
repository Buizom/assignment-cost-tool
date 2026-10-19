
from decimal import Decimal, InvalidOperation

from django.shortcuts import render
from .calculations import calculate_annual_housing_cost

def home(request):
    submitted_values = None
    results = None
    error = None

    if request.method == "POST":
        field_names = [
            "salary",
            "bonus",
            "housing",
            "relocation",
            "moving",
            "temporary",
            "exchange_rate",
        ]

        try:
            submitted_values = {}

            for field in field_names:
                value = Decimal(request.POST.get(field, ""))

                if not value.is_finite() or value < 0:
                    raise ValueError

                submitted_values[field] = value

            if submitted_values["exchange_rate"] <= 0:
                raise ValueError
            results = {
                "annual_housing_gbp": calculate_annual_housing_cost(
                    submitted_values["housing"]
                )
            }

        except (InvalidOperation, ValueError):
            submitted_values = None
            error = "Please enter valid, non-negative numbers and an exchange rate greater than zero."

    return render(
        request,
        "estimator/home.html",
        {
            "submitted_values": submitted_values,
            "error": error,
            "results": results,
        },
    )