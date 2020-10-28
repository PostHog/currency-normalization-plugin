async function fetchRatesIfNeeded(config) {
    const currencyRatesFetchedAt = await cache.get('currency_rates_fetched_at')
    if (!currencyRatesFetchedAt || currencyRatesFetchedAt < new Date().getTime() - 86400 * 1000) { // 24h
        await fetchRates(config)
    }
}

async function fetchRates(config) {
    try {
        const url = `https://openexchangerates.org/api/latest.json?app_id=${config['openExchangeRatesApiKey']}`
        const response = await fetch(url)
        const json = await response.json()

        if (json && json['rates']) {
            cache.set('currency_rates', json['rates'])
            cache.set('currency_rates_fetched_at', new Date().getTime())
        } else {
            console.error('🔺 Error fetching currency rates!')
            console.error(json)
        }
    } catch (e) {
        console.error('🔺 Error fetching currency rates!')
        console.error(e)
    }
}

function roundToDigits(number, digits) {
    return Math.round(number * Math.pow(10, digits)) / Math.pow(10, digits)
}
