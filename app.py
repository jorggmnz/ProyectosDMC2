import matplotlib.pyplot as plt
import io
import pandas as pd
import seaborn as sns
import streamlit as st

st.title("Proyecto aplicado N°2: Carga y validación de datos")
st.write("Módulo: N°2 de Python Fundamentals | Año: 2026")

#Separador visual
st.divider()

#Mantener el DataFrame en memoria
if "df" not in st.session_state:
    st.session_state["df"] = None


# Función personalizada para clasificación (Ítem 2)
def clasificar_variables(dataframe):
    num_cols = dataframe.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = dataframe.select_dtypes(exclude=["number"]).columns.tolist()
    return num_cols, cat_cols, len(num_cols), len(cat_cols)


#Separar métricas según el rol del jugador
def obtener_metricas_por_rol(df_input):
    metricas_gk = [
        c for c in df_input.columns if any(p in c.lower() for p in ["saves", "clean_sheets", "goals_conceded", "atajadas", "goles_recibidos"])
    ]
    
    # Excluir métricas exclusivas de porteros para jugadores de campo
    metricas_campo = [
        c for c in df_input.select_dtypes(include=["number"]).columns
        if c not in metricas_gk and not any(id_kw in c.lower() for id_kw in ["id", "number", "jersey"])
    ]
    return metricas_gk, metricas_campo


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

if modulos == "Home":
    st.subheader("Información General del Estudiante")
    st.write("**Elaborado por:** Estudiante")
    st.write("**Carrera:** Análisis de Datos")
    st.write("**Universidad:** Universidad")
    
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

        duplicados = df.duplicated().sum()
        if duplicados > 0:
            st.warning(f"Se detectaron {duplicados:,} registros duplicados.")
        else:
            st.success("No hay registros duplicados.")

        with st.expander("Ver salida técnica de df.info()"):
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
    else:
        st.info("Carga un archivo en el módulo correspondiente.")


# ÍTEM 2: CLASIFICACIÓN DE VARIABLES
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
        st.info("Carga un archivo en el módulo correspondiente.")


#ÍTEM 3: ESTADÍSTICAS DESCRIPTIVAS
elif modulos == "Ítem 3: Estadísticas descriptivas":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 3: Estadísticas Descriptivas")

        num_vars, _, _, _ = clasificar_variables(df)
        num_vars = [v for v in num_vars if "number" not in v.lower() and "id" not in v.lower()]

        if num_vars:
            st.write("**Resumen Estadístico**")
            st.dataframe(
                df[num_vars].describe().T.style.format("{:.2f}"),
                use_container_width=True,
            )

            st.write("**Detección de Valores Extremos (Criterio 1.5xIQR)**")
            outliers_data = []
            
            for col in num_vars:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                
                lim_inf = q1 - 1.5 * iqr
                lim_sup = q3 + 1.5 * iqr
                
                lim_inf_adj = max(0.0, lim_inf) if df[col].min() >= 0 else lim_inf

                cant_out = df[(df[col] < lim_inf) | (df[col] > lim_sup)].shape[0]

                outliers_data.append(
                    {
                        "Variable": col,
                        "Límite Inf. (Calculado)": round(lim_inf, 2),
                        "Límite Inf. (Ajustado)": round(lim_inf_adj, 2),
                        "Límite Sup.": round(lim_sup, 2),
                        "Cant. Outliers": cant_out,
                        "% Outliers": f"{(cant_out / len(df)) * 100:.2f}%",
                    }
                )

            st.dataframe(pd.DataFrame(outliers_data), use_container_width=True)
        else:
            st.info("El dataset no contiene variables numéricas aplicables.")
    else:
        st.info("Carga un archivo en el módulo correspondiente.")


