# posthog-currency-normalization-plugin

Normalize currencies in events. E.g. amounts in EUR, USD and GBP will all be converted to EUR.

## Setup via the PostHog

1. Find the "plugins" page in PostHog.
2. Either select the plugin from the list or copy the URL of this repository to install.
3. Update the required settings (get the API key [here](https://openexchangerates.org/)) and enable the plugin.

## Setup globally via CLI

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

## Questions?

### [Join our Slack community.](https://join.slack.com/t/posthogusers/shared_invite/enQtOTY0MzU5NjAwMDY3LTc2MWQ0OTZlNjhkODk3ZDI3NDVjMDE1YjgxY2I4ZjI4MzJhZmVmNjJkN2NmMGJmMzc2N2U3Yjc3ZjI5NGFlZDQ)
