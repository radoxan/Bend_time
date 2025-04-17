import streamlit as st
import pycaret.regression
import pandas as pd

def predict(model_name, df):
    predictions = pycaret.regression.predict_model(model_name, data=df)
    time_in_minutes = float(predictions['prediction_label'].iloc[0])    
    hours = int(time_in_minutes // 60)
    minutes = int(time_in_minutes % 60)
    formatted_minutes = f"{minutes:02}"
    seconds = int((time_in_minutes - hours * 60 - minutes) * 60)
    formatted_seconds = f"{seconds:02}"
    st.header(f'Czas na wykonanie elementów to: {hours}:{formatted_minutes}:{formatted_seconds}')

st.title("Oblicz czas wykonania zlecenia.")

length = st.number_input(label="Podaj długość")
width = st.number_input(label="Podaj rozwinięcie")
weigth = st.number_input(label="Podaj wagę")
bends = st.number_input(label="Ilość gięć")
capacity = st.number_input(label="Ilość sztuk")

df_2 = pd.DataFrame({
    'Capacity': [capacity],
    'Weigth': [weigth],
    'Width': [width],
    'Length': [length],
    'Bends': [bends]
})


model = pycaret.regression.load_model('bending_time_regression_compress')
predict(model, df_2)