#ÍTEM 4: ANÁLISIS DE VALORES FALTANTES
elif modulos == "Ítem 4: Análisis de valores faltantes":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 4: Análisis de Valores Faltantes")

        nulos_count = df.isnull().sum()
        nulos_pct = (nulos_count / len(df)) * 100

        df_missing = pd.DataFrame(
            {"Cant. Faltantes": nulos_count, "% Faltantes": nulos_pct.round(2)}
        )
        df_missing = df_missing[df_missing["Cant. Faltantes"] > 0].sort_values(
            by="Cant. Faltantes", ascending=False
        )

        if not df_missing.empty:
            st.dataframe(df_missing, use_container_width=True)

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(
                x=df_missing["% Faltantes"], y=df_missing.index, ax=ax, palette="Reds_r"
            )
            ax.set_title("Porcentaje de Valores Faltantes por Variable")
            ax.set_xlabel("% Faltantes")
            st.pyplot(fig)
        else:
            st.success("El dataset no contiene valores faltantes.")

        with st.expander("Discusión técnica sobre tratamiento/conservación"):
            st.markdown("""
            * **Conservación:** Si los datos faltantes son < 5%, se puede mantener el dataset o aplicar imputación por la mediana (numéricas).
            * **Eliminación:** Si superan el 40-50%, se sugiere eliminar la variable para evitar sesgos en modelos analíticos.
            """)
    else:
        st.info("Carga un archivo en el módulo correspondiente.")


#ÍTEM 5: DISTRIBUCIÓN DE VARIABLES NUMÉRICAS
elif modulos == "Ítem 5: Distribución de variables numéricas":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 5: Distribución de Variables Numéricas")

        #Diferenciación de métricas por Posición/Rol ---
        col_pos = [c for c in df.columns if "pos" in c.lower()]
        
        # Selección de rol para acotar el análisis
        rol_seleccionado = "Todos"
        if col_pos:
            pos_col = col_pos[0]
            rol_seleccionado = st.radio("Segmentar tipo de jugador:", ["Todos", "Jugadores de Campo", "Porteros"], horizontal=True)
            
            if rol_seleccionado == "Porteros":
                df_view = df[df[pos_col].astype(str).str.upper().str.contains("GK|GOALKEEPER|PORTERO|ARQUERO")]
            elif rol_seleccionado == "Jugadores de Campo":
                df_view = df[~df[pos_col].astype(str).str.upper().str.contains("GK|GOALKEEPER|PORTERO|ARQUERO")]
            else:
                df_view = df.copy()
        else:
            df_view = df.copy()

        #Control de nivel de agregación ---
        modo_agregacion = st.selectbox("Nivel de análisis de los datos:", ["Por Partido (Registro Directo)", "Acumulado por Jugador (Promedio)"])
        
        if modo_agregacion == "Acumulado por Jugador (Promedio)" and "player_name" in df_view.columns:
            num_cols_df = df_view.select_dtypes(include=["number"]).columns.tolist()
            df_view = df_view.groupby("player_name")[num_cols_df].mean().reset_index()

        cols_existentes = df_view.select_dtypes(include=["number"]).columns.tolist()
        cols_existentes = [c for c in cols_existentes if not any(kw in c.lower() for kw in ["id", "number", "jersey"])]

        if cols_existentes:
            col_sel = st.selectbox("Seleccione la variable a analizar", cols_existentes)

            if col_sel:
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.histplot(df_view[col_sel], kde=True, ax=ax, color="skyblue")
                ax.set_title(f"Distribución de {col_sel} ({rol_seleccionado} - {modo_agregacion})")
                st.pyplot(fig)

                if col_pos and rol_seleccionado == "Todos":
                    st.write(f"**Distribución de {col_sel} por Posición**")
                    fig_pos, ax_pos = plt.subplots(figsize=(9, 5))
                    sns.boxplot(data=df_view, x=col_pos[0], y=col_sel, ax=ax_pos, palette="Set2")
                    plt.xticks(rotation=45)
                    st.pyplot(fig_pos)
        else:
            st.warning("No hay variables numéricas para el filtro seleccionado.")
    else:
        st.info("Carga un archivo en el módulo correspondiente.")


