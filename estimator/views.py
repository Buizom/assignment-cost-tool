from decimal import Decimal, InvalidOperation

from django.shortcuts import render

from .calculations import calculate_assignment_costs


DEFAULTS = {
    "salary": "150000",
    "bonus": "20000",
    "housing": "3000",
    "relocation": "5000",
    "moving": "6000",
    "temporary": "4000",
    "exchange_rate": "1.10",
    "swiss_tax": "0",
    "swiss_social_security": "0",
}


def home(request):
    submitted_values = None
    results = None
    error = None

    if request.method == "POST":
        field_names = list(DEFAULTS.keys())

        try:
            submitted_values = {}

            for field in field_names:
                raw_value = request.POST.get(field, "").strip()
                value = Decimal(raw_value)

                if not value.is_finite() or value < 0:
                    raise ValueError

                submitted_values[field] = value

            if submitted_values["exchange_rate"] <= 0:
                raise ValueError

            results = calculate_assignment_costs(submitted_values)

        except (InvalidOperation, ValueError):
            submitted_values = None
            error = (
                "Please enter valid, non-negative numbers. "
                "The exchange rate must be greater than zero."
            )

    display_values = {
        key: str(value)
        for key, value in DEFAULTS.items()
    }

    if submitted_values:
        display_values.update({
            key: str(value)
            for key, value in submitted_values.items()
        })

    return render(
        request,
        "estimator/home.html",
        {
            "display_values": display_values,
            "submitted_values": submitted_values,
            "error": error,
            "results": results,
        },
    )