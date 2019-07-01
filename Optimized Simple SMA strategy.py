# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:44:48 2019

@author: Kevin
"""

#importing bt for backtesting
import bt


#fetching data from google, amazon and spy to compare with the market
#doing 2 years and before 2017 to leave 2017 to 2019 as testing set
stock_data = bt.get('goog,amzn,spy', start ='06-01-2015',end = '05-31-2017')

""" creating a loop to find the best moving average from 14 to 200 by 
extracting data from the backtest & storing the CAGR """


#creating CAGR dataframe, need to import pandas first
import pandas as pd

CAGR_df = pd.DataFrame(columns = ['ma','CAGR'])


for x in range(14,201):
    #creating a moving average with the loop value
    ma = stock_data.rolling(x).mean()
    #creating a singal for when the price of the stock is higher than the ma
    signal = stock_data > ma
    #creating the strategy using bt
    s = bt.Strategy('abovesma', [bt.algos.SelectWhere(signal),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
    #create the backtest
    t = bt.Backtest(s, stock_data)
    #run the backtest
    res = bt.run(t)
    #save the CAGR
    CAGR = res.stats.at['cagr','abovesma']
    #store the CAGR and the ma in the CAGR_df Data Frame
    CAGR_df = CAGR_df.append({'ma': x,'CAGR': CAGR},ignore_index=True) 

"""loop functions properly, now will test to see if the right CAGR scores are
assigned by picking a random ma"""

#importing random
import random
randma = random.randint(14,200)
print(randma)

#using the randma in the backtest
ma_test = stock_data.rolling(randma).mean()
signal_test = stock_data > ma_test
s_test = bt.Strategy('abovesmatest', [bt.algos.SelectWhere(signal_test),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])  
t_test = bt.Backtest(s_test, stock_data)
res_test = bt.run(t_test)
res_test.display()

"loop works! CAGR matches the one in the dataframe"

#picking the max CAGR
max_index = CAGR_df['CAGR'].argmax()
print(max_index)

#assigning the best ma 
best_x = max_index + 1

best_ma = stock_data.rolling(best_x).mean()
#creating a singal for when the price of the stock is higher than the ma
signal2 = stock_data > best_ma
#creating the strategy using bt
s2 = bt.Strategy('abovesma2', [bt.algos.SelectWhere(signal2),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
#create the backtest
t2 = bt.Backtest(s2, stock_data)
#run the backtest
res2 = bt.run(t2)

res2.plot()
res2.display()


#will now test with the testing set for the last two years
stock_test_data = bt.get('goog,amzn,spy', start='06-01-2017',end ='05-31-2019')

ma_test_set = stock_test_data.rolling(best_x).mean()
#creating a singal for when the price of the stock is higher than the ma
signal_test_set = stock_test_data > ma_test_set
#creating the strategy using bt
s_test_set = bt.Strategy('abovesmatestset', [bt.algos.SelectWhere(signal_test_set),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
#create the backtest
t_test_set = bt.Backtest(s_test_set, stock_test_data)
#run the backtest
res_test_set = bt.run(t_test_set)

res_test_set.plot()
res_test_set.display()

""" this shows that even though we would have made a total return of 58.46% 
with the best moving average from 2015 to 2017, that strategy would only give a
total return of 18.21% having invested in google, amazon and spy in the last 
two years and CAGR dropped from 25% to 8.73% """


""" now going to create a function where can choose any stocks you want and
compare the training set with the testing set with set moving average to 50 """

def abovema_trainandtest(tickers, sma = 50, start_train = '06-01-2015', 
              end_train= '05-31-2017',start_test = '06-01-2017',
              end_test = '05-31-2019', name1 = 'above_sma50_train',
              name2='above_sma50_test'):
    #training test
    data_train=bt.get(tickers,start = start_train, end = end_train)
    sma_train = data_train.rolling(sma).mean()
    signal = data_train > sma_train
    s = bt.Strategy(name1, [bt.algos.SelectWhere(signal),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
   
    #testing set
    data_test = bt.get(tickers,start=start_test,end=end_test)
    sma_test = data_test.rolling(sma).mean()
    signal2 = data_test > sma_test
    s2 = bt.Strategy(name2,[bt.algos.SelectWhere(signal2),
                                     bt.algos.WeighEqually(),
                                     bt.algos.Rebalance()])
    return (bt.Backtest(s, data_train), bt.Backtest(s2,data_test))

 
    
above50 = abovema_trainandtest('goog,amzn,spy')
above62 = abovema_trainandtest('goog,amzn,spy',name1='above62train',name2='above52test')    

combined_results = bt.run(above50,above62)    
combined_results.plot()

""" above function does not work because cannot return two backtests in one 
function for now, will try smaller function and call it with different dates"""


def abovema(tickers, sma_days = 50, start = '06-01-2015', end= '05-31-2017',
            name = 'abovesma50train'):
    
    data=bt.get(tickers,start = start, end = end)
    sma = data.rolling(sma_days).mean()
    signal = data > sma
    s = bt.Strategy(name, [bt.algos.SelectWhere(signal),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
    return bt.Backtest(s,data)

tickers = 'goog,amzn,spy'
start_test = '06-01-2017'
end_test = '06-01-2019'

abovema50train = abovema(tickers)
abovema50test = abovema(tickers, start = start_test, end = end_test, 
                        name = 'above50test')
above62train = abovema(tickers, sma_days = 62, name = 'above62train')
above62test = abovema(tickers, sma_days = 62, start = start_test, 
                      end = end_test, name = 'above62test')

#running the backtests all at once to see the plot and results
combined_res = bt.run(abovema50train,abovema50test,above62train,above62test)
combined_res.plot(freq = 'm' )
combined_res.display()











    
