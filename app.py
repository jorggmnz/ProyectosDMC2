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

elif modulos == "Ítem 1: Información general del dataset":

  #Cargar el archivo
  archivo_cargado = st.file_uploader("Carga tu archivo", type=["csv"])

  #Almacenamiento del dataframe
  df = None

#Validación de la carga
if archivo_cargado is not None:
    try:
        df = pd.read_csv(archivo_cargado, sep=',')
        st.success("¡Archivo cargado correctamente!")
        
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

# Si el df se cargo con éxito, mostrar la información solicitada
if df is not None:
    #Dimensiones del dataset (filas y columnas)
    filas, columnas = df.shape
    
    st.subheader("Dimensiones del Dataset")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Número de Filas", value=f"{filas:,}")
    with col2:
        st.metric(label="Número de Columnas", value=f"{columnas:,}")

    #Head del dataset
    st.subheader("Vista Previa (primeras filas)")
    st.dataframe(df.head(), use_container_width=True)
else:
    st.info("Por favor, sube un archivo para continuar.")


