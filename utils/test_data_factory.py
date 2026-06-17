"""Generates randomized but realistic test data using Faker, so checkout
and API tests don't rely on hardcoded values that could collide or go
stale."""
from faker import Faker

fake = Faker()


class TestDataFactory:
    @staticmethod
    def random_checkout_info() -> dict:
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "postal_code": fake.postcode(),
        }

    @staticmethod
    def random_user_payload() -> dict:
        return {
            "name": fake.name(),
            "job": fake.job(),
        }

    @staticmethod
    def random_email() -> str:
        return fake.email()