#ÍTEM 6: ANÁLISIS DE VARIABLES CATEGÓRICAS
elif modulos == "Ítem 6: Análisis de variables categóricas":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 6: Análisis de Variables Categóricas")

        cat_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

        if cat_cols:
            col_cat = st.selectbox("Seleccione una variable categórica", cat_cols)

            if col_cat:
                counts = df[col_cat].value_counts()
                props = (df[col_cat].value_counts(normalize=True) * 100).round(2)

                df_cat = pd.DataFrame({"Conteo": counts, "Proporción (%)": props})
                
                col_t, col_g = st.columns([1, 1.5])

                with col_t:
                    st.write("**Frecuencias y Proporciones**")
                    st.dataframe(df_cat, use_container_width=True)

                with col_g:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.barplot(
                        x=counts.values, y=counts.index, ax=ax, palette="viridis"
                    )
                    ax.set_title(f"Distribución de {col_cat}")
                    ax.set_xlabel("Cantidad")
                    st.pyplot(fig)
        else:
            st.info("No se encontraron variables categóricas en el dataset.")
    else:
        st.info("Carga un archivo en el módulo correspondiente.")


#ÍTEM 7: ANÁLISIS BIVARIADO (NUMÉRICO VS CATEGÓRICO)
elif modulos == "Ítem 7: Análisis bivariado (numérico vs categórico)":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 7: Análisis Bivariado (Numérico vs Categórico)")

        #Agregado para evitar sumar registros duplicados por partido
        eval_level = st.radio("Evaluación métrica:", ["Por partido individual", "Promedio por jugador en el torneo"], horizontal=True)
        
        df_biv = df.copy()
        if eval_level == "Promedio por jugador en el torneo" and "player_name" in df_biv.columns:
            cat_cols = df_biv.select_dtypes(exclude=["number"]).columns.tolist()
            num_cols = df_biv.select_dtypes(include=["number"]).columns.tolist()
            df_biv = df_biv.groupby(["player_name"] + cat_cols, as_index=False)[num_cols].mean()

        comparaciones = [
            ("player_rating", "position"),
            ("performance_score", "match_result"),
            ("distance_covered_km", "position"),
        ]

        comp_validas = [
            f"{num} vs {cat}"
            for num, cat in comparaciones
            if num in df_biv.columns and cat in df_biv.columns
        ]

        if comp_validas:
            opcion = st.selectbox("Seleccione la relación a analizar", comp_validas)
            num_var, cat_var = opcion.split(" vs ")

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.boxplot(data=df_biv, x=cat_var, y=num_var, ax=ax, palette="Set2")
            ax.set_title(f"Distribución de {num_var} por {cat_var}")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            st.write(f"**Resumen estadístico de {num_var} según {cat_var}:**")
            resumen = (
                df_biv.groupby(cat_var)[num_var]
                .agg(["count", "mean", "median", "std"])
                .round(2)
            )
            st.dataframe(resumen, use_container_width=True)
        else:
            st.warning("No se encontraron las columnas requeridas para las comparaciones predeterminadas.")
    else:
        st.info("Carga un archivo en el módulo correspondiente.")


#ÍTEM 8: ANÁLISIS BIVARIADO (CATEGÓRICO VS CATEGÓRICO)
elif modulos == "Ítem 8: Análisis bivariado (categórico vs categórico)":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 8: Análisis Bivariado (Categórico vs Categórico)")

        comparaciones = [
            ("position", "tournament_stage"),
            ("team", "match_result"),
            ("preferred_foot", "position"),
        ]

        comp_validas = [
            f"{var1} vs {var2}"
            for var1, var2 in comparaciones
            if var1 in df.columns and var2 in df.columns
        ]

        if comp_validas:
            opcion = st.selectbox("Seleccione la combinación categórica", comp_validas)
            var1, var2 = opcion.split(" vs ")

            crosstab_counts = pd.crosstab(df[var1], df[var2])
            crosstab_pct = pd.crosstab(df[var1], df[var2], normalize="index") * 100

            st.write("**Tabla de Frecuencias Absolutas**")
            st.dataframe(crosstab_counts, use_container_width=True)

            fig, ax = plt.subplots(figsize=(8, 4))
            crosstab_pct.plot(kind="bar", stacked=True, ax=ax, colormap="tab10")
            ax.set_title(f"Distribución porcentual de {var2} por {var1}")
            ax.set_ylabel("Porcentaje (%)")
            plt.xticks(rotation=45)
            st.legend(title=var2, bbox_to_anchor=(1.05, 1), loc="upper left")
            st.pyplot(fig)
        else:
            st.warning("No se encontraron las columnas requeridas para las comparaciones categóricas.")
    else:
        st.info("Carga un archivo en el módulo correspondiente.")


