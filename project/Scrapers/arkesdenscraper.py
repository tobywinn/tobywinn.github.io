import tabula
import pandas as pd

# Read remote pdf into a list of DataFrame
df = tabula.convert_into("project/Arkesden Banking Compensation Report 2020-2021.pdf", "project/ArkesdenData.csv", output_format='csv', lattice=True, pages=4)

df = pd.read_csv("project/ArkesdenData.csv")

# cant replace all in this case as yields bug due to * character
df['LEVEL'] = df['LEVEL'].str.replace("*", "")

df['LEVEL'] = df['LEVEL'].str.replace("\r", " ")
df = df.replace('£','', regex=True)

df['Analyst 3'] = df['Analyst 3'].str.replace("*", "", regex=False)

# get header titels which we will want at end
seniority = df.columns.tolist()
del seniority[10:]
seniority[0] = "Firm"

# make years new header
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header

# drop previous years values according to header value
df = df.drop('19-20', 1)

# rename header as we desire
df.columns = seniority

# format numbers so no k or K
df = df.replace('K','', regex=True)
df = df.replace('k','', regex=True)

# put the data in vega friendly format
df = df.melt(id_vars=["Firm"], var_name="Seniority", value_name="Compensation")

ratings = pd.read_csv("project/Banks data/BanksRatings.csv")

df = pd.merge(ratings, df, on="Firm",  how="outer")

df = df.drop('Unnamed: 0', 1)

# save
df.to_csv('project/ArkesdenData.csv')