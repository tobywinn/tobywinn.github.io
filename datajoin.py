import pandas as pd

df = pd.read_csv('BanksAverage.csv')
ratingdf = pd.read_csv('BanksRatings.csv')

df = df.set_index('Firm').join(ratingdf.set_index('Firm'))

df = df.drop(df.columns[4],axis=1)
df = df.drop(df.columns[0:3],axis=1)

df.to_csv('BanksSalaryandRating.csv')
