import io
import pandas as pd
import streamlit as st

st.title("Proyecto aplicado N°2: Carga y validación de datos")
st.write("Módulo: N°2 de Python Fundamentals | Año: 2026")

# Separador visual
st.divider()

# Inicializar st.session_state para mantener el DataFrame en memoria
if "df" not in st.session_state:
    st.session_state["df"] = None


# Función personalizada para clasificación (Ítem 2)
def clasificar_variables(dataframe):
    num_cols = dataframe.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = dataframe.select_dtypes(exclude=["number"]).columns.tolist()
    return num_cols, cat_cols, len(num_cols), len(cat_cols)

# Menú lateral
st.sidebar.title("Parámetros")
modulos = st.sidebar.selectbox(
    "Seleccione un módulo",
    [
        "Home",
        "Carga del dataset",
        "Ítem 1: Información general del dataset",
        "Ítem 2: Clasificación de variables",
        "Ítem 3: Estadísticas descriptivas",
        "Ítem 4: Análisis de valores faltantes",
        "Ítem 5: Distribución de variables numéricas",
        "Ítem 6: Análisis de variables categóricas",
        "Ítem 7: Análisis bivariado (numérico vs categórico)",
        "Ítem 8: Análisis bivariado (categórico vs categórico)",
        "Ítem 9: Análisis basado en parámetros seleccionados",
        "Ítem 10: Hallazgos clave",
    ],
)

# HOME
if modulos == "Home":
    st.subheader("Información General del Estudiante")
    st.write("**Elaborado por:** Jorge Enrique Muñoz Ccasa")
    st.write("**Carrera:** Estadística")
    st.write("**Universidad:** Universidad Nacional Mayor de San Marcos")
    
    st.divider()
    
    st.markdown(
        "Esta aplicación permite poner en práctica lo desarrollado en las clases de Python for Analytics. "
        "Tecnologías empleadas: GitHub, Streamlit y Python."
    )

#Carga del dataset
elif modulos == "Carga del dataset":
    archivo_cargado = st.file_uploader("Carga tu archivo", type=["csv"])

    if archivo_cargado is not None:
        try:
            st.session_state["df"] = pd.read_csv(archivo_cargado, sep=";")
            st.success("¡Archivo cargado correctamente!")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    df = st.session_state["df"]
    if df is not None:
        filas, columnas = df.shape
        st.subheader("Dimensiones del Dataset")
        col1, col2 = st.columns(2)
        col1.metric("Número de Filas", f"{filas:,}")
        col2.metric("Número de Columnas", f"{columnas:,}")

        st.subheader("Vista Previa (head)")
        st.dataframe(df.head(), use_container_width=True)
    else:
        st.info("Por favor, sube un archivo para continuar.")


#ÍTEM 1: INFORMACIÓN GENERAL DEL DATASET
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

        # Duplicados
        duplicados = df.duplicated().sum()
        if duplicados > 0:
            st.warning(f"Se detectaron {duplicados:,} registros duplicados.")
        else:
            st.success("No hay registros duplicados.")

        # Consola df.info()
        with st.expander("Ver salida técnica de df.info()"):
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
    else:
        st.info("Carga un archivo CSV en el módulo correspondiente.")


#ÍTEM 2: CLASIFICACIÓN DE VARIABLES
elif modulos == "Ítem 2: Clasificación de variables":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 2: Clasificación de Variables")

        num_vars, cat_vars, cant_num, cant_cat = clasificar_variables(df)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Variables", len(df.columns))
        c2.metric("Numéricas", cant_num)
        c3.metric("Categóricas", cant_cat)

        col_a, col_b = st.columns(2)
        col_a.write("**Numéricas:**")
        col_a.json(num_vars)
        col_b.write("**Categóricas:**")
        col_b.json(cat_vars)
    else:
        st.info("Carga un archivo CSV en el módulo correspondiente.")

#ESTADÍSTICAS DESCRIPTIVAS

elif modulos == "Ítem 3: Estadísticas descriptivas":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 3: Estadísticas Descriptivas")

        num_vars, _, _, _ = clasificar_variables(df)

        if num_vars:
            # Resumen .describe()
            st.write("**Resumen Estadístico**")
            st.dataframe(
                df[num_vars].describe().T.style.format("{:.2f}"),
                use_container_width=True,
            )

            # Detección preliminar de outliers (IQR)
            st.write("**Detección de Valores Extremos (Criterio 1.5xIQR)**")
            outliers_data = []
            for col in num_vars:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                cant_out = df[
                    (df[col] < lim_inf) | (df[col] > lim_sup)
                ].shape[0]

                outliers_data.append(
                    {
                        "Variable": col,
                        "Límite Inferior": round(lim_inf, 2),
                        "Límite Superior": round(lim_sup, 2),
                        "Cant. Outliers": cant_out,
                        "% Outliers": f"{(cant_out / len(df)) * 100:.2f}%",
                    }
                )

            st.dataframe(
                pd.DataFrame(outliers_data), use_container_width=True
            )
        else:
            st.info("El dataset no contiene variables numéricas.")
    else:
        st.info("Carga un archivo en el módulo correspondiente.")

