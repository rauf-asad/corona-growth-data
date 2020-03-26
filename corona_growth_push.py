import pandas as pd
import os

confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
del confirmed['Province/State']
confirmed.rename(columns={'Country/Region': 'Country'}, inplace=True)
df = confirmed.melt(id_vars=['Country', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
df['Date'] = pd.to_datetime(df.Date)
df = df.sort_values(by='Date', ignore_index=True)
del df['Lat']
del df['Long']
df = df.groupby(['Country', 'Date']).sum().reset_index().sort_values('Date')
df = df.reset_index(drop=True)
df = df[df.Confirmed != 0]
df = df.sort_values('Date')
df = df.groupby(['Country', 'Date']).sum()
df = df.groupby(level=0).diff().fillna(df).reset_index()
df = df.sort_values(by='Date')
df['day'] = df.groupby('Country')['Date'].rank(ascending=True)
del df['Date']
df = df.groupby(['Country', 'day']).sum().groupby(level=0).cumsum()
df = df.reset_index()
df.to_csv('data.csv', index=False)
os.system('git add .')
os.system('git commit -m "Auto update"')
os.system('git push')