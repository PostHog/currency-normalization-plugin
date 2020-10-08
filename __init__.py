import coinoxr
import os

from posthog.plugins import PluginBaseClass, PosthogEvent
from datetime import datetime, timedelta


class CurrencyNormalizationPlugin(PluginBaseClass):
    def __init__(self, config):
        super().__init__(config)

        self.openexchangerates_api_key = self.config.get("openexchangerates_api_key", None)
        self.normalized_currency = self.config.get("normalized_currency", None)

        self.amount_property = self.config.get("amount_property", "amount")
        self.currency_property = self.config.get("currency_property", "currency")
        self.normalized_amount_property = self.config.get("normalized_amount_property", "normalized_amount")
        self.normalized_currency_property = self.config.get("normalized_currency_property", "normalized_currency")

        self.will_normalize = True

        if not self.normalized_currency:
            print("🔻 Running posthog-maxmind-plugin without the 'normalized_currency' config key")
            print("🔺 No amounts will be normalized!")
            self.will_normalize = False

        if not self.openexchangerates_api_key:
            print("🔻 Running posthog-maxmind-plugin without 'openexchangerates_api_key' config key")
            print("🔺 No amounts will be normalized!")
            self.will_normalize = False

        self.currency_rates = self.cache.get("currency_rates")
        self.currency_rates_fetched_at = self.cache.get("currency_rates_fetched_at")

        if self.will_normalize:
            coinoxr.app_id = self.openexchangerates_api_key
            self._fetch_rates()

    def _fetch_rates(self):
        try:
            # last fetched a day ago
            if not self.currency_rates or self.currency_rates_fetched_at < datetime.now() - timedelta(days=1):
                self.currency_rates_fetched_at = datetime.now()
                self.currency_rates = coinoxr.Latest().get().body['rates']

                self.cache.set("currency_rates", self.currency_rates)
                self.cache.set("currency_rates_fetched_at", self.currency_rates_fetched_at)

        except Exception as e:
            print("🔺 Error fetching currency rates! {}: \"{}\"".format(type(e), e))

    def process_event(self, event: PosthogEvent):
        if self.will_normalize:
            self._fetch_rates()

            if self.currency_rates:
                amount = event.properties.get(self.amount_property, 0)
                currency = event.properties.get(self.currency_property, None)
                if currency and self.currency_rates[currency] and self.currency_rates[self.normalized_currency]:
                    normalized_amount = round(amount * self.currency_rates[self.normalized_currency] / self.currency_rates[currency], 4)
                    event.properties[self.normalized_amount_property] = normalized_amount
                    event.properties[self.normalized_currency_property] = self.normalized_currency

        return event
