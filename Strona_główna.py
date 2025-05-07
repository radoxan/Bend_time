import streamlit as st
import pycaret.regression
import pandas as pd
import time
from datetime import datetime


st.set_page_config(layout="wide")

# Inicjalizacja session_state
def initialize_session_state():
    values = {
        'choosen_parts': pd.DataFrame(),
        'new_df': pd.DataFrame(),
        'input_name': '',
        'name': '',
        'input_index': '',
        'index': '',
        'my_info': '',
        'info_visible': 0,
        'input_length': 0,
        'length': 0,
        'input_weight': 0,
        'weight': 0,
        'input_width': 0,
        'width': 0,
        'input_bends': 0,
        'bends': 0,
        'input_capacity': 0,
        'capacity': 0,
        'sumary_time': 0,
        'wycena_zlecenia': 0
    }

    for key, value in values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def wycena_1(weight, bend_nums, price):
    w = (weight*0.1)+((bend_nums-1.0)*(price-((bend_nums-1)*0.01)))
    if w < 0:
        w = 0
    return w

def wycena_2(bend_nums, price):
    w = (price-((bend_nums-1)*0.01))*bend_nums
    if w < 0:
        w = 0
    return w

def wycena_3(weight, bend_nums, multi):
    w = (weight*0.1)*(1.0+(multi*(bend_nums-1)))
    if w < 0:
        w = 0
    return w

def wycena_max(weight, bend_nums, price, multi):
    w1 = wycena_1(weight, bend_nums, price)
    w2 = wycena_2(bend_nums, price)
    w3 = wycena_3(weight, bend_nums, multi)
    w_max = max(w1,w2,w3)
    return w_max

