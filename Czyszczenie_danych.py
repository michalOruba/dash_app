
# %% Import danych
import pandas as pd

df = pd.read_csv(r'DANE.csv', encoding= 'unicode_escape')

# %% Pobranie wierszy zawierające puste wartosci

puste_wartosci = df[df['zgony'].isna()]

puste_wartosci_zgony_1996_1997 = puste_wartosci.loc[(puste_wartosci['Rok'] == 1996) | (puste_wartosci['Rok'] == 1997)]



# %% Poprawne nazwy województw
poprawne_nazwy = df.loc[(~df['Nazwa'].str.isalpha())]

# %% Usuniecie wierszy z brakiem danych

df_bez_lat_1996_1997 = df.drop(df[(df.Rok == 1996) | (df.Rok == 1997)].index)
df_bez_lat_1996_1997 = df_bez_lat_1996_1997.reset_index(drop=True)



# %% Uzupelnienie brakujacych wartosci dla roku 1998
from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors=8)
df_bez_lat_1996_1997_drop_name = df_bez_lat_1996_1997.drop(columns='Nazwa')
df_bez_lat_1996_1997_uzupelnione_1998 = pd.DataFrame(imputer.fit_transform(
                    df_bez_lat_1996_1997_drop_name), 
                    columns = df_bez_lat_1996_1997_drop_name.columns)


df_uzupelnione = df_bez_lat_1996_1997.copy()
df_uzupelnione.loc[df_bez_lat_1996_1997_uzupelnione_1998.index, 'zgony'] = df_bez_lat_1996_1997_uzupelnione_1998


print(df_uzupelnione.isnull().sum())


# %% dodanie kolumny z liczba zgonow w przeliczeniu na 100 000 mieszkancow
df_obliczone = df_uzupelnione.copy()

df_obliczone['Zgony_per_100k'] = (df_uzupelnione.zgony / df_uzupelnione.populacja) * 100000
df_obliczone['Zgony_per_100k'] = df_obliczone['Zgony_per_100k'].round(2)


# %% Formatowanie nazw wojewodztw

df_poprawa_nazw = df_obliczone.copy()
df_poprawa_nazw['Nazwa'] = df_poprawa_nazw['Nazwa'].str.title()

df_poprawa_nazw['Nazwa'] = df_poprawa_nazw['Nazwa'].str.replace(r"\SwieTokrzyskie\b", "Swietokrzyskie")


# %% Zapis pliku wynikowego
df_poprawa_nazw.to_csv(r'DANEOczyszczone.tsv', sep='\t')










