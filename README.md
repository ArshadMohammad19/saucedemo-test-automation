# SauceDemo Test Automation Framework

A full end-to-end (UI) and API test automation framework built with **Python**, **Playwright**, and **pytest** — featuring the Page Object Model, data-driven testing, Allure reporting, Docker containerization, and a GitHub Actions CI/CD pipeline.

This project was built as a QA portfolio piece to demonstrate practical, production-style test automation skills: not just "tests that pass," but a framework with the structure, tooling, and reporting that real QA teams expect.

**[View the live Allure test report →](https://arshadmohammad19.github.io/saucedemo-test-automation/)**

## What this project demonstrates

- **Page Object Model (POM)** — clean separation between test logic and UI locators/interactions
- **pytest fixtures & conftest** — reusable setup (browser config, page objects, authenticated sessions, API client)
- **UI + API testing in one framework** — Playwright for the browser, `requests` for REST API coverage
- **Config-driven design** — environment variables (`.env`) for secrets/environment values, YAML for static test settings
- **Data-driven tests** — `pytest.mark.parametrize` for negative/edge cases, Faker for dynamic test data
- **Failure diagnostics** — automatic screenshot capture, logging, and trace-friendly setup on test failure
- **Allure reporting** — rich, navigable HTML test reports with feature/story tagging
- **Retry handling** — `pytest-rerunfailures` to absorb flaky network blips without masking real bugs
- **Containerization** — Dockerfile + docker-compose for environment-independent test runs
- **CI/CD** — GitHub Actions workflow that runs smoke tests on every push, full regression nightly, and publishes the Allure report to GitHub Pages

## Tech stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Playwright | Browser automation (UI tests) |
| pytest | Test runner & fixtures |
| requests | API testing |
| Allure | Test reporting |
| Docker | Containerized execution |
| GitHub Actions | CI/CD pipeline |
| Faker | Dynamic test data generation |

## Application under test

- **UI**: [SauceDemo](https://www.saucedemo.com) — a purpose-built demo e-commerce site for test automation practice, including seeded edge cases (locked-out user, UI-bug user, slow-performance user).
- **API**: [JSONPlaceholder](https://jsonplaceholder.typicode.com) — a free, no-auth REST API used for CRUD-style test coverage independent of the UI.

## Project structure

```
saucedemo-test-automation/
├── config/
│   ├── config.yaml          # Static, non-secret test settings
│   └── settings.py           # Merges .env + config.yaml into one Settings object
├── pages/
│   ├── base_page.py          # Shared Playwright helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/
│   │   ├── test_login.py
│   │   ├── test_inventory.py
│   │   ├── test_cart.py
│   │   └── test_checkout.py
│   └── api/
│       └── test_jsonplaceholder_api.py
├── utils/
│   ├── api_client.py         # Thin requests wrapper with logging
│   ├── logger.py             # Console + file logger
│   └── test_data_factory.py  # Faker-based dynamic test data
├── .github/workflows/ci.yml  # GitHub Actions pipeline
├── conftest.py                # Fixtures, browser config, failure screenshots
├── pytest.ini                 # Markers, addopts, test discovery
├── Dockerfile
├── docker-compose.yml
├── Makefile                   # Convenience commands
├── requirements.txt
├── .env.example
└── README.md
```

## Getting started

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
git clone https://github.com/<your-username>/saucedemo-test-automation.git
cd saucedemo-test-automation

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
playwright install --with-deps chromium

cp .env.example .env              # adjust values if needed
```

### Running tests

```bash
# Smoke tests only (fast critical-path checks)
pytest -m smoke

# Full regression suite
pytest -m regression

# API tests only
pytest -m api

# Everything, in parallel across 4 workers
pytest -n 4

# Generate and view the Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

Or use the included `Makefile`:

```bash
make smoke
make regression
make report
```

### Running with Docker

```bash
docker compose up --build
```

This runs the suite inside a container preloaded with Playwright browsers and OS dependencies, and writes Allure results, screenshots, and logs back to your local `allure-results/`, `screenshots/`, and `logs/` folders.

## CI/CD

Every push to `main` triggers the GitHub Actions workflow (`.github/workflows/ci.yml`), which:

1. Installs dependencies and Playwright browsers
2. Runs the smoke suite on every push/PR
3. Runs the full regression + API suite on a nightly schedule (and on manual trigger)
4. Uploads Allure results, failure screenshots, and logs as build artifacts
5. Publishes the Allure HTML report to GitHub Pages

## Test design notes

- **Negative testing is treated as first-class**, not an afterthought: locked-out users, invalid credentials, missing required fields, and a known SauceDemo UI bug (`problem_user`) are all explicitly covered.
- **Business-logic assertions**, not just "did the page load": checkout totals are verified as `subtotal + tax == total`, sort orders are verified programmatically rather than visually.
- **API tests are independent of the UI** to keep the suite fast and to demonstrate REST API testing skills separately from browser automation.
- Locators prefer `data-test` attributes where SauceDemo provides them, falling back to stable CSS selectors otherwise — avoiding brittle XPath where possible.

## Possible extensions

- Visual regression testing (Playwright screenshot comparison)
- Cross-browser matrix (Firefox, WebKit) in CI
- Database/backend validation layer if a non-mock backend is introduced
- Load testing integration (e.g. Locust) for the same endpoints

## License

MIT — feel free to fork and adapt for your own portfolio.
