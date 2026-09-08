import streamlit as st
import pandas as pd


st.title("Proyecto aplicado N°2: Carga y validación de datos")
st.write("Módulo: N°2 de Python Fundamentals")
st.write("Año: 2026")

# Separador visual
st.divider()

#Mantener el df en memoria
if "df" not in st.session_state:
    st.session_state["df"] = None


# Función personalizada para clasificación (Ítem 2)
def clasificar_variables(dataframe):
    num_cols = dataframe.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = dataframe.select_dtypes(exclude=["number"]).columns.tolist()
    return num_cols, cat_cols, len(num_cols), len(cat_cols)
  
st.sidebar.title("Parámetros")

modulos = st.sidebar.selectbox ("Selecione un módulo", ["Home", "Carga del dataset",
                                                        "Ítem 1: Información general del dataset", "Ítem 2: Clasificación de variables",
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

elif modulos == "Carga del dataset":

  #Cargar el archivo
  archivo_cargado = st.file_uploader("Carga tu archivo", type=["csv"])

  #Almacenamiento del dataframe
  df = None

#Validación de la carga
if archivo_cargado is not None:
        try:
            df = pd.read_csv(archivo_cargado, sep=';')
            st.success("¡Archivo cargado correctamente!")
        
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

        df = st.session_state["df"]

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

# ÍTEM 1: INFORMACIÓN GENERAL DEL DATASET
# ----------------------------------------------------

elif modulos == "Ítem 1: Información general del dataset":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 1: Información General")

        # Tabla de tipos y nulos
        info_df = pd.DataFrame(
            {
                "Tipo de Dato": df.dtypes.astype(str),
                "Valores Nulos": df.isnull().sum(),
                "% Nulos": (df.isnull().sum() / len(df) * 100)
                .round(2)
                .astype(str)
                + "%",
            }
        )
        st.dataframe(info_df, use_container_width=True)

        #Duplicados
        duplicados = df.duplicated().sum()
        if duplicados > 0:
            st.warning(f"Se detectaron {duplicados:,} registros duplicados.")
        else:
            st.success("No hay registros duplicados.")

        #df.info()
        with st.expander("Ver salida técnica de df.info()"):
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
    else:
        st.info("Carga un archivo en el módulo correspondiente.")
