import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Step 1: Retrieve historical data
ticker = "PLUG"
start_date = "2023-01-01"
end_date = "2024-07-31"
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Step 2: Prepare the data
closing_prices = stock_data['Close']

# Step 3: Apply ARIMA model
model = ARIMA(closing_prices, order=(5, 1, 0))  # ARIMA parameters: (p,d,q)
model_fit = model.fit()

# Step 4: Forecast for the next month (August)
forecast = model_fit.forecast(steps=31)  # Forecast for 31 days
forecast_dates = pd.date_range(start=closing_prices.index[-1], periods=31, freq='D')

# Step 5: Plot the results
plt.figure(figsize=(12, 6))
plt.plot(closing_prices, label='Historical Closing Prices')
plt.plot(forecast_dates, forecast, label='Forecast', color='red')
plt.title('Plug Power (PLUG) Price Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

# Print the forecasted prices
print(forecast)
