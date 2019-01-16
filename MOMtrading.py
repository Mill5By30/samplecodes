 #Building mom trading strat
 
import numpy as np
import pandas as pd
import talib
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.factors import Latest
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.data import morningstar
from quantopian.pipeline.factors import CustomFactor, SimpleMovingAverage, AverageDollarVolume
from quantopian.pipeline.filters.morningstar import IsPrimaryShare
from quantopian.pipeline.data import morningstar as mstar
from quantopian.pipeline.classifiers.morningstar import Sector
from quantopian.pipeline.data.quandl import fred_usdontd156n as libor

# Trendline
    class Trendline(CustomFactor):
        inputs = [USEquityPricing.close]
        """
        52-Week Trendline:
        Slope of the linear regression across a 1 year lookback window.
        https://www.math.nyu.edu/faculty/avellane/Lo13030.pdf
        Notes:
        High value suggests momentum
        Calculated using the MLE of the slope of the regression 
        """
        window_length = 252

        def compute(self, today, assets, out, close):

            # array to store values of each security
            secs = []

            # days elapsed
            days = xrange(self.window_length)

            for col in close.T:
                # metric for each security
                col_cov = np.cov(col, days)
                secs.append(col_cov[0, 1] / col_cov[1, 1])
            out[:] = secs
            
  # 1-month Price Rate of Change
    class Price_Momentum_1M(CustomFactor):
        """
        1-Month Price Momentum:
        1-month closing price rate of change.
        https://www.pnc.com/content/dam/pnc-com/pdf/personal/wealth-investments/WhitePapers/FactorAnalysisFeb2014.pdf
        Notes:
        High value suggests momentum (shorter term)
        Equivalent to analysis of returns (1-month window)
        """
        inputs = [USEquityPricing.close]
        window_length = 21

        def compute(self, today, assets, out, close):
            out[:] = (close[-1] - close[0]) / close[0]
   
   # 3-month Price Rate of Change
    class Price_Momentum_3M(CustomFactor):
        """
        3-Month Price Momentum:
        3-month closing price rate of change.
        https://www.pnc.com/content/dam/pnc-com/pdf/personal/wealth-investments/WhitePapers/FactorAnalysisFeb2014.pdf
        Notes:
        High value suggests momentum (shorter term)
        Equivalent to analysis of returns (3-month window)
        """
        inputs = [USEquityPricing.close]
        window_length = 63

        def compute(self, today, assets, out, close):
            out[:] = (close[-1] - close[0]) / close[0]
            

  # 4/52 Price Oscillator
    class Price_Oscillator(CustomFactor):
        """
        4/52-Week Price Oscillator:
        Average close prices over 4-weeks divided by average close prices over 52-weeks all less 1.
        https://www.math.nyu.edu/faculty/avellane/Lo13030.pdf
        Used with the goal to explain where short term momentum is based off long term average in % difference
        Notes:
        High value suggests momentum
        """
        inputs = [USEquityPricing.close]
        window_length = 252            
   
  # 1-month Mean Reversion
    class Mean_Reversion_1M(CustomFactor):
        """
        1-Month Mean Reversion:
        1-month returns minus 12-month average of monthly returns over standard deviation
        of 12-month average of monthly returns.
        https://www.pnc.com/content/dam/pnc-com/pdf/personal/wealth-investments/WhitePapers/FactorAnalysisFeb2014.pdf
        Notes:
        High value suggests momentum (short term)
        Equivalent to analysis of returns (12-month window)
        """
        inputs = [USEquityPricing.close]
        window_length = 252

        def compute(self, today, assets, out, close):
            ret_1M = (close[-1] - close[-21]) / close[-21]
            ret_1Y_monthly = ((close[-1] - close[0]) / close[0]) / 12.
            out[:] = (ret_1M - np.nanmean(ret_1Y_monthly)) / \
                np.nanstd(ret_1Y_monthly)
