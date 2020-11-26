async function setupPlugin({ config, cache }) {
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
                const normalizedAmount = roundToDigits((amount * rates[normalizedCurrency]) / rates[currency], 4)
                event.properties[normalizedAmountProperty] = normalizedAmount
                event.properties[normalizedCurrencyProperty] = normalizedCurrency
            }
        }
    }

    return event
}

module.exports = {
    setupPlugin,
    processEvent,
}

// Internal library functions below

async function fetchRatesIfNeeded(config, cache) {
    const currencyRatesFetchedAt = await cache.get('currency_rates_fetched_at')
    if (!currencyRatesFetchedAt || currencyRatesFetchedAt < new Date().getTime() - 86400 * 1000) {
        // 24h
        await fetchRates(config, cache)
    }
}

async function fetchRates(config, cache) {
    try {
        const url = `https://openexchangerates.org/api/latest.json?app_id=${config['openExchangeRatesApiKey']}`
        const response = await fetch(url)
        const json = await response.json()

        if (json && json['rates']) {
            cache.set('currency_rates', json['rates'])
            cache.set('currency_rates_fetched_at', new Date().getTime())
        } else {
            throw new Error('Error fetching currency rates!')
        }
    } catch (e) {
        throw new Error('Error fetching currency rates!')
    }
}

function roundToDigits(number, digits) {
    return Math.round(number * Math.pow(10, digits)) / Math.pow(10, digits)
}
