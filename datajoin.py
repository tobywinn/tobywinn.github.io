import pandas as pd

df = pd.read_csv('BanksAverage.csv')
ratingdf = pd.read_csv('BanksRatings.csv')

df = df.set_index('Firm').join(ratingdf.set_index('Firm'))

df.to_csv('BanksSalaryandRating.csv')

ratings = [4.2, 4.0]
names1 = ['Astrazeneca', 'Glaxosmithkline']

df1 = pd.DataFrame([[i for i in names1],[i for i in ratings]]).T
print(df1)
