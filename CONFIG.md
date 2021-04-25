# Configuration
To use this program, you will need to create a configuration file named `config.yml` in the same directory as the program. Alternatively, you can also modify the [example configuration file](config.yml) included.

## API Key

This program uses the Yahoo Finance API, which is publicly available and does not require an API key for authentication.

## Parameters

### Required

refresh - Refresh interval in seconds (set to 0 for maximum performance). Can be any positive integer. Values from 10 to 60 are recommended.

theme - Colour theme of the program. Can be light, dark, or default. Default is recommended.

colour - Whether to use colour or stay in monochrome mode. May not work on some older terminals even if set to true. True is recommended.

sort - Key to sort listings by. Can be alpha (alphabetical by name), change (total change in the past 24 hours), symbol (alphabetical by symbol), trading (if the market is open), and value (USD value). Change is recommended.

reverse - Whether to reverse the default ascending sort order. True is recommended for most sorting keys.

prices - Currency that the prices are displayed in. Most of the ISO 4217 codes should work, but anything other than USD will be converted at market rates.

### Optional

stocks - A list of stocks, indicies, and ETFs, most symbols will work.

cryptos - A list of cryptocurrencies, the symbols aren't as standardised but most common ones will work.

forexes - A list of two currency symbols together, most ISO 4217 codes should work.

others - A list of bonds, futures, mutual funds, and more. Generally, anything tracked on [Yahoo Finance](https://finance.yahoo.com/) will work here.
