# Data Ingestion

## What do we need from an API?

### Daily Close Price
To determine the quantity ratio for the day, so that notional is equal-weighted.

Should be available as raw data in any API.

### Daily Market Capitalization Data
To determine which 100 stocks will be included in the index. We will need daily historical values to determine historical composition(for at least 30 days)
#### Two possible approaches:
- Direct market cap value from last 30 days
- Calculated using (shares outstanding × daily price) from last 30 days

## Data sources

### Alpha Vantage API Endpoints

#### 1. Daily Time Series
- Provides:
  - Opening/Closing prices
  - High/Low prices
  - Trading volume
- Example response
```json
{
    "2025-10-07": {
        "1. open": "295.5500",
        "2. high": "301.0425",
        "3. low": "293.2850",
        "4. close": "293.8700",
        "5. volume": "7190126"
    }
}
```

#### 2. Overview Endpoint
- Provides current market cap directly
- Single API call
- Current values only
- Example response:
```json
{
    "MarketCapitalization": "2180000000000"
}
```

#### 3. Shares Outstanding Data
- Quarterly historical data
- Example response:
```json
{
    "date": "2025-06-30",
    "shares_outstanding_diluted": "7462000000",
    "shares_outstanding_basic": "7430000000"
}
```

