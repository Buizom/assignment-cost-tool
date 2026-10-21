# Assignment Cost Estimator

## 1. Project Overview

The Assignment Cost Estimator is a full-stack web application built with Python and Django. It estimates the employer cost of assigning a Swiss employee from Zurich to London for two years, from 6 April 2026 to 5 April 2028.

The application allows users to enter salary, bonus, housing, relocation expenses, exchange rates and hypothetical Swiss deductions. It estimates net home pay, UK tax gross-up and total employer assignment cost for each year and across the full assignment.

The application also provides guidance on UK work visas, business visits, passport requirements and official sources.

This is an illustrative cost-estimation tool for the assignment brief, not professional tax, legal or immigration advice.

## 2. Features

- Input form for salary, bonus, housing, relocation costs and exchange rate.
- Conversion of Swiss francs (CHF) to British pounds (GBP).
- Estimates of UK income tax using the 2026/27 England tax bands.
- Iterative UK tax gross-up calculation.
- Separate estimates for Year 1 and Year 2.
- Breakdown of assignment benefits and expenses, including their assumed tax treatment.
- Hypothetical Swiss income tax and social security deductions.
- Estimated employer assignment cost and cost multiple for each year.
- Immigration guidance with links to official sources.
- Input validation and automated tests.

## 3. Technology Stack

- **Python** — calculation logic and validation.
- **Django** — web framework and request handling.
- **HTML and CSS** — user interface.
- **Python `decimal` module** — monetary calculations using decimal arithmetic.
- **Django testing framework** — automated tests.
- **Git and GitHub** — version control and source-code hosting.

## 4. Project Structure

```text
assignment-cost-tool/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── estimator/
│   ├── templates/
│   │   └── estimator/
│   │       └── home.html
│   ├── calculations.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── .gitignore
└── README.md
```

`calculations.py` contains the main calculation functions. `views.py` handles user input and passes results to the template. `home.html` displays the form, estimates, assumptions and source links. `tests.py` contains automated tests for the calculation logic and expected behaviour.

## 5. Installation and Setup

### Prerequisites

Install Python and Git, and have Visual Studio Code available. The commands below use Windows PowerShell.

### Step 1: Clone the repository

```powershell
git clone https://github.com/Buizom/assignment-cost-tool.git
cd assignment-cost-tool
```

If the project is already on your computer, open its folder in VS Code and continue to Step 2.

### Step 2: Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, follow the Python documentation for your system's execution-policy settings, or activate the environment from a suitable terminal.

### Step 3: Install Django

```powershell
python -m pip install django
```

### Step 4: Apply database migrations

```powershell
python manage.py migrate
```

### Step 5: Start the development server

```powershell
python manage.py runserver
```

Open the obtained address in your browser.

To stop the server, press `Ctrl+C` in the terminal.

These instructions reflect the project's current dependencies.

## 6. Running the Tests

Run the automated test suite from the project root, with the virtual environment activated:

```powershell
python manage.py test
```

The tests cover key areas including:

- Annual salary and bonus calculations.
- CHF-to-GBP conversion and invalid exchange rates.
- UK income tax calculations and invalid income values.
- Tax gross-up calculations.
- Housing and relocation cost calculations.
- Employer National Insurance helper functions.
- Two-year assignment estimates and assignment totals.

The test suite helps verify that the calculations behave as expected for the tested inputs. Passing tests does not independently confirm that every tax or immigration assumption is legally correct.

## 7. Calculation Methodology

### Currency conversion

Swiss-franc amounts are converted to pounds using the user-provided exchange rate, expressed as CHF per GBP.

`GBP amount = CHF amount / CHF per GBP exchange rate`

### Home pay

Annual gross pay is the sum of salary and bonus. The hypothetical Swiss income tax and social security deductions are subtracted to estimate net home pay.

The Swiss deductions are inputs to the model, rather than a complete Swiss tax assessment.

### UK tax gross-up

The model estimates UK employment income tax using the 2026/27 England income tax bands and Personal Allowance.

The gross-up calculation starts with:

`I = net home pay + taxable assignment benefits`

It then iteratively estimates the tax payable on income including the tax itself:

`T = UKTax(I + T)`

The iteration stops when the calculated tax stabilises to the nearest penny, or raises an error if it does not converge within the configured limit.

### Assignment benefits and expenses

The model distinguishes between cash allowances, benefits in kind and direct assignment expenses. Employer-provided London housing is treated as a taxable benefit in the estimate. The relocation allowance is treated as taxable cash.

The model applies a simplified £8,000 qualifying relocation-expense exemption to moving and temporary-housing costs. Actual eligibility depends on the expense type and the relevant conditions, so the taxable relocation amount is an estimate.

### Employer assignment cost

The total cost calculation combines estimated net home pay, direct assignment expenses, UK grossed-up tax and any employer National Insurance charges included in the model.

The displayed cost multiple compares annual employer assignment cost with estimated net home pay.