def predict(capacity, weigth, width, length, bends):
    st.session_state['new_df'] = pd.DataFrame({
    'Capacity': [capacity],
    'Weigth': [weigth],
    'Width': [width],
    'Length': [length],
    'Bends': [bends]
     })
    model_name = pycaret.regression.load_model('bending_time_regression_compress')
    predictions = pycaret.regression.predict_model(model_name, data=st.session_state['new_df'])
    time_in_minutes = float(predictions['prediction_label'].iloc[0])
    hours = int(time_in_minutes // 60)
    minutes = int(time_in_minutes % 60)
    formatted_minutes = f"{minutes:02}"
    seconds = int((time_in_minutes - hours * 60 - minutes) * 60)
    formatted_seconds = f"{seconds:02}"
    predicted_time = f'{hours}:{formatted_minutes}:{formatted_seconds}'
    with st.spinner(text='Liczę czas wykonania...'):
        time.sleep(3)
    st.header(f'Czas na wykonanie elementów to: {predicted_time}')
    st.session_state['new_df']['Time'] = predicted_time

def przechwyc_wartosci():
    st.session_state['input_name'] = str(st.session_state['name'])
    st.session_state['input_length'] = float(st.session_state['length'])
    st.session_state['input_width'] = float(st.session_state['width'])
    st.session_state['input_weight'] = float(st.session_state['weight'])
    st.session_state['input_bends'] = int(st.session_state['bends'])
    st.session_state['input_capacity'] = int(st.session_state['capacity'])
    st.session_state['input_index'] = str(st.session_state['index'])

def licz_czas():
    df = pd.DataFrame()
    df['time'] = pd.to_timedelta(st.session_state['choosen_parts']['Time'])
    total_time = df['time'].sum()
    total_seconds = int(total_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    total_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    st.session_state['sumary_time'] = total_time_str

def dodaj_do_kolejki():
    st.session_state['new_df']['Index'] = st.session_state['input_index']
    st.session_state['new_df']['Price'] = st.session_state['wycena_zlecenia']
    st.session_state['choosen_parts'] = pd.concat([st.session_state['choosen_parts'],st.session_state['new_df']])
    licz_czas()

def czysc_tabele():
    clear_df = pd.DataFrame()
    st.session_state['choosen_parts'] = clear_df
    st.session_state['sumary_time'] = 0

def show_info():
    if st.session_state['info_visible'] == 0:        
        st.session_state['my_info'] = ('W pierwszej komórce wyszukaj indeks elementu. Możesz wpisać tylko początek a następnie wyszukać i wybrać interesujący cię element w rozwijanej liście poniżej. Dalej wpisz ilość elementów do wykoniania i naciśnij przycisk "Wczytaj dane". Informacje o datalu zostaną wczytane do pól po prawej stronie. Jeśli nie znajdziesz interesującego cię elementu na liście możesz uzupełnić samodzielnie pola po prawej stronie. Następnie wciśnij przycisk "Oblicz". Po oszacowaniu czasu wykonania możesz zapisać wynik w tabeli wciskając przycisk "Dodaj do kolejki". Po lewej stronie utworzy się tabela i czasy wszystkich zleceń zostaną zsumowane. Algorytm oszacowuje czas wykonania zlecenia od momentu pobrania w kiosku do momentu zaraportowania wykonania zlecenia w IPO. Jeśli operator w ramach jednego zlecenia ma do wykonania 20 kompletów w polu "Podaj ilość" należy wprowadzić 40 sztuk jednej strony.')
        st.session_state['info_visible'] = 1
    else:
        st.session_state['my_info'] = ''
        st.session_state['info_visible'] = 0

# Odczyt danych z pliku JSON
parts_df = pd.read_json('parts.json', lines=True)
parts_df['Masa'] = pd.to_numeric(parts_df['Masa'])
parts_df = parts_df.dropna(subset=['Numer'])

initialize_session_state()


st.title('Oszacuj czas gięcia zleceń w Temared by Radosław Krupa')
# my_info = ('W pierwszej komórce wyszukaj indeks elementu. Możesz wpisać tylko początek a następnie wyszukać i wybrać interesujący cię element w rozwijanej liście poniżej. Dalej wpisz ilość elementów do wykoniania i naciśnij przycisk "Wczytaj dane". Informacje o datalu zostaną wczytane do pól po prawej stronie. Jeśli nie znajdziesz interesującego cię elementu na liście możesz uzupełnić samodzielnie pola po prawej stronie. Następnie wciśnij przycisk "Oblicz". Po oszacowaniu czasu wykonania możesz zapisać wynik w tabeli wciskając przycisk "Dodaj do kolejki". Po lewej stronie utworzy się tabela i czasy wszystkich zleceń zostaną zsumowane. Algorytm oszacowuje czas wykonania zlecenia od momentu pobrania w kiosku do momentu zaraportowania wykonania zlecenia w IPO. Jeśli operator w ramach jednego zlecenia ma do wykonania 20 kompletów w polu "Podaj ilość" należy wprowadzić 40 sztuk jednej strony.')

st.button('Instrukcja obsługi', on_click=show_info)
st.markdown(f'<div class="wrapped-text">{st.session_state["my_info"]}</div>', unsafe_allow_html=True)

# Streamlit input and selection
col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.header('1. Wyszukaj element gięty:')
        options = parts_df['Numer']
        search_number = st.text_input('Wprowadź początek numeru rysunkowego do wyszukania')
        wyniki = parts_df[parts_df['Numer'].str.startswith(search_number)]['Numer'].tolist()
        choosen_draw = st.selectbox("Wybierz jeden z poniższych plików", wyniki)
        st.text(f'Wybrano plik: {choosen_draw}')
        choosen_row = parts_df.loc[parts_df['Numer'] == choosen_draw]
        st.dataframe(choosen_row)
        capacity = st.number_input('Podaj ilość', step=1, min_value=1)
        st.session_state['capacity'] = capacity    
        st.write(f'Ilość elementów do wykonania: {capacity}')
        try:
            st.session_state['name'] = choosen_row['Nazwa'].astype(str).iloc[0]
            st.session_state['index'] = choosen_row['Numer'].astype(str).iloc[0]
            st.session_state['weight'] = choosen_row['Masa'].astype(float).iloc[0]
            st.session_state['width'] = choosen_row['Rozwinięcie'].iloc[0]
            st.session_state['length'] = choosen_row['Długość'].astype(float).iloc[0]
            st.session_state['bends'] = choosen_row['ilość gięć'].iloc[0]
        except IndexError:
            st.warning('Nie znaleziono takiego indeksu')

        choosen_row['Ilość'] = st.session_state['capacity']
        st.button(label="Wczytaj dane wybranego detalu do tabeli po prawej", on_click=przechwyc_wartosci)

    
    


    with st.container(border=True):
        st.header('3. Stwórz tabelę:')
        st.dataframe(st.session_state['choosen_parts'])
        st.button(label='Wyczyść tabelę', on_click=czysc_tabele)
    st.header(f'Suma czasu: {st.session_state["sumary_time"]}')
    try:
        sum_price = st.session_state['choosen_parts']['Price'].sum()
    except:
        sum_price = 0
    st.header(f'Suma akordu: {sum_price:.4f}zł')

with col2:
    with st.container(border=True):
        st.header("2. Wprowadź dane:")
        name = st.text_input(label="Podaj nazwę", value=st.session_state['input_name'])
        index = st.text_input(label="Podaj numer rysunku", value=st.session_state['input_index'])
        length = st.number_input(label="Podaj długość", max_value=float(6100), min_value=float(0), value=float(st.session_state['input_length']), step=float(1))
        width = st.number_input(label="Podaj rozwinięcie", max_value=float(3000), min_value=float(0), value=float(st.session_state['input_width']), step=float(1))
        weigth = st.number_input(label="Podaj wagę", min_value=float(0), max_value=float(100), step=float(1), value=float(st.session_state['input_weight']))
        bends = st.number_input(label="Ilość gięć", step=int(1), min_value=int(0), max_value=int(12), value=int(st.session_state['input_bends']))
        capacity = st.number_input(label="Ilość sztuk", step=int(1), min_value=int(0), value=int(st.session_state['input_capacity']))

        st.session_state['new_df'] = pd.DataFrame({
            'Capacity': [capacity],
            'Weigth': [weigth],
            'Width': [width],
            'Length': [length],
            'Bends': [bends]
        })

        if st.button(label="Oblicz czas wykonania zlecenia dla powyższych danych"):
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

        st.button(label='Dodaj czas do kolejki zleceń po lewej', on_click= dodaj_do_kolejki)

    wycena = wycena_max(weigth, bends, 0.22, 0.25)
    st.subheader(f'Wycena elementu: {wycena:.4f}zł')
    wycena_zlecenia = wycena * capacity
    st.session_state['wycena_zlecenia'] = wycena_zlecenia
    st.subheader(f'Wycena zlecenia: {wycena_zlecenia:.4f}zł')