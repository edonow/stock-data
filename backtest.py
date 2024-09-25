import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

from indicators import SmaCross, EmaCross, MACDStrategy, MACD


def plot_macd_sgnal(data, n1, n2, n_signal):
    close = data['Close'].values
    macd, signal = MACD(close, n1, n2, n_signal)

    plt.figure(figsize=(12, 4))
    plt.plot(macd, label="MACD", color='blue')
    plt.plot(signal, label="Signal", color='red')
    plt.title("MACD and Signal Line")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    ticker_symbol = "AAPL"
    company_name = yf.Ticker(ticker_symbol).info.get("longName", "No comapany name")
    data = yf.download(ticker_symbol, start="2024-01-01")
    data = data[["Open", "High", "Low", "Close", "Volume"]]

    bt = Backtest(data, MACDStrategy, cash=50000, commission=0.001, exclusive_orders=True)
    output = bt.run()
    
    # output = bt.optimize(n1=range(1, 75), n2=range(1, 75), maximize="Equity Final [$]", constraint=lambda p: p.n1 < p.n2, max_tries=800, return_heatmap=False, random_state=1)
    output = bt.optimize(n1=range(2, 75), n2=range(2, 75), n_signal=range(1, 30), maximize="Equity Final [$]", constraint=lambda p: p.n1 < p.n2, max_tries=800, return_heatmap=False, random_state=1)
    
    print(company_name)
    print(f"{output.get("Equity Final [$]"):.4f}")
    print(f"{output.get("Return [%]"):.4f}%")
    print(f"\n  > {output._strategy}", end="\n\n")
    
    # plot_macd_sgnal(data, output._strategy.n1, output._strategy.n2, output._strategy.n_signal)

    bt.plot()
    
    
if __name__ == "__main__":
    main()
    
