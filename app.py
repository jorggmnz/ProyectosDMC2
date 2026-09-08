import streamlit as st
import pandas as pd


st.title("Proyecto aplicado N°2: Carga y validación de datos")
st.write("Módulo: N°2 de Python Fundamentals")
st.write("Año: 2026")

# Separador visual
st.divider()

st.sidebar.title("Parámetros")

modulos = st.sidebar.selectbox ("Selecione un módulo", ["Home","Ítem 1: Información general del dataset", "Ítem 2: Clasificación de variables",
                                                        "Ítem 3: Estadísticas descriptivas", "Ítem 4: Análisis de valores faltantes",
                                                        "Ítem 5: Distribución de variables numéricas", "Ítem 6: Análisis de variables categóricas",
                                                        "Ítem 7: Análisis bivariado (numérico vs categórico)","Ítem 8: Análisis bivariado (categórico vs categórico)",
                                                        "Ítem 9: Análisis basado en parámetros seleccionados","Ítem 10: Hallazgos clave"])


if modulos == "Home":

  st.subheader("Información General del Estudiante")
  st.write("**Elaborado por:** Jorge Enrique Muñoz Ccasa")
  st.write("**Carrera:** Estadística")
  st.write("**Universidad:** Universidad Nacional Mayor de San Marcos")

  st.divider()

  st.markdown("""Esta aplicación permite poner en practica todo lo aprendido y desarrollado en las primeras clases
del módulo 1 Python for Analytics 
                Las tecnologías empleadas en este proyecto son Github, Streamlit y Python""") 








