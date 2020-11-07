async function setupTeam({ config, cache }) {
    const apiKey = config['openExchangeRatesApiKey'] || null

    if (apiKey) {
        await fetchRatesIfNeeded(config, cache)
    } else {
        throw new Error('No API key found!')
    }
}

async function processEvent(event, { config, cache }) {
    const {
        openExchangeRatesApiKey,
        normalizedCurrency,
        amountProperty,
        currencyProperty,
        normalizedAmountProperty,
        normalizedCurrencyProperty,
    } = config

    if (
        openExchangeRatesApiKey &&
        normalizedCurrency &&
        event?.properties &&
        typeof event.properties[amountProperty] !== 'undefined' &&
        typeof event.properties[currencyProperty] !== 'undefined'
    ) {
        await fetchRatesIfNeeded(config, cache)
        const rates = await cache.get('currency_rates')

        if (rates) {
            const amount = event.properties[amountProperty]
            const currency = event.properties[currencyProperty]

            if (rates[currency] && rates[normalizedCurrency]) {
                const normalizedAmount = roundToDigits(amount * rates[normalizedCurrency] / rates[currency], 4)
                event.properties[normalizedAmountProperty] = normalizedAmount
                event.properties[normalizedCurrencyProperty] = normalizedCurrency
            }
        }
    }

    return event
}