## 8. Key Assumptions and Limitations

- The assignment runs from 6 April 2026 to 5 April 2028.
- UK income tax is estimated using the 2026/27 England rates for both years.
- The employee is assumed to be UK tax resident in both years.
- The employee is single, has no children and has three years of employment in Zurich.
- Annual salary is CHF 150,000 and annual bonus is CHF 20,000.
- Employer-provided housing costs £3,000 per month.
- The first year includes a CHF 5,000 cash relocation allowance, £6,000 in moving costs and £4,000 in temporary housing costs.
- The exchange rate is entered by the user; the default is £1 = CHF 1.10.
- Swiss income tax is a hypothetical input and must be verified separately for an actual employee.
- Swiss social security deductions are estimated inputs. The model does not calculate a complete Swiss tax return.
- The model assumes the employee remains covered by the Swiss social security system under an applicable coverage arrangement. UK National Insurance charges are therefore set to zero in the assignment estimate. This is an assumption, not a universal exemption; the applicable rules and documentation must be confirmed.
- The model does not include every possible tax relief, pension contribution, benefit, employer charge or individual circumstance.

Actual employer costs may differ depending on the employee's circumstances, applicable tax and social security rules, and the treatment of benefits and expenses.

## 9. Official Sources

The following official sources were consulted when developing the tax calculations and immigration guidance. The application simplifies some rules, so these sources should be checked before using the estimates for a real assignment.

### UK income tax

- [Income Tax rates and allowances for current and previous tax years — GOV.UK](https://www.gov.uk/government/publications/rates-and-allowances-income-tax/income-tax-rates-and-allowances-current-and-past)

Used to check the 2026/27 Personal Allowance, income tax bands and rates for England.

### Assignment benefits and relocation expenses

- [Expenses and benefits: relocation costs — what is exempt — GOV.UK](https://www.gov.uk/expenses-and-benefits-relocation/whats-exempt)
- [Expenses and benefits: relocation costs — what to report and pay — GOV.UK](https://www.gov.uk/expenses-and-benefits-relocation/what-to-report-and-pay)
- [Rates and thresholds for employers, 2026 to 2027 — GOV.UK](https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027)
- [Tax on company benefits — GOV.UK](https://www.gov.uk/tax-company-benefits)

These sources support research into qualifying relocation expenses, the £8,000 exemption, taxable benefits and employer National Insurance. The application uses a simplified estimate; not every moving or temporary-housing expense automatically qualifies.

### Swiss tax and social security

- [Zurich Cantonal Tax Office: tax calculator](https://www.zh.ch/de/steuern-finanzen/steuern/steuern-natuerliche-personen/steuererklaerung-natuerliche-personen/steuerrechner.html)
- [Social security contributions for workers coming to the UK from the EU, Iceland, Liechtenstein, Norway or Switzerland — GOV.UK](https://www.gov.uk/guidance/social-security-contributions-for-workers-coming-to-the-uk-from-the-eea-or-switzerland)
- [Tax if you come to the UK — GOV.UK](https://www.gov.uk/tax-come-to-uk)

These sources support checking the hypothetical Swiss tax estimate and researching social security coverage. The application assumes an applicable Swiss coverage arrangement and sets UK National Insurance charges to zero. That assumption must be verified for the employee's actual employment arrangement and documentation.

### UK immigration and business visits

- [Senior or Specialist Worker visa: overview — GOV.UK](https://www.gov.uk/senior-specialist-worker-visa)
- [Senior or Specialist Worker visa: eligibility — GOV.UK](https://www.gov.uk/senior-specialist-worker-visa/eligibility)
- [Visit the UK as a Standard Visitor: visit on business — GOV.UK](https://www.gov.uk/standard-visitor/visit-on-business)
- [Get an electronic travel authorisation (ETA) to visit the UK — GOV.UK](https://www.gov.uk/eta)
- [Entering the UK: before you leave for the UK — GOV.UK](https://www.gov.uk/uk-border-control/before-you-leave-for-the-uk)

These sources support research into a possible work visa route, permitted business visitor activities, ETA requirements and travel documents. The correct route depends on the person's nationality, job, sponsorship and intended activities.

These links provide official guidance, not a determination that a particular individual qualifies for a visa, tax exemption or social security arrangement.

## 10. AI Assistance Disclosure

AI assistance was used during development to support understanding of Django, review calculation logic, troubleshoot issues, suggest automated tests and improve project documentation.

The application was tested locally, and the calculations and assumptions were reviewed during development. AI-generated suggestions were treated as assistance rather than authoritative tax or immigration advice. The developer remains responsible for understanding and explaining the implementation and its limitations.

## 11. Demo Video

https://www.loom.com/share/9b6688331c41477f846368e565f05fdb

The demonstration will cover the running application, user inputs, two-year results, key calculation functions, automated tests and important assumptions.

## 12. Author

Developed as a candidate assignment demonstrating Python, Django, calculation logic, input validation, automated testing and documentation.
