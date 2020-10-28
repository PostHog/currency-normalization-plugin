# posthog-currency-normalization-plugin

Normalize currencies in events. E.g. amounts in EUR, USD and GBP will all be converted to EUR.

## Setup

1. Install [posthog-cli](https://github.com/PostHog/posthog-cli)
2. Install this plugin: `posthog plugin install posthog-currency-normalization-plugin`
3. [Sign up](https://openexchangerates.org/) to OpenExchangeRates.org and get the API key
4. Edit `posthog.json` and add update the required config variables:
```json
{
    "name": "posthog-currency-normalization-plugin",
    "url": "https://github.com/PostHog/posthog-currency-normalization-plugin",
    "global": {
        "enabled": true,
        "config": {
            "openExchangeRatesApiKey": "<COPY KEY HERE>",
            "normalizedCurrency": "EUR",
            "amountProperty": "amount",
            "currencyProperty": "currency",
            "normalizedAmountProperty": "normalized_amount",
            "normalizedCurrencyProperty": "normalized_currency"
        }
    }
}
```
5. Run PostHog
