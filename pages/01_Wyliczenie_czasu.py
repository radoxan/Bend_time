import streamlit as st
import pycaret.regression
import pandas as pd
import time


st.title('Jak obliczony zostaje czas wykonania zlecenia?')

col1 , col2 = st.columns([5,2])
with col1:
    text = """
    <p style="text-align: justify; text-justify: inter-word; font-size: 24px">
        Do przewidywania czasu wykonania elementów program wykorzystuje regersyjny model uczenia maszynowego Random Forest Regressor.
        Przewidywany czas wykonania liczony jest od momentu pobrania zlecenia przez pracownika do czasu zaraportowania pracy w systemie. 
        Do wytrenowania modelu pobrano z systemu czas fizycznie giętych elementów.
        Ilość danych, która posłużyła do wytrenowania modelu znajduje się po prawej stronie.
    </p>
    """
    st.markdown(text, unsafe_allow_html=True)

with col2:
    st.subheader('87432 zleceń')
    st.subheader('1920 numerów rysunkowych')
    st.subheader('8 498 189 sztuk detali')
    st.subheader('9 721 233 minut pracy')
    st.subheader('20 892 138 gięć')

st.markdown('<hr>', unsafe_allow_html=True)

col3 , col4 = st.columns(2)
with col3:
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

    st.title("Oblicz czas wykonania zlecenia")

    length = st.number_input(label="Podaj długość", max_value=6100, min_value=0)
    width = st.number_input(label="Podaj rozwinięcie", max_value=3000, min_value=0)
    weigth = st.number_input(label="Podaj wagę", min_value=0, max_value=100)
    bends = st.number_input(label="Ilość gięć", step=1, min_value=0, max_value=12)
    capacity = st.number_input(label="Ilość sztuk", step=1, min_value=0)

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
with col4:
    st.text("")
    st.subheader('Wykres zależności pomiędzy poszczególymi właściwościami elementu')
    st.image('newplot.png')