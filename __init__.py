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
else:
    coinoxr.app_id = openexchangerates_api_key


def fetch_rates():
    try:
        return coinoxr.Latest().get().body['rates']
    except:
        return None


currency_rates = None
currency_rates_fetched_at = None
if will_normalize:
    currency_rates = fetch_rates()
    currency_rates_fetched_at = datetime.now()


class CurrencyNormalizationPlugin(PluginBaseClass):
    def process_event(self, event: PosthogEvent):
        if will_normalize:
            global currency_rates
            global currency_rates_fetched_at

            # last fetched a day ago
            if not currency_rates or currency_rates_fetched_at < datetime.now() - timedelta(days=1):
                currency_rates = fetch_rates()
                currency_rates_fetched_at = datetime.now()

            if currency_rates:
                amount = event.properties.get(amount_property, 0)
                currency = event.properties.get(currency_property, None)
                if currency and currency_rates[currency] and currency_rates[normalized_currency]:
                    normalized_amount = round(amount * currency_rates[normalized_currency] / currency_rates[currency], 4)
                    event.properties[normalized_amount_property] = normalized_amount
                    event.properties[normalized_currency_property] = normalized_currency

        return event
