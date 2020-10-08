import coinoxr
import os

from posthog.plugins import PluginBaseClass, PosthogEvent
from datetime import datetime, timedelta

openexchangerates_api_key = os.environ.get('OPENEXCHANGERATES_API_KEY', None)
normalized_currency = os.environ.get("CNP_NORMALIZED_CURRENCY", None)

amount_property = os.environ.get("CNP_AMOUNT_PROPERTY", "amount")
currency_property = os.environ.get("CNP_CURRENCY_PROPERTY", "currency")
normalized_amount_property = os.environ.get("CNP_NORMALIZED_AMOUNT_PROPERTY", "normalized_amount")
normalized_currency_property = os.environ.get("CNP_NORMALIZED_CURRENCY_PROPERTY", "normalized_currency")

will_normalize = True

if not normalized_currency:
    print("🔻 Running posthog-maxmind-plugin without CNP_NORMALIZED_CURRENCY")
    print("🔺 No amounts will be normalized!")
    will_normalize = False

if not openexchangerates_api_key:
    print("🔻 Running posthog-maxmind-plugin without OPENEXCHANGERATES_API_KEY")
    print("🔺 No amounts will be normalized!")
    will_normalize = False

class CurrencyNormalizationPlugin(PluginBaseClass):
    def __init__(self):
        self.currency_rates = None
        self.currency_rates_fetched_at = None
        if will_normalize:
            coinoxr.app_id = openexchangerates_api_key
            self._fetch_rates()

    def _fetch_rates(self):
        try:
            self.currency_rates = coinoxr.Latest().get().body['rates']
            self.currency_rates_fetched_at = datetime.now()
        except:
            return None

    def process_event(self, event: PosthogEvent):
        if will_normalize:
            # last fetched a day ago
            if not self.currency_rates or self.currency_rates_fetched_at < datetime.now() - timedelta(days=1):
                self._fetch_rates()

            if self.currency_rates:
                amount = event.properties.get(amount_property, 0)
                currency = event.properties.get(currency_property, None)
                if currency and self.currency_rates[currency] and self.currency_rates[normalized_currency]:
                    normalized_amount = round(amount * self.currency_rates[normalized_currency] / self.currency_rates[currency], 4)
                    event.properties[normalized_amount_property] = normalized_amount
                    event.properties[normalized_currency_property] = normalized_currency

        return event
