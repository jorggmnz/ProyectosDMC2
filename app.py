import streamlit as st
import numpy as np
import pandas as pd
import librería_funciones_proyecto1 as lf


st.title("Proyecto aplicado N°1")
st.write("Módulo: N°1 de Python Fundamentals")
st.write("Año: 2026")

# Separador visual
st.divider()

st.image("Python_logo.png", width=200)
st.sidebar.image("DMC.png", width=100)
st.sidebar.title("Parámetros")

modulos = st.sidebar.selectbox ("Selecione un módulo", ["Home","Ejercicio 1: Listas", "Ejercicio 2: Arreglos con Numpy", "Ejercicio 3: Funciones", "Ejercicio 4: CRUD"])
