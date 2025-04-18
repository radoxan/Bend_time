import streamlit as st
import pycaret.regression
import pandas as pd
import time
from datetime import datetime

# Inicjalizacja session_state
if 'choosen_parts' not in st.session_state:
    st.session_state['choosen_parts'] = []

if 'input_name' not in st.session_state:
    st.session_state['input_name'] = ''
if 'name' not in st.session_state:
    st.session_state['name'] = ''

if 'input_length' not in st.session_state:
    st.session_state['input_length'] = 0
if 'length' not in st.session_state:
    st.session_state['length'] = 0

if 'input_weight' not in st.session_state:
    st.session_state['input_weight'] = 0
if 'weight' not in st.session_state:
    st.session_state['weight'] = 0

if 'input_width' not in st.session_state:
    st.session_state['input_width'] = 0
if 'width' not in st.session_state:
    st.session_state['width'] = 0

if 'input_bends' not in st.session_state:
    st.session_state['input_bends'] = 0
if 'bends' not in st.session_state:
    st.session_state['bends'] = 0

if 'input_capacity' not in st.session_state:
    st.session_state['input_capacity'] = 0
if 'capacity' not in st.session_state:
    st.session_state['capacity'] = 0

def predict(capacity, weigth, width, length, bends):
    df = pd.DataFrame({
    'Capacity': [capacity],
    'Weigth': [weigth],
    'Width': [width],
    'Length': [length],
    'Bends': [bends]
     })
    model_name = pycaret.regression.load_model('bending_time_regression_compress')
    predictions = pycaret.regression.predict_model(model_name, data=df)
    time_in_minutes = float(predictions['prediction_label'].iloc[0])
    hours = int(time_in_minutes // 60)
    minutes = int(time_in_minutes % 60)
    formatted_minutes = f"{minutes:02}"
    seconds = int((time_in_minutes - hours * 60 - minutes) * 60)
    formatted_seconds = f"{seconds:02}"
    st.header(f'Czas na wykonanie elementów to: {hours}:{formatted_minutes}:{formatted_seconds}')

def przechwyc_wartosci():
    st.session_state['input_name'] = str(st.session_state['name'])
    st.session_state['input_length'] = float(st.session_state['length'])
    st.session_state['input_width'] = float(st.session_state['width'])
    st.session_state['input_weight'] = float(st.session_state['weight'])
    st.session_state['input_bends'] = int(st.session_state['bends'])
    st.session_state['input_capacity'] = int(st.session_state['capacity'])

# Wczytanie danych
df_1 = pd.read_excel('Bend_parts_data.xlsx')
df_1.to_json('parts.json', orient='records', lines=True)

# Odczyt danych z pliku JSON
parts_df = pd.read_json('parts.json', lines=True)
parts_df['Masa'] = pd.to_numeric(parts_df['Masa'])
parts_df = parts_df.dropna(subset=['Numer'])

# Streamlit input and selection
col1, col2 = st.columns(2)
with col1:
    options = parts_df['Numer']
    search_number = st.text_input('Wprowadź numer do wyszukania')
    wyniki = parts_df[parts_df['Numer'].str.startswith(search_number)]['Numer'].tolist()
    choosen_draw = st.selectbox("Wybierz jeden z poniższych plików", wyniki)
    st.text(f'Wybrano plik: {choosen_draw}')
    choosen_row = parts_df.loc[parts_df['Numer'] == choosen_draw]
    st.dataframe(choosen_row)

    capacity = st.number_input('Podaj ilość', step=1, min_value=1)
    st.session_state['capacity'] = capacity    
    st.write(f'Ilość elementów do wykonania: {capacity}')
    st.session_state['name'] = choosen_row['Nazwa'].astype(str).iloc[0]
    st.session_state['weight'] = choosen_row['Masa'].astype(float).iloc[0]
    st.session_state['width'] = choosen_row['Rozwinięcie'].iloc[0]
    st.session_state['length'] = choosen_row['Długość'].astype(float).iloc[0]
    st.session_state['bends'] = choosen_row['ilość gięć'].iloc[0]
    choosen_row['Ilość'] = st.session_state['capacity']
    st.button(label="Wczytaj dane wybranego detalu", on_click=przechwyc_wartosci)

with col2:
    name = st.text_input(label="Podaj nazwę", value=st.session_state['input_name'])
    length = st.number_input(label="Podaj długość", max_value=float(6100), min_value=float(0), value=float(st.session_state['input_length']), step=float(1))
    width = st.number_input(label="Podaj rozwinięcie", max_value=float(3000), min_value=float(0), value=float(st.session_state['input_width']), step=float(1))
    weigth = st.number_input(label="Podaj wagę", min_value=float(0), max_value=float(100), step=float(1), value=float(st.session_state['input_weight']))
    bends = st.number_input(label="Ilość gięć", step=int(1), min_value=int(0), max_value=int(12), value=int(st.session_state['bends']))
    capacity = st.number_input(label="Ilość sztuk", step=int(1), min_value=int(0), value=int(st.session_state['capacity']))

    df = pd.DataFrame({
        'Capacity': [capacity],
        'Weigth': [weigth],
        'Width': [width],
        'Length': [length],
        'Bends': [bends]
    })

    st.dataframe(df)

    if st.button(label="Oblicz"):
        if length == 0:
            st.header("Podaj długość")
        elif width == 0:
            st.header('Podaj rozwinięcie')
        elif weigth == 0:
            st.header('Podaj wagę')
        elif bends == 0:
            st.header('Podaj ilość gięć')
        elif capacity == 0:
            st.header('Podaj ilość sztuk')
        else:
            predict(capacity, weigth, width, length, bends)
            time.sleep(5)