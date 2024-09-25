import pandas as pd
import talib as ta

from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA


# ----------------------------------------------
# SMA class
# ----------------------------------------------
# EmaCross strategy class
class SmaCross(Strategy):
    n1 = 5  # ma10
    n2 = 25  # ma20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


# ----------------------------------------------
# EMA class
# ----------------------------------------------
def EMA(array, period):
    return ta.EMA(array, timeperiod=period)


# EmaCross strategy class
class EmaCross(Strategy):
    n1 = 5
    n2 = 25

    def init(self):
        close = self.data.Close
        self.ema1 = self.I(EMA, close, self.n1)
        self.ema2 = self.I(EMA, close, self.n2)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.buy()
        elif crossover(self.ema2, self.ema1):
            self.sell()


# ----------------------------------------------
# MACD class
# ----------------------------------------------
def MACD(array, n_fast, n_slow, n_signal):
    macd, signal, _ = ta.MACD(array, fastperiod=n_fast, slowperiod=n_slow, signalperiod=n_signal)
    return macd, signal


class MACDStrategy(Strategy):
    n1 = 12  # EMA period for fast line
    n2 = 26  # EMA period for slow line
    n_signal = 9  # signal line period

    def init(self):
        close = self.data.Close
        self.macd_line, self.signal_line = self.I(MACD, close, self.n1, self.n2, self.n_signal)

    def next(self):
        macd = self.macd_line[-1]

        # if crossover(self.macd_line, self.signal_line) or macd > 0:
        #     self.buy()

        # elif crossover(self.signal_line, self.macd_line) or macd < 0:
        #     self.sell()

        if crossover(self.macd_line, self.signal_line):
            self.buy()

        elif crossover(self.signal_line, self.macd_line):
            self.sell()