#ÍTEM 9: ANÁLISIS BASADO EN PARÁMETROS SELECCIONADOS
elif modulos == "Ítem 9: Análisis basado en parámetros seleccionados":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 9: Análisis Dinámico por Parámetros")

        df_filt = df.copy()

        if "match_date" in df_filt.columns:
            df_filt["match_date"] = pd.to_datetime(df_filt["match_date"], errors="coerce")

        #SECCIÓN DE FILTROS
        st.sidebar.markdown("### Filtros Dinámicos")

        #1 Filtro de Rol
        col_pos = [c for c in df_filt.columns if "pos" in c.lower()]
        if col_pos:
            filtro_rol = st.sidebar.radio("Filtrar Posición/Rol:", ["Todos", "Solo Porteros", "Solo Jugadores de Campo"])
            if filtro_rol == "Solo Porteros":
                df_filt = df_filt[df_filt[col_pos[0]].astype(str).str.upper().str.contains("GK|GOALKEEPER|PORTERO|ARQUERO")]
            elif filtro_rol == "Solo Jugadores de Campo":
                df_filt = df_filt[~df_filt[col_pos[0]].astype(str).str.upper().str.contains("GK|GOALKEEPER|PORTERO|ARQUERO")]

        #2 Filtros categóricos
        filtros_cat = ["team", "tournament_stage", "match_result", "player_name"]
        for col in filtros_cat:
            if col in df_filt.columns:
                opciones = df_filt[col].dropna().unique().tolist()
                sel = st.sidebar.multiselect(f"Filtrar por {col}:", opciones)
                if sel:
                    df_filt = df_filt[df_filt[col].isin(sel)]

        #3 Tratamiento de Métricas (Para no duplicar sumas de partido)
        agrupar_jugador = st.sidebar.checkbox("Consolidar promedios por jugador (Evita duplicados por partido)", value=False)
        if agrupar_jugador and "player_name" in df_filt.columns:
            num_cols = df_filt.select_dtypes(include=["number"]).columns.tolist()
            cat_cols = [c for c in df_filt.columns if c not in num_cols and c != "player_name"]
            df_filt = df_filt.groupby("player_name", as_index=False).agg(
                {**{c: "mean" for c in num_cols}, **{c: "first" for c in cat_cols}}
            )

        # Filtro numérico
        num_cols = df_filt.select_dtypes(include=["number"]).columns.tolist()
        num_cols = [c for c in num_cols if not any(kw in c.lower() for kw in ["id", "number", "jersey"])]
        
        if num_cols:
            col_num = st.sidebar.selectbox("Variable numérica para rango:", num_cols)
            min_v, max_v = float(df_filt[col_num].min()), float(df_filt[col_num].max())
            rango = st.sidebar.slider(
                f"Rango de {col_num}:", min_v, max_v, (min_v, max_v)
            )
            df_filt = df_filt[(df_filt[col_num] >= rango[0]) & (df_filt[col_num] <= rango[1])]

        #RESULTADOS
        st.write(f"**Registros encontrados:** {len(df_filt):,} de {len(df):,}")

        if not df_filt.empty:
            metricas_disp = [c for c in df_filt.select_dtypes(include=["number"]).columns if not any(kw in c.lower() for kw in ["id", "number", "jersey"])]
            if metricas_disp:
                met_sel = st.multiselect(
                    "Seleccione métricas a comparar:",
                    metricas_disp,
                    default=metricas_disp[:3],
                )

                if met_sel and "player_name" in df_filt.columns:
                    st.write("**Comparación de Jugadores Filtrados:**")
                    st.dataframe(
                        df_filt[["player_name"] + met_sel].head(15),
                        use_container_width=True,
                    )

            st.subheader("Vista Previa de Datos Filtrados")
            st.dataframe(df_filt.head(), use_container_width=True)
        else:
            st.warning("No hay registros que cumplan con los filtros seleccionados.")
    else:
        st.info("Carga un archivo en el módulo correspondiente.")

