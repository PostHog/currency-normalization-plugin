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
    "path": "https://github.com/PostHog/posthog-currency-normalization-plugin",
    "config": {
        "openexchangerates_api_key": "COPY KEY HERE",
        "normalized_currency": "EUR"
    }
}
```
5. Optionally update some of the other variables:
```json
{
    "openexchangerates_api_key": "",
    "normalized_currency": "",
    "amount_property": "amount",
    "currency_property": "currency",
    "normalized_amount_property": "normalized_amount",
    "normalized_currency_property": "normalized_currency"
}
```
6. Run PostHog
