import numpy as np
import pandas as pd
from pprint import pprint

# read file
df = pd.read_csv("GA_data.csv")
pprint(df.head())
pprint(df.columns)

# 1. Adding 10 days moving average
df['SMA_10'] = df.iloc[:,4].rolling(window=10).mean()


# 2. Adding 20 days moving average
df['SMA_20'] = df.iloc[:,4].rolling(window=20).mean()

# 3. Adding 50 days moving average
df['SMA_50'] = df.iloc[:,4].rolling(window=50).mean()

# 4. Adding 200 days moving average
df['SMA_200'] = df.iloc[:,4].rolling(window=200).mean()

# 5. Adding 12 days ROC
#Rate of Change  
def ROC(df, n):  
    M = df['Close'].diff(n - 1)  
    N = df['Close'].shift(n - 1)  
    ROC = pd.Series(M / N, name = 'ROC_' + str(n))  
    df = df.join(ROC)  
    return df

df  =  ROC(df, 12)


# 6. PPO Oscillator price = ((SMA_10 - SMA_20)/SMA_20) * 100

df['PPO'] = ((df['SMA_10']-df['SMA_20'])/df['SMA_20'])*100

# 7. 10 days bias >>> not found replaced by momentum
#Momentum  
def MOM(df, n):  
    M = pd.Series(df['Close'].diff(n), name = 'Momentum_' + str(n))  
    df = df.join(M)  
    return df

df  = MOM(df,15)

# 8. 20 days Volume rate of change
#Rate of Change Volume  
def ROC_Vol(df, n):  
    M = df['Volume'].diff(n - 1)  
    N = df['Volume'].shift(n - 1)  
    ROC = pd.Series(M / N, name = 'ROC-Vol_' + str(n))  
    df = df.join(ROC)  
    return df

df  = ROC_Vol(df, 20)


#Relative Strength Index  
def RSI(df, n):  
    i = 0  
    UpI = [0]  
    DoI = [0]  
    while i + 1 <= df.index[-1]:  
        UpMove = df.at[i + 1, 'High'] - df.at[i, 'High']  
        DoMove = df.at[i, 'Low'] - df.at[i + 1, 'Low']  
        if UpMove > DoMove and UpMove > 0:  
            UpD = UpMove  
        else: UpD = 0  
        UpI.append(UpD)  
        if DoMove > UpMove and DoMove > 0:  
            DoD = DoMove  
        else: DoD = 0  
        DoI.append(DoD)  
        i = i + 1  
    UpI = pd.Series(UpI)  
    DoI = pd.Series(DoI)  
    PosDI = pd.DataFrame.ewm(UpI, span = n, min_periods = n - 1).mean()
    NegDI = pd.DataFrame.ewm(DoI, span = n, min_periods = n - 1).mean() 
    RSI = pd.Series(PosDI / (PosDI + NegDI), name = 'RSI_' + str(n))  
    df = df.join(RSI)  
    return df
# 9. 10 days RSI
df = RSI(df,10)

# 10. 14 days RSI
df = RSI(df, 14)
# 11. 21 days RSI
df = RSI(df,21)
# 12. Stocastic Osillator (k%)
#Stochastic oscillator %K  
def STOK(df):  
    SOk = pd.Series((df['Close'] - df['Low']) / (df['High'] - df['Low']), name = 'SO%k')  
    df = df.join(SOk)  
    return df

df = STOK(df)

# Stochastic Oscillator, EMA smoothing, nS = slowing (1 if no slowing)  
def STO(df,  nK, nD, nS=1):  
    SOk = pd.Series((df['Close'] - df['Low'].rolling(nK).min()) / (df['High'].rolling(nK).max() - df['Low'].rolling(nK).min()), name = 'SO%k'+str(nK))  
    if nS ==1:
        name_ = 'SO'+str(nD)+'Fast'
    else:
        name_ = 'SO'+str(nD)+'Slow'
    SOd = pd.Series(SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), name = name_)  
    SOk = SOk.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    SOd = SOd.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    #df = df.join(SOk)  
    df = df.join(SOd)  
    return df 
# 13. Fast Stocastic (D%)

df = STO(df,15,5,1)

# 14. Slow stocastic (slow D)
df = STO(df,15,5,3)

# drop Null values
df  = df.dropna()

#view df
pprint(df.head(22))
pprint(df.columns)

# total values in the data frame
pprint(df.shape)

# Normalize every colum
def normalize(df):
    result = df.copy()
    for feature_name in df.columns[1:]:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result
normalize_df = normalize(df)
normalize_df['Open_new'] = df['Open']
pprint(normalize_df.head())
pprint(normalize_df.columns)
# write it to a file
#df.to_csv('GA_Data_with_TI.csv',index = False)
normalize_df.to_csv('GA_Data_with_TI_Normalized.csv',index = False)
