import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

class StockPortfolio:
    def __init__(self, filename='portfolio.csv'):
        self.filename = filename
        self.portfolio = pd.DataFrame(columns=['Ticker', 'Shares', 'Purchase Price'])
        self.load_portfolio()

    def add_stock(self, ticker, shares, purchase_price):
        """Add a stock to the portfolio."""
        self.portfolio = self.portfolio.append({
            'Ticker': ticker,
            'Shares': shares,
            'Purchase Price': purchase_price
        }, ignore_index=True)
        self.save_portfolio()

    def remove_stock(self, ticker):
        """Remove a stock from the portfolio."""
        self.portfolio = self.portfolio[self.portfolio['Ticker'] != ticker]
        self.save_portfolio()

    def get_portfolio_value(self):
        """Calculate the total value of the portfolio."""
        total_value = 0
        for index, row in self.portfolio.iterrows():
            stock_data = yf.Ticker(row['Ticker'])
            current_price = stock_data.history(period='1d')['Close'].iloc[-1]
            total_value += current_price * row['Shares']
        return total_value

    def get_performance(self):
        """Calculate and return the performance of each stock."""
        performance = []
        for index, row in self.portfolio.iterrows():
            stock_data = yf.Ticker(row['Ticker'])
            current_price = stock_data.history(period='1d')['Close'].iloc[-1]
            gain_loss = (current_price - row['Purchase Price']) * row['Shares']
            performance.append({
                'Ticker': row['Ticker'],
                'Current Price': current_price,
                'Gain/Loss': gain_loss
            })
        return pd.DataFrame(performance)

    def display_portfolio(self):
        """Display the current portfolio."""
        print("\nCurrent Portfolio:")
        print(self.portfolio)
        print(f"Total Portfolio Value: ${self.get_portfolio_value():.2f}")
        print("\nPerformance:")
        print(self.get_performance())

    def save_portfolio(self):
        """Save the portfolio to a CSV file."""
        self.portfolio.to_csv(self.filename, index=False)

    def load_portfolio(self):
        """Load the portfolio from a CSV file."""
        if os.path.exists(self.filename):
            self.portfolio = pd.read_csv(self.filename)

    def plot_stock(self, ticker):
        """Plot historical stock prices."""
        stock_data = yf.Ticker(ticker)
        hist = stock_data.history(period='1y')
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], label=ticker)
        plt.title(f'Historical Prices for {ticker}')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid()
        plt.show()

def main():
    portfolio = StockPortfolio()

    while True:
        print("\nOptions:")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Display Portfolio")
        print("4. Plot Stock Price")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            ticker = input("Enter stock ticker: ")
            shares = int(input("Enter number of shares: "))
            purchase_price = float(input("Enter purchase price per share: "))
            portfolio.add_stock(ticker, shares, purchase_price)
        elif choice == '2':
            ticker = input("Enter stock ticker to remove: ")
            portfolio.remove_stock(ticker)
        elif choice == '3':
            portfolio.display_portfolio()
        elif choice == '4':
            ticker = input("Enter stock ticker to plot: ")
            portfolio.plot_stock(ticker)
        elif choice == '5':
            print("Exiting the portfolio tracker.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

