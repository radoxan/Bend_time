import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

def wycena_1(weight, bend_nums, price):
    w = (weight * 0.1) + ((bend_nums - 1.0) * (price - ((bend_nums - 1) * 0.01)))
    if w < 0:
        w = 0
    return w

def wycena_2(bend_nums, price):
    w = (price - ((bend_nums - 1) * 0.01)) * bend_nums
    if w < 0:
        w = 0
    return w

def wycena_3(weight, bend_nums, multi):
    w = (weight * 0.1) * (1.0 + (multi * (bend_nums - 1)))
    if w < 0:
        w = 0
    return w

def wycena_max(weight, bend_nums, price, multi):
    w1 = wycena_1(weight, bend_nums, price)
    w2 = wycena_2(bend_nums, price)
    w3 = wycena_3(weight, bend_nums, multi)
    w_max = max(w1, w2, w3)
    return w_max

st.title('Lista elementów')
parts_df = pd.read_json('parts.json', lines=True)

# Konwersja kolumn na typ liczbowy
parts_df['Długość'] = pd.to_numeric(parts_df['Długość'], errors='coerce')
parts_df['Rozwinięcie'] = pd.to_numeric(parts_df['Rozwinięcie'], errors='coerce')
parts_df['Grubość'] = pd.to_numeric(parts_df['Grubość'], errors='coerce')
parts_df['ilość gięć'] = pd.to_numeric(parts_df['ilość gięć'], errors='coerce')
parts_df['Masa'] = pd.to_numeric(parts_df['Masa'], errors='coerce')

# Usuwanie wierszy z wartościami NaN
parts_df = parts_df.dropna()

# Obliczanie nowej kolumny 'Wycena' dla każdego wiersza
parts_df['Wycena'] = parts_df.apply(lambda row: wycena_max(row['Masa'], row['ilość gięć'], 0.22, 0.25), axis=1)

# Pole tekstowe do wyszukiwania
search_query = st.text_input("Wyszukaj:", "")

# Filtrowanie DataFrame na podstawie zapytania wyszukiwania
if search_query:
    filtered_df = parts_df[parts_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
else:
    filtered_df = parts_df

# Wyświetlanie przefiltrowanego DataFrame w Streamlit
st.dataframe(filtered_df)
