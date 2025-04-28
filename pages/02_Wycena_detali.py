import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

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

def get_color(number, pricing_type):
    if pricing_type == 'Wycena 1':
        color_number = 4 * (number - 1) + 4
    elif pricing_type ==  'Wycena 2':
        color_number = 4 * (number - 1) + 3
    elif pricing_type == 'Wycena 3':
        color_number = 4 * (number - 1) + 2
    elif pricing_type == 'Wycena Końcowa':
        color_number = 4 * (number - 1) + 1
    else:
        color_number = 1
    colors = {
        1: '#0000FF',  # Niebieski
        2: '#3333FF',  # Jaśniejszy niebieski
        3: '#6666FF',  # Jeszcze jaśniejszy niebieski
        4: '#9999FF',  # Najjaśniejszy niebieski
        5: '#FF0000',  # Czerwony
        6: '#FF3333',  # Jaśniejszy czerwony
        7: '#FF6666',  # Jeszcze jaśniejszy czerwony
        8: '#FF9999',  # Najjaśniejszy czerwony
        9: '#00FF00',  # Zielony
        10: '#33FF33', # Jaśniejszy zielony
        11: '#66FF66', # Jeszcze jaśniejszy zielony
        12: '#99FF99', # Najjaśniejszy zielony
        13: '#FFFF00', # Żółty
        14: '#FFFF33', # Jaśniejszy żółty
        15: '#FFFF66', # Jeszcze jaśniejszy żółty
        16: '#FFFF99', # Najjaśniejszy żółty
        17: '#00FFFF', # Cyjan
        18: '#33FFFF', # Jaśniejszy cyjan
        19: '#66FFFF', # Jeszcze jaśniejszy cyjan
        20: '#99FFFF', # Najjaśniejszy cyjan
        21: '#FF00FF', # Magenta
        22: '#FF33FF', # Jaśniejsza magenta
        23: '#FF66FF', # Jeszcze jaśniejsza magenta
        24: '#FF99FF', # Najjaśniejsza magenta
        25: '#FFA500', # Pomarańczowy
        26: '#FFB733', # Jaśniejszy pomarańczowy
        27: '#FFC966', # Jeszcze jaśniejszy pomarańczowy
        28: '#FFD999'  # Najjaśniejszy pomarańczowy
    }
    return colors.get(color_number)

wycena_1_info = r'1. (WAGA * 0.1) + ((GIĘCIA - 1.0) * (CENA - ((GIĘCIA - 1) * 0.01)))'
wycena_2_info = r'2. (CENA - ((GIĘCIA - 1) * 0.01)) * GIĘCIA'
wycena_3_info = r'3. (WAGA * 0.1) * (1.0 + (MULTI * (GIĘCIA - 1)))'

st.title("Wyceń gięcie detali")
st.text("")
text = """
<p style="text-align: justify; text-justify: inter-word; font-size: 21px">
    Wycena polega na obliczeniu wartości trzech funkcji liniowych. Następnie dla wybranej wagi należy przyjąć najwyższą wartośc spośród trzech funkcji.
</p>
"""
st.markdown(text, unsafe_allow_html=True)
st.text("")
col1, col2 = st.columns([2,3])

with col1:
    basic_price = 0.22
    basic_multi = 0.25    
    henra_multi = 1.3
    weight = st.number_input("Podaj wagę",min_value=0.1,value=0.1,step=0.01,format="%0.2f")
    bend_nums = st.number_input("Podaj ilość gięć",min_value=1,value=1,step=1,format="%d")
    price = st.number_input("Podaj minimalną cenę (Domyślnie 0.22)",min_value=0.0,value=basic_price,step=0.01,format="%0.2f")
    multi = st.number_input("Podaj współczynnik (Domyślnie 0.25)",min_value=0.0,value=basic_multi,step=0.01,format="%0.2f")
    henra = st.checkbox('HENRA')
    if henra:    
        price_sum = wycena_max(weight, bend_nums, price, multi)*henra_multi
        st.header(f"Wycena elementu: {price_sum:.4f}zł")
        price_1 = wycena_1(weight, bend_nums, price)*henra_multi
        st.subheader(f"Wycena 1: {price_1:.2f}")
        price_2 = wycena_2(bend_nums, price)*henra_multi
        st.subheader(f"Wycena 2: {price_2:.2f}")
        price_3 = wycena_3(weight, bend_nums, multi)*henra_multi
        st.subheader(f"Wycena 3: {price_3:.2f}")
    else:
        price_sum = wycena_max(weight, bend_nums, price, multi)        
        st.header(f"Wycena elementu: {price_sum:.4f}zł")
        price_1 = wycena_1(weight, bend_nums, price)
        st.subheader(f"Wycena 1: {price_1:.2f}")
        price_2 = wycena_2(bend_nums, price)
        st.subheader(f"Wycena 2: {price_2:.2f}")
        price_3 = wycena_3(weight, bend_nums, multi)
        st.subheader(f"Wycena 3: {price_3:.2f}")


with col2:
    weight = np.linspace(0, 30, 100)
    fig = go.Figure()

    choosen_bend_nums = st.multiselect('Wybierz ilość gięć', [1,2,3,4,5,6,7,8,9], default=[1,2,3])
    choosen_pricing = st.multiselect('Wybierz wycenę', ['Wycena 1','Wycena 2','Wycena 3', 'Wycena Końcowa'], default=['Wycena Końcowa'])

    for choice in choosen_bend_nums:
        wycena_1_values = [wycena_1(w, choice, price) for w in weight]
        wycena_2_values = [wycena_2(choice, price) for _ in weight]
        wycena_3_values = [wycena_3(w, choice, multi) for w in weight]
        wycena_max_values = [wycena_max(w, choice,price, multi) for w in weight]
        if 'Wycena 1' in choosen_pricing:
            fig.add_trace(go.Scatter(x=weight, y=wycena_1_values, mode='lines', name=f'wycena_1 {choice}G', line=dict(color=get_color(choice, 'Wycena 1'), width=2, dash='dash')))
        if 'Wycena 2' in choosen_pricing:
            fig.add_trace(go.Scatter(x=weight, y=wycena_2_values, mode='lines', name=f'wycena_2 {choice}G', line=dict(color=get_color(choice, 'Wycena 2'), width=2, dash='dashdot')))            
        if 'Wycena 3' in choosen_pricing:     
            fig.add_trace(go.Scatter(x=weight, y=wycena_3_values, mode='lines', name=f'wycena_3 {choice}G', line=dict(color=get_color(choice, 'Wycena 3'), width=2, dash='dot')))
        if 'Wycena Końcowa' in choosen_pricing:     
            fig.add_trace(go.Scatter(x=weight, y=wycena_max_values, mode='lines', name=f'Końcowa {choice}G', line=dict(color=get_color(choice, 'Wycena Końcowa'), width=2, dash='solid')))
    fig.update_layout(title='Wykres funkcji wyceny', xaxis_title='Waga', yaxis_title='Wycena')   
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey')


    # Wyświetlanie wykresu w Streamlit
    st.plotly_chart(fig)

    st.text('Wzory dla każdej wyceny:')
    st.text(wycena_1_info)
    st.text(wycena_2_info)
    st.text(wycena_3_info)