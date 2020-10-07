from abc import ABC, abstractmethod
from openexchangerates import OpenExchangeRatesClient
from datetime import datetime, timedelta

import os

openexchangerates_api_key = os.environ.get('OPENEXCHANGERATES_API_KEY', None)
amount_property = os.environ.get("CNP_AMOUNT_PROPERTY", "amount")
currency_property = os.environ.get("CNP_CURRENCY_PROPERTY", "currency")
normalized_amount_property = os.environ.get("CNP_NORMALIZED_AMOUNT_PROPERTY", "normalized_amount")
normalized_currency_property = os.environ.get("CNP_NORMALIZED_CURRENCY_PROPERTY", "normalized_currency")
normalized_currency = os.environ.get("CNP_NORMALIZED_CURRENCY", None)

will_normalize = True

if not normalized_currency:
    print("🔻 Running posthog-maxmind-plugin without CNP_NORMALIZED_CURRENCY")
    print("🔺 No amounts will be normalized!")
    will_normalize = False

if not openexchangerates_api_key:
    print("🔻 Running posthog-maxmind-plugin without OPENEXCHANGERATES_API_KEY")
    print("🔺 No amounts will be normalized!")
    will_normalize = False


class Plugin(ABC):
    @abstractmethod
    def process_event(self, event):
        pass

    @abstractmethod
    def process_person(self, event):
        pass

    @abstractmethod
    def process_identify(self, event):
        pass


class CurrencyNormalizationPlugin(Plugin):
    def __init__(self):
        self.client = None
        self.currency_rates = None
        self.currency_rates_fetched_at = None
        if will_normalize:
            self.client = OpenExchangeRatesClient(openexchangerates_api_key)
            self.currency_rates = self.client.latest()['rates']
            self.currency_rates_fetched_at = datetime.now()

    def process_event(self, event):
        if will_normalize:
            # last fetched a day ago
            if not self.currency_rates or self.currency_rates_fetched_at < datetime.now() - timedelta(days=1):
                self.currency_rates = self.client.latest()['rates']
                self.currency_rates_fetched_at = datetime.now()

            amount = event.properties.get(amount_property, None)
            currency = event.properties.get(currency_property, None)
            if currency and self.currency_rates[currency] and self.currency_rates[normalized_currency]:
                normalized_amount = ((amount or 0) * self.currency_rates[normalized_currency] / self.currency_rates[currency]).round(round)
                event.properties[normalized_amount_property] = normalized_amount
                event.properties[normalized_currency_property] = normalized_currency

        return event
