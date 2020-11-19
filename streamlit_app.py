import streamlit as st
import numpy as np
import pandas as pd
import requests
import json

st.title('Mezago - Demo')

#### menu lateral
num_locations = st.sidebar.slider("Ubicaciones a generar", min_value=3, max_value=50, value=30, step=1)
vehiculos = st.sidebar.slider("Vehiculos a generar", min_value=1, max_value=15, value=5, step=1)
texto_pickupdelivery = st.sidebar.text_area("PickUp and Delivery", value='2-5,12-4,23-24', height=10)
if len(texto_pickupdelivery) > 0:
    array = []
    texto_sep = texto_pickupdelivery.split(",")
    for elemento in texto_sep:
        elemento_separado = elemento.split("-")
        pickup_pair = [int(elemento_separado[0]), int(elemento_separado[1])]
        array.append(pickup_pair)
else:
    array = []


df = pd.DataFrame(np.random.randn(num_locations, 2) / [20, 20] + [19.400719, -99.147398] ,columns=['lat', 'lon'])


locations_list=[[19.393873, -99.196253, 'almacen']]

counter=1
for index, row in df.iterrows():
    list_element=[row[0], row[1],str(counter)]
    locations_list.append(list_element)
    counter=counter+1

df_ubicaciones = pd.DataFrame(locations_list, columns = ['Latitud', 'Longitud', 'Ubicación'])


url = "http://40.122.124.87/routing_pickupdelivery"

payload = json.dumps({"locations": locations_list,   "pickups_deliveries" : array,"num_vehicles" : vehiculos})
headers = {
    'Content-Type': 'application/json'
}
df_ubicaciones_persistido = pd.DataFrame(locations_list, columns=['latitude', 'longitude', 'Ubicación'])

response = requests.request("POST", url, headers=headers, data=payload)
col1, col2 = st.beta_columns([3, 1])
col1.subheader("Ubicaciones generadas aleatoriamente")
col1.map(df_ubicaciones_persistido)

col2.subheader("Datos generados")
col2.dataframe(df_ubicaciones)

st.header('Ruta optimizada')
st.write(response.text)
