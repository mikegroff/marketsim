"""MC2-P1: Market simulator.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Michael Groff
GT User ID: mgroff3 (replace with your User ID)
GT ID: 902772277 (replace with your GT ID)
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
        return 'mgroff3'

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    syms = df["Symbol"].values
    n = len(syms)
    syms = list(set(syms))
    m = len(syms)
    sh = np.zeros(m)

    i = 0
    cash = start_val

    start_date = df.index.min()
    end_date = df.index.max()
    dates = pd.date_range(start_date, end_date)
    prices_SPY = get_data(syms,dates)  # automatically adds SPY

    pSPY = prices_SPY['SPY']
    prices_SPY = prices_SPY.dropna()
    #pSPY.to_csv('spy.csv')
    dfo = prices_SPY
    df = prices_SPY.join(df,how = 'left')

    #df.to_csv('frame.csv')
    df = df.drop(['SPY'],axis = 1)

    pv = np.zeros(len(prices_SPY))
    ldate = end_date
    for row in df.itertuples():
        date = row[0].date()
        date = pd.date_range(date, date)
        sym = [row[1+m]]
        act = row[2+m]
        shares = row[3+m]

        if act=='BUY':
            symind = syms.index(sym[0])
            price = row[symind+1]*(1+impact)
            cash -= price*shares
            cash -= commission
            sh[symind] += shares
        elif act=='SELL':
            symind = syms.index(sym[0])
            price = row[symind+1]*(1-impact)
            cash += price*shares
            cash -= commission
            sh[symind] -= shares
        prices = np.asarray(row[1:m+1])
        value = np.sum(np.multiply(prices,sh))
        if ldate == date:
            pv[i-1] = cash + value
        else:
            pv[i] = cash + value
            i+=1
        ldate = date

    dfo["PortVal"] = pd.Series(pv, index = dfo.index)
    dfo = dfo.drop(['SPY'],axis = 1)
    portvals = dfo.drop(syms,axis = 1)
    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-01.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv,commission=0, impact=00)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    #print(portvals)
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = portvals.index.min()
    end_date = portvals.index.max()
    dates = pd.date_range(start_date, end_date)
    prices_SPY = get_data(['SPY'],dates)  # automatically adds SPY
    prices_SPY = prices_SPY['SPY']
    normspy = prices_SPY.div(prices_SPY.ix[0,:])
    normp = portvals.div(portvals.ix[0,:])
    dretspy = (normspy / np.roll(normspy, 1)) - 1
    dretspy = dretspy[1:]
    dretp = (normp / np.roll(normp, 1)) - 1
    dretp =dretp[1:]
    cum_ret = (normp[-1] / normp[0]) - 1
    avg_daily_ret = dretp.mean()
    std_daily_ret = dretp.std(ddof=1)
    sharpe_ratio = np.sqrt(252)*avg_daily_ret/std_daily_ret
    cum_ret_SPY = (normspy[-1]/normspy[0])   - 1
    avg_daily_ret_SPY = dretspy.values.mean()
    #print(avg_daily_ret_SPY)
    std_daily_ret_SPY = dretspy.values.std(ddof=1)
    sharpe_ratio_SPY = np.sqrt(252)*avg_daily_ret_SPY/std_daily_ret_SPY

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