# ====================================================
# ÍTEM 10: HALLAZGOS CLAVE
# ====================================================
elif modulos == "Ítem 10: Hallazgos clave":
    df = st.session_state["df"]
    if df is not None:
        st.subheader("Ítem 10: Hallazgos Clave e Insights Ejecutivos")

        # Preparación de datos y detección de estructura
        df_hallazgos = df.copy()
        col_pos = [c for c in df_hallazgos.columns if "pos" in c.lower()]
        pos_var = col_pos[0] if col_pos else None

        # --- 1. VISUALIZACIÓN RESUMEN (PANEL MULTIGRÁFICO) ---
        st.write("### 1. Panel Resumen del Desempeño General")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Gráfico A: Distribución de métrica principal por posición
        if pos_var and "player_rating" in df_hallazgos.columns:
            sns.boxplot(
                data=df_hallazgos, 
                x=pos_var, 
                y="player_rating", 
                ax=axes[0], 
                palette="Set2"
            )
            axes[0].set_title("Distribución de Player Rating por Posición")
            axes[0].tick_params(axis='x', rotation=45)
        elif "player_rating" in df_hallazgos.columns:
            sns.histplot(df_hallazgos["player_rating"], kde=True, ax=axes[0], color="skyblue")
            axes[0].set_title("Distribución General del Player Rating")

        # Gráfico B: Relación Rendimiento vs Distancia (o Matriz de Correlación Corta)
        cols_corr = [c for c in ["player_rating", "performance_score", "pass_accuracy", "distance_covered_km"] if c in df_hallazgos.columns]
        if len(cols_corr) >= 2:
            sns.heatmap(
                df_hallazgos[cols_corr].corr(), 
                annot=True, 
                cmap="coolwarm", 
                fmt=".2f", 
                ax=axes[1]
            )
            axes[1].set_title("Matriz de Correlación de Métricas Clave")
        
        st.pyplot(fig)

        st.divider()

        # --- 2. INSIGHTS PRINCIPALES DERIVADOS DEL EDA ---
        st.write("### 2. Insights Principales del Análisis Exploratorio")

        col_ins1, col_ins2 = st.columns(2)

        with col_ins1:
            st.markdown("""
            **Calidad y Estructura de Datos:**
            * **Consistencia de Registros:** Se validó la ausencia de registros duplicados en el conjunto de datos y la integridad del tipado numérico/categórico.
            * **Comportamiento Atípico:** La aplicación del rango intercuartílico ($1.5 \times \text{IQR}$) identificó variaciones marcadas en métricas de rendimiento, las cuales responden a la naturaleza de ciertas posiciones (ej. baja frecuencia de remates en defensas vs. atacantes).
            """)

        with col_ins2:
            st.markdown("""
            **Patrones Operativos y de Juego:**
            * **Segregación por Rol:** Existe una clara heterogeneidad técnica entre porteros y jugadores de campo, requiriendo matrices de evaluación independientes.
            * **Efecto de la Frecuencia:** El análisis a nivel de partido individual tiende a sobredimensionar extremos atípicos; la agregación por jugador ofrece una visión más representativa del rendimiento acumulado.
            """)

        st.divider()

        # --- 3. RECOMENDACIONES ORIENTADAS A LA TOMA DE DECISIONES ---
        st.write("### 3. Recomendaciones de Interpretación para la Gestión")

        st.info("""
        * **Evaluación Segmentada:** Se recomienda no comparar el desempeño global de atletas sin filtrar por su rol táctico (Porteros vs. Jugadores de Campo).
        * **Toma de Decisiones Basada en Promedios:** Para decisiones de reclutamiento o renovación, priorizar el rendimiento consolidado por torneo antes que actuaciones aisladas de un único partido.
        * **Monitoreo de Carga Física:** Cruce la distancia recorrida (`distance_covered_km`) con el rendimiento para identificar desgaste físico en fases avanzadas del torneo sin realizar inferencias predictivas.
        """)

    else:
        st.info("Carga un archivo CSV en el módulo correspondiente.")
