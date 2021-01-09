
# %% Import danych
import pandas as pd

df = pd.read_csv(r'DANE.csv', encoding= 'unicode_escape')

#%% Weryfikacja kolumn
columns = df.columns.tolist()
print(columns)

# %% Typy danych w kolumnach

print(df.dtypes)


# %% Weryfikacja pustych wartosci

print(df.isnull().sum())

# %% Opis danych

desc = df.describe()
descObj = df.describe(include='object')

print(desc)
print(descObj)

# %% Unikatowe wartosci
unikalne_nazwa = df['Nazwa'].unique()
