.PHONY: install browsers smoke regression api all report docker-build docker-run clean

install:
	pip install -r requirements.txt

browsers:
	playwright install --with-deps chromium

smoke:
	pytest -m smoke --alluredir=allure-results

regression:
	pytest -m regression --alluredir=allure-results

api:
	pytest -m api --alluredir=allure-results

all:
	pytest --alluredir=allure-results

report:
	allure serve allure-results

docker-build:
	docker build -t saucedemo-qa-tests .

docker-run:
	docker compose up --build

clean:
	rm -rf allure-results allure-report screenshots logs .pytest_cache test-results playwright-report
