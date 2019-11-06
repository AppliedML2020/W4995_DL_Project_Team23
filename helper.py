import numpy as np
import pandas as pd
import math
import seaborn as sns

def get_data(stock_name, 
        start_train = '2010-01-01 01:00:00',end_train = '2015-12-31 04:00:00',
        start_test = '2016-01-01 01:00:00' , end_test = '2018-12-31 12:00:00',
        key = 'close'):
    
    print("-"*30)
    print("We are training from {} to {} ".format(start_train,end_train))
    print("And testing from {} to {} ".format(start_test, end_test))
    print("-"*30)
    df = pd.read_csv("./data/"+stock_name+".csv")
    train = list(df[(df['timestamp'] >= start_train) & (df['timestamp'] <= end_train)][key])
    test = list(df[(df['timestamp'] >= start_test) & (df['timestamp'] <= end_test)][key])
    return train, test

def get_state(data, t, n):
    # This function takes in inputs and return the states for MDP
	d = t - n + 1
	block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1]
	res = []
	for i in range(n - 1):
		res.append(sigmoid(block[i - 1] - block[i]))

	return np.array([res])

def get_state2(data, t, window_size):
    # This function takes in inputs and return the states for MDP
    d = t - window_size
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1]
    return get_return(block,  window_size-1, True)

def evaluate(series):
    '''
    Input: A list of returns
    The function evalutes a series of close price by computing the average rate of return and sharpe ratio.
    Output: Rate of Return, Sharpe Ratio
    * The risk free rate is set as 1.55
    '''
    series = np.array(series)
    rate_returns = get_return(series, len(series), False)
    rate_return_avg = 250*np.mean(rate_returns)
    sharpe_ratio =(rate_return_avg-0.0155)/np.sqrt(np.var(rate_returns))
    return rate_return_avg, sharpe_ratio

def get_return(lst,n, m ):
    res = []
    for i in range(n-1):
        # Computing the return rate
        if m :
            res.append(sigmoid(lst[i - 1] - lst[i]))
        else :
            res.append((lst[i] - lst[i-1])/lst[i-1])
            
    return np.array(res)

def sigmoid(x):
    return 1 / (1+math.exp(-x))

def benchmark(start ='2016-01-01 01:00:00',end = '2018-12-31 12:00:00'):
    df = pd.read_csv('./data/sp500.csv')
    series = list(df[(df['timestamp'] >= start) & (df['timestamp'] <= end)]['close'])
    a,b  = evaluate(series)
    print("The evaluation of S&P500 (Basline): Rate of Return {}, Sharpe Ratio {}".format(a,b) )
    return a,b

def action_plot(tracker,l):
    dat = pd.DataFrame(tracker)
    x = [i+1 for i in range(l)]
    sns.set_style("whitegrid")
    sns.scatterplot(x, y  = 'close',hue = 'action', style= 'action', palette="inferno", data = dat)
    sns.lineplot(x, y  = 'close',data = dat)