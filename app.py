import streamlit as st
import pycaret.regression
import pandas as pd

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
    predict(capacity, weigth, width, length, bends)