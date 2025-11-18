📈 Stock Predictor:

A web application that predicts stock prices using Simple Moving Average (SMA) analysis. Built with Flask, C++, and modern web technologies Features

Real-time stock data from Yahoo Finance
SMA calculations for 5, 10, 20, and 30-day periods
Interactive price charts
Multi-currency support (USD, EUR, GBP, JPY, INR, etc.)
Dark/Light theme
52-week high/low tracking
Responsive design

Requirements:
1) Python 3.8+
2) C++ compiler (g++)
3) pip

🏗️ Architecture
## Architecture
```
Frontend (HTML/CSS/JS)
         ↓
    Flask Backend
         ↓
    ┌────┴────┐
    ↓         ↓
yfinance    C++ Core
  API       Engine
```


How It Works:
1) Enter a stock symbol (e.g., AAPL, MSFT)
2) Select SMA period (5, 10, 20, or 30 days)
3) The app fetches historical data and calculates the moving average
4) View predictions with confidence metrics and price charts

Technology Stack:

Backend: Flask, Python
Core Engine: C++ with nlohmann/json
Frontend: HTML, CSS, JavaScript
Charts: Chart.js
Data Source: Yahoo Finance API
