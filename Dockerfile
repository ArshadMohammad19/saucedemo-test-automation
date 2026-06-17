# Official Playwright image already has browsers + OS deps preinstalled,
# which avoids the most common CI flakiness source (missing system libs).
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure browsers are present even if the base image is updated upstream
RUN playwright install --with-deps chromium

ENV HEADLESS=true \
    PYTHONUNBUFFERED=1

CMD ["pytest", "--alluredir=allure-results"]
